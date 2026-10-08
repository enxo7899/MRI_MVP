# MRI Analysis System

Proposal-stage prototype built for Albania's Ministry of Health and Social Protection: upload a scan, get automatic organ segmentation and a clinical-style report in Albanian.

> **Medical disclaimer:** research prototype. It assists clinicians and must never be the sole basis for a clinical decision. Every AI-generated report requires review by a qualified radiologist.

## What it does

1. **Upload** a scan in NIfTI (`.nii`, `.nii.gz`), DICOM (`.dcm`) or image format (`.png`, `.jpg`).
2. **Analyse.** [TotalSegmentator](https://github.com/wasserth/TotalSegmentator) (nnU-Net, PyTorch) segments the organs in a background worker while the UI shows live progress.
3. **Report.** A generated report in Albanian summarises the segmented structures for the reviewing radiologist.

## Architecture

```
Browser ──► Flask app (app.py) ──► job queue (job_manager.py) ──► async worker (async_worker.py)
                                                                   └─► segmentation engine (engine_mri.py, TotalSegmentator / nnU-Net)
                                                                   └─► report generator (medical_report.py, translations.py)
```

- **Flask** serves the UI and a JSON API.
- Long-running segmentation runs **asynchronously**, so uploads return immediately and the UI polls for progress.
- Everything ships as a **Docker** image (`mri-app/Dockerfile`, `docker-compose-simple.yml`).

## Run it

**Docker (recommended)**
```bash
chmod +x start-mri.sh
./start-mri.sh            # then open http://localhost:5001
```

**Local**
```bash
cd mri-app
pip install -r requirements.txt
python app.py             # then open http://localhost:5000
```

Two sample abdominal CT volumes are in `test-mri-scans/`. More open datasets: [OpenNeuro](https://openneuro.org/), [IXI](https://brain-development.org/ixi-dataset/).

## Project structure

```
mri-app/
├── app.py              # Flask web server and API
├── engine_mri.py       # segmentation engine (TotalSegmentator / nnU-Net)
├── async_worker.py     # background processing
├── job_manager.py      # job queue and progress tracking
├── medical_report.py   # report generator
├── translations.py     # Albanian labels and report text
└── templates/index.html
```

## Status

Prototype built for a Ministry of Health proposal; further development depends on the proposal moving forward.

---
*Shqip:* Sistem prototip për analizën e skanimeve MRI për Ministrinë e Shëndetësisë dhe Mbrojtjes Sociale. Raportet duhet të rishikohen gjithmonë nga një radiolog i kualifikuar.
