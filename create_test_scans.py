#!/usr/bin/env python3
"""
Create Synthetic Test MRI/CT Scans for TotalSegmentator Testing
Generates realistic synthetic scans: one healthy and one pathological
"""

import numpy as np
import nibabel as nib
import os

def create_synthetic_ct_scan(output_path, scan_type='healthy'):
    """
    Create a synthetic CT scan with realistic organ-like structures.
    
    Args:
        output_path: Where to save the NIfTI file
        scan_type: 'healthy' or 'pathological'
    """
    print(f"\n🔬 Creating {scan_type} synthetic CT scan...")
    
    # Create 3D volume (typical CT dimensions)
    # Size: 512x512x300 (realistic CT scan dimensions)
    # But we'll use smaller for faster processing: 256x256x150
    shape = (256, 256, 150)
    volume = np.zeros(shape, dtype=np.float32)
    
    # Add background noise (air = -1000 HU, soft tissue = 40-80 HU)
    volume += np.random.normal(-1000, 50, shape)
    
    # Create body outline (ellipsoid)
    print("   Creating body outline...")
    z_center, y_center, x_center = shape[2]//2, shape[1]//2, shape[0]//2
    
    for z in range(shape[2]):
        for y in range(shape[1]):
            for x in range(shape[0]):
                # Ellipsoid equation
                dist = ((x - x_center)/80)**2 + ((y - y_center)/100)**2 + ((z - z_center)/60)**2
                if dist < 1:
                    volume[x, y, z] = np.random.normal(40, 10)  # Soft tissue
    
    # Add liver (large organ, right side)
    print("   Adding liver...")
    liver_center_x = x_center + 30
    liver_center_y = y_center - 20
    liver_center_z = z_center + 10
    
    for z in range(max(0, liver_center_z-25), min(shape[2], liver_center_z+25)):
        for y in range(max(0, liver_center_y-30), min(shape[1], liver_center_y+30)):
            for x in range(max(0, liver_center_x-35), min(shape[0], liver_center_x+35)):
                dist = ((x - liver_center_x)/35)**2 + ((y - liver_center_y)/30)**2 + ((z - liver_center_z)/25)**2
                if dist < 1:
                    intensity = 55 + np.random.normal(0, 5)
                    
                    # Add pathology if needed
                    if scan_type == 'pathological':
                        # Simulate enlarged liver or lesion
                        if dist < 0.3:  # Central lesion
                            intensity = 80 + np.random.normal(0, 10)  # Hyperdense lesion
                    
                    volume[x, y, z] = intensity
    
    # Add spleen (left side)
    print("   Adding spleen...")
    spleen_center_x = x_center - 40
    spleen_center_y = y_center - 25
    spleen_center_z = z_center + 5
    
    for z in range(max(0, spleen_center_z-15), min(shape[2], spleen_center_z+15)):
        for y in range(max(0, spleen_center_y-15), min(shape[1], spleen_center_y+15)):
            for x in range(max(0, spleen_center_x-15), min(shape[0], spleen_center_x+15)):
                dist = ((x - spleen_center_x)/15)**2 + ((y - spleen_center_y)/15)**2 + ((z - spleen_center_z)/15)**2
                if dist < 1:
                    intensity = 50 + np.random.normal(0, 5)
                    
                    if scan_type == 'pathological':
                        # Simulate enlarged spleen
                        intensity = 60 + np.random.normal(0, 8)
                    
                    volume[x, y, z] = intensity
    
    # Add kidneys (both sides)
    print("   Adding kidneys...")
    for side, offset in [('left', -35), ('right', 35)]:
        kidney_center_x = x_center + offset
        kidney_center_y = y_center + 30
        kidney_center_z = z_center
        
        for z in range(max(0, kidney_center_z-20), min(shape[2], kidney_center_z+20)):
            for y in range(max(0, kidney_center_y-15), min(shape[1], kidney_center_y+15)):
                for x in range(max(0, kidney_center_x-12), min(shape[0], kidney_center_x+12)):
                    dist = ((x - kidney_center_x)/12)**2 + ((y - kidney_center_y)/15)**2 + ((z - kidney_center_z)/20)**2
                    if dist < 1:
                        volume[x, y, z] = 45 + np.random.normal(0, 5)
    
    # Add heart (center-left)
    print("   Adding heart...")
    heart_center_x = x_center - 10
    heart_center_y = y_center - 40
    heart_center_z = z_center - 20
    
    for z in range(max(0, heart_center_z-20), min(shape[2], heart_center_z+20)):
        for y in range(max(0, heart_center_y-25), min(shape[1], heart_center_y+25)):
            for x in range(max(0, heart_center_x-25), min(shape[0], heart_center_x+25)):
                dist = ((x - heart_center_x)/25)**2 + ((y - heart_center_y)/25)**2 + ((z - heart_center_z)/20)**2
                if dist < 1:
                    volume[x, y, z] = 50 + np.random.normal(0, 8)
    
    # Add lungs (both sides, air-filled)
    print("   Adding lungs...")
    for side, offset in [('left', -25), ('right', 25)]:
        lung_center_x = x_center + offset
        lung_center_y = y_center - 30
        lung_center_z = z_center - 30
        
        for z in range(max(0, lung_center_z-35), min(shape[2], lung_center_z+35)):
            for y in range(max(0, lung_center_y-40), min(shape[1], lung_center_y+40)):
                for x in range(max(0, lung_center_x-30), min(shape[0], lung_center_x+30)):
                    dist = ((x - lung_center_x)/30)**2 + ((y - lung_center_y)/40)**2 + ((z - lung_center_z)/35)**2
                    if dist < 1:
                        volume[x, y, z] = -800 + np.random.normal(0, 50)  # Air-filled
    
    # Add spine (posterior)
    print("   Adding spine...")
    spine_center_x = x_center
    spine_center_y = y_center + 60
    
    for z in range(shape[2]):
        for y in range(max(0, spine_center_y-10), min(shape[1], spine_center_y+10)):
            for x in range(max(0, spine_center_x-8), min(shape[0], spine_center_x+8)):
                dist = ((x - spine_center_x)/8)**2 + ((y - spine_center_y)/10)**2
                if dist < 1:
                    volume[x, y, z] = 300 + np.random.normal(0, 50)  # Bone density
    
    # Create NIfTI image with proper affine matrix
    # Standard CT spacing: 1mm x 1mm x 1mm
    affine = np.eye(4)
    affine[0, 0] = 1.0  # x spacing
    affine[1, 1] = 1.0  # y spacing
    affine[2, 2] = 1.0  # z spacing
    
    nifti_img = nib.Nifti1Image(volume, affine)
    
    # Save
    nib.save(nifti_img, output_path)
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    
    print(f"✅ Created: {output_path}")
    print(f"   Size: {file_size:.2f} MB")
    print(f"   Dimensions: {shape}")
    print(f"   Voxel spacing: 1.0 x 1.0 x 1.0 mm")
    
    return output_path

