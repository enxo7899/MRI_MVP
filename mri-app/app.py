"""
Flask Web Application for MRI Scan Analysis
Ministria e Shëndetësisë dhe Mbrojtjes Sociale - Republika e Shqipërisë
"""

from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
from PIL import Image
import io
import os
import base64
from datetime import datetime
import nibabel as nib
from engine_mri import analyze_mri_scan
from translations import ANATOMY_LABELS
from medical_report import generate_professional_report

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Increase request timeout for AI processing
import signal
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Request timeout")

# Set timeout to 5 minutes for AI processing
signal.signal(signal.SIGALRM, timeout_handler)


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
    
    try:
        # Save uploaded file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"mri_{timestamp}{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create async job
        from job_manager import create_job
        from async_worker import process_analysis_async
        
        job_id = create_job(filepath, file.filename)
        
        # Start async processing
        process_analysis_async(job_id, filepath)
        
        # Return job ID for polling
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Analiza filloi. Ju lutem prisni...'
        })
    
    except Exception as e:
        return jsonify({'error': f'Gabim në përpunim: {str(e)}'}), 500


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
    # For production deployment
    app.run(host='0.0.0.0', port=5000, debug=False)
