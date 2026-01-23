#!/bin/bash

# ============================================================================
# Download Test MRI Data
# Quick script to get sample MRI scans for testing
# ============================================================================

set -e

echo "=========================================="
echo "📥 Downloading Test MRI Data"
echo "=========================================="
echo ""

# Create test-data directory
mkdir -p test-data
cd test-data

echo "📁 Created test-data directory"
echo ""

# Download sample MRI scans
echo "⬇️  Downloading sample medical scans..."
echo "   These are real medical images ready for testing"
echo ""

# Option 1: Brain MRI from OpenNeuro (small sample)
if [ ! -f "brain_mri.nii.gz" ]; then
    echo "📥 Downloading brain MRI sample (10-20 MB)..."
    curl -L -o brain_mri.nii.gz \
        "https://openneuro.org/crn/datasets/ds000114/snapshots/1.0.1/files/sub-01:anat:sub-01_T1w.nii.gz" \
        2>/dev/null || echo "⚠️  Brain MRI download failed (optional)"
fi

# Option 2: Create synthetic test file using Python in Docker
echo "📥 Creating synthetic test MRI (20-30 MB)..."
docker run --rm -v "$(pwd):/data" python:3.10-slim bash -c "
pip install -q numpy nibabel && python3 << 'EOF'
import numpy as np
import nibabel as nib

# Create realistic 3D MRI volume
width, height, slices = 256, 256, 100
volume = np.zeros((width, height, slices), dtype=np.float32)

for z in range(slices):
    y, x = np.ogrid[:height, :width]
    center_x, center_y = width // 2, height // 2
    radius = 80 + z * 0.3
    body_mask = (x - center_x)**2 + (y - center_y)**2 < radius**2
    volume[:, :, z] += body_mask * (800 + np.random.randn(width, height) * 50)
    
    # Add simulated organs
    liver_x, liver_y = center_x + 30, center_y - 20
    liver_mask = (x - liver_x)**2 + (y - liver_y)**2 < 1200
    volume[:, :, z] += liver_mask * 400

volume = np.clip(volume, 0, 2000)
affine = np.diag([1.0, 1.0, 3.0, 1.0])
nifti_img = nib.Nifti1Image(volume, affine)
nib.save(nifti_img, '/data/test_mri_scan.nii.gz')
print('✅ Created synthetic MRI scan')
EOF
"

echo "✅ Test files ready!"

echo ""
echo "=========================================="
echo "✅ Test Data Ready!"
echo "=========================================="
echo ""
echo "📂 Location: $(pwd)"
echo ""
echo "📋 Available test files:"
ls -lh *.nii.gz 2>/dev/null || echo "   (downloading...)"
echo ""
echo "🚀 Next steps:"
echo "   1. Make sure app is running: ./start-mri.sh"
echo "   2. Open http://localhost:5001"
echo "   3. Upload test_sample.nii.gz"
echo "   4. Click 'Analizoni Skanimin'"
echo ""
echo "⚠️  First run will download AI models (~1.5GB)"
echo "   This may take 2-5 minutes"
echo ""
echo "=========================================="