def main():
    """Create test scans."""
    print("\n" + "="*60)
    print("🏥 Synthetic Test Scan Generator")
    print("   Ministria e Shëndetësisë dhe Mbrojtjes Sociale")
    print("="*60)
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'test-mri-scans')
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Create healthy scan
    healthy_path = os.path.join(output_dir, 'healthy_abdomen_ct.nii.gz')
    create_synthetic_ct_scan(healthy_path, 'healthy')
    
    # Create pathological scan
    pathological_path = os.path.join(output_dir, 'pathological_abdomen_ct.nii.gz')
    create_synthetic_ct_scan(pathological_path, 'pathological')
    
    # Summary
    print("\n" + "="*60)
    print("✅ Test Scans Created Successfully!")
    print("="*60)
    
    print(f"\n📊 Healthy Scan:")
    print(f"   {healthy_path}")
    print(f"   Contains: Liver, Spleen, Kidneys, Heart, Lungs, Spine")
    print(f"   Status: Normal organs with typical intensities")
    
    print(f"\n🔬 Pathological Scan:")
    print(f"   {pathological_path}")
    print(f"   Contains: Same organs with simulated pathology")
    print(f"   Pathology: Liver lesion (hyperdense), Enlarged spleen")
    
    print("\n" + "="*60)
    print("🚀 Next Steps:")
    print("="*60)
    print("\n1. Make sure the MRI Analysis app is running:")
    print("   http://localhost:5050")
    print("\n2. Upload the HEALTHY scan first:")
    print(f"   {healthy_path}")
    print("\n3. Then upload the PATHOLOGICAL scan:")
    print(f"   {pathological_path}")
    print("\n4. Compare the AI analysis results!")
    print("\n⚠️  Note: These are synthetic scans for testing.")
    print("   TotalSegmentator should detect the organs and")
    print("   potentially identify differences between scans.")
    print("\n")

if __name__ == '__main__':
    main()
