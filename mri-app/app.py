"""
Flask Web Application for MRI Scan Analysis
Ministria e Shëndetësisë dhe Mbrojtjes Sociale - Republika e Shqipërisë

Professional Medical MRI Analysis System
Version 2.0
"""

from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Application metadata
APP_VERSION = '2.0.0'
APP_NAME = 'MRI Analysis System - Ministria e Shëndetësisë'


@app.route('/')
def index():
    """Render the main interface."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Start async MRI analysis job.
    Returns job_id for progress tracking.
    """
    import traceback
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nuk ka skedar të ngarkuar'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nuk është zgjedhur asnjë skedar'}), 400
        
        # Check file extension
        allowed_extensions = {'.nii', '.nii.gz', '.dcm', '.png', '.jpg', '.jpeg'}
        filename_lower = file.filename.lower()
        
        # Check for .nii.gz first (double extension)
        if filename_lower.endswith('.nii.gz'):
            file_ext = '.nii.gz'
        else:
            file_ext = os.path.splitext(filename_lower)[1]
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': f'Format i pavlefshëm. Formatet e pranuara: .nii, .nii.gz, .dcm, .png, .jpg'}), 400
        
        # Save uploaded file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mri_{timestamp}{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f"💾 Saving file to: {filepath}")
        file.save(filepath)
        print(f"✅ File saved successfully: {os.path.getsize(filepath)} bytes")
        
        # Create async job
        from job_manager import create_job
        from async_worker import process_analysis_async
        
        job_id = create_job(filepath, file.filename)
        print(f"📋 Job created: {job_id}")
        
        # Start async processing
        process_analysis_async(job_id, filepath)
        print(f"🚀 Async processing started for job: {job_id}")
        
        # Return job ID for polling
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Analiza filloi. Ju lutem prisni...'
        })
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"❌ Error in /analyze endpoint:")
        print(error_trace)
        return jsonify({
            'error': f'Gabim në përpunim: {str(e)}',
            'details': error_trace
        }), 500


@app.route('/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """
    Get job status and results.
    Used for polling progress.
    """
    from job_manager import get_job
    
    job = get_job(job_id)
    
    if not job:
        return jsonify({'error': 'Puna nuk u gjet'}), 404
    
    return jsonify(job)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'MRI Analysis - Ministria e Shëndetësisë',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    # For development/production deployment
    app.run(host='0.0.0.0', port=5050, debug=True, threaded=True)
