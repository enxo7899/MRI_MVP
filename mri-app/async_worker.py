"""
Async Worker for AI Processing
Runs AI analysis in background thread
Ministria e Shëndetësisë dhe Mbrojtjes Sociale - Republika e Shqipërisë
"""

import threading
import traceback
import os
from datetime import datetime
from engine_mri import analyze_mri_scan
from medical_report import generate_professional_report
from job_manager import update_job_status, update_job_progress, complete_job, fail_job


def process_analysis_async(job_id: str, filepath: str):
    """
    Process MRI analysis in background thread.
    
    Args:
        job_id: Job identifier
        filepath: Path to MRI file
    """
    def worker():
        try:
            print(f"🚀 Starting job {job_id} at {datetime.now().isoformat()}")
            
            # Verify file exists
            if not os.path.exists(filepath):
                fail_job(job_id, f'Skedari nuk u gjet: {filepath}')
                return
            
            # Update status to processing
            update_job_status(job_id, 'processing', started_at=datetime.now().isoformat())
            update_job_progress(job_id, 5, 'Duke verifikuar skedarin...')
            
            # Check file size
            file_size = os.path.getsize(filepath)
            print(f"📁 File size: {file_size / 1024 / 1024:.2f} MB")
            
            update_job_progress(job_id, 10, 'Duke ngarkuar skanimin...')
            
            # Run AI analysis
            update_job_progress(job_id, 20, 'Duke ekzekutuar modelin AI...')
            print(f"🤖 Running AI analysis on {filepath}")
            
            results = analyze_mri_scan(filepath)
            
            if not results.get('success', False):
                error_msg = results.get('error', 'Gabim i panjohur në analizë')
                print(f"❌ Analysis failed: {error_msg}")
                fail_job(job_id, error_msg)
                return
            
            print(f"✅ Analysis completed: {results.get('organs_detected', 0)} organs detected")
            
            # Generate professional report
            update_job_progress(job_id, 80, 'Duke gjeneruar raportin profesional...')
            
            try:
                report = generate_professional_report(results)
            except Exception as report_error:
                print(f"⚠️ Report generation error: {report_error}")
                # Create basic report if professional report fails
                report = {
                    'header': {'report_date': datetime.now().strftime('%d/%m/%Y %H:%M')},
                    'clinical_summary': {'summary_text': f"Analiza identifikoi {results.get('organs_detected', 0)} organe."},
                    'detailed_findings': results.get('organs', []),
                    'recommendations': ['Konsultohuni me një specialist.']
                }
            
            # Prepare final result
            update_job_progress(job_id, 95, 'Duke finalizuar...')
            final_result = {
                'success': True,
                'report': report,
                'organs_detected': results.get('organs_detected', 0),
                'total_organs': results.get('total_organs', 0),
                'processing_time': results.get('processing_time', 0),
                'segmentation_map': results.get('segmentation_map_base64'),
                'ai_model': results.get('ai_model', 'Unknown')
            }
            
            # Mark as completed
            complete_job(job_id, final_result)
            print(f"✅ Job {job_id} completed successfully")
            
            # Cleanup uploaded file
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"🗑️ Cleaned up: {filepath}")
            except Exception as cleanup_error:
                print(f"⚠️ Cleanup error: {cleanup_error}")
            
        except Exception as e:
            error_msg = f"{str(e)}"
            print(f"❌ Job {job_id} failed with exception: {error_msg}")
            print(f"   Traceback: {traceback.format_exc()}")
            fail_job(job_id, error_msg)
    
    # Start background thread (non-daemon so it completes even if main thread exits)
    thread = threading.Thread(target=worker, daemon=False, name=f"MRI-Analysis-{job_id[:8]}")
    thread.start()
    print(f"📋 Job {job_id} queued for processing")
