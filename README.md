# MRI Analysis System

## 🇦🇱 Ministria e Shëndetësisë dhe Mbrojtjes Sociale - Republika e Shqipërisë

Professional AI-powered MRI scan analysis system.

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
chmod +x start-mri.sh
./start-mri.sh
```
**Open:** http://localhost:5001

### Option 2: Local Development
```bash
cd mri-app
pip install -r requirements.txt
python app.py
```
**Open:** http://localhost:5000

---

## 📋 Features

- **AI-Powered Analysis** - Automatic organ segmentation
- **Medical-Grade Reports** - Professional Albanian reports with clinical assessments
- **Multiple Formats** - NIfTI (.nii, .nii.gz), DICOM (.dcm), images (.png, .jpg)
- **Real-time Progress** - Live progress tracking with visual feedback
- **Professional UI** - Modern, responsive medical interface

---

## 🔧 How It Works

1. **Upload** - Drag & drop or select MRI scan file
2. **Analyze** - AI processes and segments organs
3. **Report** - View professional medical report in Albanian

---

## 📁 Project Structure

```
albania-moh-ai/
├── mri-app/
│   ├── app.py              # Flask web server
│   ├── engine_mri.py       # AI segmentation engine
│   ├── async_worker.py     # Background processing
│   ├── medical_report.py   # Report generator
│   ├── job_manager.py      # Job queue management
│   ├── translations.py     # Albanian translations
│   └── templates/
│       └── index.html      # Professional UI
├── docker-compose-simple.yml
├── start-mri.sh
└── README.md
```

---

## 🧪 Test Data

Download free MRI datasets:
- [OpenNeuro](https://openneuro.org/)
- [IXI Dataset](https://brain-development.org/ixi-dataset/)

---

## ⚕️ Medical Disclaimer

This system assists medical professionals and **must not** be used as sole basis for clinical decisions. All AI-generated reports require review by qualified radiologists.

---

**© 2026 Ministria e Shëndetësisë dhe Mbrojtjes Sociale**
