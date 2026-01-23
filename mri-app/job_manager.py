"""
Job Manager for Async AI Processing
Handles long-running AI analysis jobs with progress tracking
"""

import uuid
import time
import threading
from datetime import datetime
from typing import Dict, Optional

# In-memory job storage (use Redis in production)
jobs: Dict[str, dict] = {}
job_lock = threading.Lock()


def create_job(filepath: str, filename: str) -> str:
    """
    Create a new analysis job.
    
    Args:
        filepath: Path to uploaded file
        filename: Original filename
    
    Returns:
        job_id: Unique job identifier
    """
    job_id = str(uuid.uuid4())
    
    with job_lock:
        jobs[job_id] = {
            'id': job_id,
            'filepath': filepath,
            'filename': filename,
            'status': 'queued',  # queued, processing, completed, failed
            'progress': 0,
            'message': 'Duke pritur në radhë...',
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'completed_at': None,
            'result': None,
            'error': None
        }
    
    return job_id


def update_job_progress(job_id: str, progress: int, message: str):
    """Update job progress."""
    with job_lock:
        if job_id in jobs:
            jobs[job_id]['progress'] = progress
            jobs[job_id]['message'] = message


def update_job_status(job_id: str, status: str, **kwargs):
    """Update job status and optional fields."""
    with job_lock:
        if job_id in jobs:
            jobs[job_id]['status'] = status
            for key, value in kwargs.items():
                jobs[job_id][key] = value


def get_job(job_id: str) -> Optional[dict]:
    """Get job details."""
    with job_lock:
        return jobs.get(job_id)


def complete_job(job_id: str, result: dict):
    """Mark job as completed with results."""
    with job_lock:
        if job_id in jobs:
            jobs[job_id]['status'] = 'completed'
            jobs[job_id]['progress'] = 100
            jobs[job_id]['message'] = 'Analiza u përfundua!'
            jobs[job_id]['completed_at'] = datetime.now().isoformat()
            jobs[job_id]['result'] = result


def fail_job(job_id: str, error: str):
    """Mark job as failed."""
    with job_lock:
        if job_id in jobs:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['message'] = f'Gabim: {error}'
            jobs[job_id]['error'] = error
            jobs[job_id]['completed_at'] = datetime.now().isoformat()


def cleanup_old_jobs(max_age_seconds: int = 3600):
    """Remove jobs older than max_age_seconds."""
    cutoff_time = time.time() - max_age_seconds
    
    with job_lock:
        to_remove = []
        for job_id, job in jobs.items():
            created_at = datetime.fromisoformat(job['created_at']).timestamp()
            if created_at < cutoff_time:
                to_remove.append(job_id)
        
        for job_id in to_remove:
            del jobs[job_id]
