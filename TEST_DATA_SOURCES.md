# 🧪 Test MRI Data Sources

## Where to Find Test MRI Scans

### 1. **Medical Segmentation Decathlon** (Recommended)
**Best for testing - Real medical MRI scans in NIfTI format**

```bash
# Download sample MRI scans
mkdir -p test-data
cd test-data

# Task 1: Brain Tumors (MRI)
wget http://medicaldecathlon.com/files/Task01_BrainTumour.tar
tar -xf Task01_BrainTumour.tar

# Task 2: Heart (MRI)
wget http://medicaldecathlon.com/files/Task02_Heart.tar
tar -xf Task02_Heart.tar

# Task 6: Lung (CT - also works)
wget http://medicaldecathlon.com/files/Task06_Lung.tar
tar -xf Task06_Lung.tar
```

**Files will be in**: `Task0X_*/imagesTr/*.nii.gz`

---

### 2. **The Cancer Imaging Archive (TCIA)**
**Large collection of medical imaging data**

🔗 https://www.cancerimagingarchive.net/

**Popular Collections:**
- **TCGA-GBM**: Brain MRI scans
- **TCGA-LGG**: Brain MRI scans
- **Prostate-MRI**: Prostate MRI scans
- **RIDER Lung CT**: Lung CT scans

**How to download:**
1. Visit https://www.cancerimagingarchive.net/
2. Browse Collections
3. Download NBIA Data Retriever
4. Select and download studies

---

### 3. **OpenNeuro** (Brain MRI)
**Open neuroscience data**

🔗 https://openneuro.org/

```bash
# Example: Download a brain MRI dataset
# Install AWS CLI first: pip install awscli

aws s3 sync --no-sign-request \
  s3://openneuro.org/ds000001 \
  test-data/brain-mri/
```

---

### 4. **Sample Data from TotalSegmentator**
**Official test samples**

```bash
# Download TotalSegmentator sample data
mkdir -p test-data/totalseg-samples
cd test-data/totalseg-samples

# Sample CT scan
wget https://github.com/wasserth/TotalSegmentator/raw/master/resources/test_sample.nii.gz
```

---

### 5. **Quick Test with Synthetic Data**
**Create a simple test file**

```python
# Create a synthetic NIfTI file for testing
import numpy as np
import nibabel as nib

# Create random 3D volume (simulating MRI scan)
data = np.random.rand(256, 256, 100) * 1000
img = nib.Nifti1Image(data, np.eye(4))

# Save
nib.save(img, 'test-data/synthetic_mri.nii.gz')
```

---

## 📋 Recommended Test Files

### For Initial Testing:
1. **Brain MRI**: Task01_BrainTumour from Medical Decathlon
2. **Abdominal CT**: Task06_Lung from Medical Decathlon
3. **Synthetic**: Create using Python script above

### File Formats Supported:
- ✅ `.nii` - NIfTI format
- ✅ `.nii.gz` - Compressed NIfTI (recommended)
- ✅ `.dcm` - DICOM (will be converted)
- ✅ `.png`, `.jpg` - Images (will be converted)

---

## 🚀 Quick Start Testing

### Option 1: Download Medical Decathlon Sample

```bash
cd /Users/enxom/Desktop/MRI_MVP/albania-moh-ai

# Create test data directory
mkdir -p test-data
cd test-data

# Download brain MRI sample (small dataset)
wget https://github.com/wasserth/TotalSegmentator/raw/master/resources/test_sample.nii.gz

# This file is ready to upload!
```

### Option 2: Use Existing Medical Images

If you have access to medical imaging systems:
- Export a study as NIfTI or DICOM
- Upload directly to http://localhost:5001

### Option 3: Convert DICOM to NIfTI

```bash
# Install dcm2niix
brew install dcm2niix  # macOS
# or
sudo apt-get install dcm2niix  # Linux

# Convert DICOM folder to NIfTI
dcm2niix -o output_folder input_dicom_folder
```

---

## 📊 Expected Results

### For Brain MRI:
- **Detected**: Brain, Cerebellum, Brainstem
- **Volume**: ~1200-1500 ml (brain)
- **Processing**: 10-30 seconds (first run downloads models)

### For Abdominal CT/MRI:
- **Detected**: Liver, Spleen, Kidneys, Heart, Pancreas, Stomach
- **Volume**: Liver ~1400ml, Spleen ~180ml, etc.
- **Processing**: 15-45 seconds

### For Chest CT:
- **Detected**: Lungs, Heart, Aorta, Esophagus
- **Volume**: Lungs ~4000-6000ml combined
- **Processing**: 10-30 seconds

---

## ⚠️ Important Notes

### First Run:
- **Model Download**: TotalSegmentator will download ~1.5GB of models on first use
- **Time**: First analysis may take 2-5 minutes
- **Subsequent runs**: Much faster (5-30 seconds)

### File Size:
- **Typical MRI**: 10-100 MB compressed (.nii.gz)
- **Typical CT**: 50-200 MB compressed
- **Max upload**: 100 MB (configurable in app.py)

### Quality:
- **Best results**: Full 3D MRI/CT scans in NIfTI format
- **Good results**: DICOM files
- **Limited results**: 2D images (converted to 3D)

---

## 🔗 Direct Download Links

### Ready-to-Use Test Files:

1. **Brain MRI Sample**
   ```
   https://github.com/wasserth/TotalSegmentator/raw/master/resources/test_sample.nii.gz
   ```

2. **Medical Decathlon - Brain**
   ```
   http://medicaldecathlon.com/files/Task01_BrainTumour.tar
   ```

3. **Medical Decathlon - Heart**
   ```
   http://medicaldecathlon.com/files/Task02_Heart.tar
   ```

---

## 📝 Testing Workflow

```bash
# 1. Download test file
cd /Users/enxom/Desktop/MRI_MVP/albania-moh-ai/test-data
wget https://github.com/wasserth/TotalSegmentator/raw/master/resources/test_sample.nii.gz

# 2. Make sure app is running
cd ..
./start-mri.sh

# 3. Open browser
open http://localhost:5001

# 4. Upload test_sample.nii.gz

# 5. Click "Analizoni Skanimin"

# 6. Wait for results (first run: 2-5 min, subsequent: 10-30 sec)

# 7. View Albanian report with detected organs!
```

---

## 🆘 Troubleshooting

### "File too large"
- Compress with: `gzip yourfile.nii` → creates `yourfile.nii.gz`
- Or increase `MAX_CONTENT_LENGTH` in `app.py`

### "Invalid format"
- Ensure file is `.nii`, `.nii.gz`, `.dcm`, or image
- Convert DICOM: `dcm2niix -o output input_folder`

### "Model download failed"
- Check internet connection
- Models download automatically on first use
- Retry the analysis

### "Processing timeout"
- First run downloads models (2-5 minutes)
- Subsequent runs are faster
- Check Docker logs: `docker-compose -f docker-compose-simple.yml logs -f`

---

## 📞 Support

For issues with test data:
- Medical Decathlon: http://medicaldecathlon.com/
- TCIA: https://www.cancerimagingarchive.net/
- TotalSegmentator: https://github.com/wasserth/TotalSegmentator

---

**Ready to test! Download a sample and upload to http://localhost:5001** 🚀
