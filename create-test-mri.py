#!/usr/bin/env python3
"""
Generate realistic test MRI scan for testing
Creates a 3D volume with simulated anatomy
"""

import numpy as np
import nibabel as nib
import os

print("🧠 Generating realistic test MRI scan...")

# Create realistic 3D MRI volume (256x256x100 slices)
# Typical MRI dimensions
width, height, slices = 256, 256, 100

# Initialize volume
volume = np.zeros((width, height, slices), dtype=np.float32)

# Add simulated anatomical structures with realistic intensities
for z in range(slices):
    # Create circular body outline
    y, x = np.ogrid[:height, :width]
    center_x, center_y = width // 2, height // 2
    radius = 80 + z * 0.3  # Varying radius
    
    # Body tissue (medium intensity)
    body_mask = (x - center_x)**2 + (y - center_y)**2 < radius**2
    volume[:, :, z] += body_mask * (800 + np.random.randn(width, height) * 50)
    
    # Simulated organs (higher intensity)
    # Liver-like structure
    liver_x, liver_y = center_x + 30, center_y - 20
    liver_mask = (x - liver_x)**2 + (y - liver_y)**2 < 1200
    volume[:, :, z] += liver_mask * 400
    
    # Spleen-like structure
    spleen_x, spleen_y = center_x - 40, center_y - 15
    spleen_mask = (x - spleen_x)**2 + (y - spleen_y)**2 < 400
    volume[:, :, z] += spleen_mask * 300
    
    # Kidney-like structures
    kidney1_x, kidney1_y = center_x + 35, center_y + 25
    kidney1_mask = (x - kidney1_x)**2 + (y - kidney1_y)**2 < 300
    volume[:, :, z] += kidney1_mask * 350
    
    kidney2_x, kidney2_y = center_x - 35, center_y + 25
    kidney2_mask = (x - kidney2_x)**2 + (y - kidney2_y)**2 < 300
    volume[:, :, z] += kidney2_mask * 350
    
    # Add noise for realism
    volume[:, :, z] += np.random.randn(width, height) * 20

# Clip values to realistic MRI range
volume = np.clip(volume, 0, 2000)

# Create NIfTI image with proper header
# Set voxel spacing (1mm x 1mm x 3mm - typical for abdominal MRI)
affine = np.diag([1.0, 1.0, 3.0, 1.0])
nifti_img = nib.Nifti1Image(volume, affine)

# Set proper header information
nifti_img.header['descrip'] = b'Simulated abdominal MRI scan for testing'
nifti_img.header['pixdim'][1:4] = [1.0, 1.0, 3.0]  # voxel dimensions in mm

# Save as compressed NIfTI
output_path = 'test-data/test_mri_scan.nii.gz'
os.makedirs('test-data', exist_ok=True)
nib.save(nifti_img, output_path)

# Get file size
file_size_mb = os.path.getsize(output_path) / (1024 * 1024)

print(f"✅ Created: {output_path}")
print(f"📊 Dimensions: {width}x{height}x{slices}")
print(f"💾 Size: {file_size_mb:.1f} MB")
print(f"🔬 Voxel spacing: 1.0 x 1.0 x 3.0 mm")
print(f"🏥 Simulated organs: Liver, Spleen, Kidneys")
print("")
print("Ready to upload to http://localhost:5001")
