"""
Async Worker for AI Processing
Runs AI analysis in background thread
"""

import threading
import traceback
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
            # Update status to processing
            update_job_status(job_id, 'processing', started_at=None)
            update_job_progress(job_id, 10, 'Duke ngarkuar skanimin...')
            
            # Run AI analysis
            update_job_progress(job_id, 20, 'Duke ekzekutuar modelin AI...')
            results = analyze_mri_scan(filepath)
            
            if not results['success']:
                fail_job(job_id, results.get('error', 'Gabim i panjohur'))
                return
            
            # Generate professional report
            update_job_progress(job_id, 80, 'Duke gjeneruar raportin profesional...')
            report = generate_professional_report(results)
            
            # Prepare final result
            update_job_progress(job_id, 95, 'Duke finalizuar...')
            final_result = {
                'success': True,
                'report': report,
                'organs_detected': results['organs_detected'],
                'total_organs': results['total_organs'],
                'processing_time': results.get('processing_time', 0),
                'segmentation_map': results.get('segmentation_map_base64')
            }
            
            # Mark as completed
            complete_job(job_id, final_result)
            
        except Exception as e:
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            print(f"❌ Job {job_id} failed: {error_msg}")
            fail_job(job_id, str(e))
    
    # Start background thread
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
