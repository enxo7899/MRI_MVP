"""
============================================================================
MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
Platforma Kombëtare AI e Imazherisë Mjekësore

DICOM Utilities with Albanian Localization
HighDICOM Segmentation Writer
============================================================================
"""

import logging
import os
import tempfile
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pydicom
from pydicom.uid import generate_uid
from pydicom.dataset import Dataset

logger = logging.getLogger("DicomUtils")


class DicomSegmentationWriter:
    """
    DICOM SEG Writer with Albanian Metadata.
    
    Shkruan objekte DICOM Segmentation (DICOM SEG) me metadata shqiptare
    duke përdorur highdicom dhe pydicom.
    
    Writes DICOM Segmentation objects with Albanian metadata
    using highdicom and pydicom.
    """

    def __init__(
        self,
        manufacturer: str = "Republika e Shqipërisë",
        institution: str = "Ministria e Shëndetësisë dhe Mbrojtjes Sociale",
        series_description: str = "Analiza AI (Ministria)",
        software_version: str = "1.0.0",
    ):
        """
        Initialize DICOM SEG writer with Albanian metadata.
        
        Args:
            manufacturer: Manufacturer name (Albanian government)
            institution: Institution name (Ministry of Health)
            series_description: Default series description
            software_version: Software version
        """
        self.manufacturer = manufacturer
        self.institution = institution
        self.series_description = series_description
        self.software_version = software_version
        
        logger.info(f"DicomSegmentationWriter inicializuar")
        logger.info(f"  Prodhuesi: {manufacturer}")
        logger.info(f"  Institucioni: {institution}")

    def write(
        self,
        source_dicom_path: str,
        segmentation_mask: np.ndarray,
        segment_descriptions: List[Dict],
        output_path: Optional[str] = None,
        series_description: Optional[str] = None,
        series_number: int = 1000,
    ) -> str:
        """
        Shkruan DICOM SEG me etiketa shqiptare.
        Write DICOM SEG with Albanian labels.
        
        Args:
            source_dicom_path: Path to source DICOM file/directory
            segmentation_mask: Numpy array with segmentation labels
            segment_descriptions: List of segment description dicts
            output_path: Output file path (auto-generated if None)
            series_description: Series description (uses default if None)
            series_number: Series number for the DICOM SEG
            
        Returns:
            Path to written DICOM SEG file
        """
        try:
            import highdicom as hd
            from highdicom.seg import (
                Segmentation,
                SegmentDescription,
                SegmentAlgorithmTypeValues,
                SegmentationTypeValues,
            )
            from highdicom.content import AlgorithmIdentificationSequence
            from highdicom.sr.coding import CodedConcept
        except ImportError:
            logger.error("highdicom nuk është instaluar!")
            raise ImportError(
                "highdicom nuk u gjet. Instaloni me: pip install highdicom"
            )
        
        logger.info("Duke gjeneruar DICOM SEG...")
        
        # Load source DICOM
        source_images = self._load_source_dicom(source_dicom_path)
        
        if not source_images:
            raise ValueError(f"Nuk u gjetën imazhe DICOM në: {source_dicom_path}")
        
        logger.info(f"U ngarkuan {len(source_images)} imazhe DICOM burim")
        
        # Create segment descriptions with Albanian labels
        segment_descs = []
        
        for seg_info in segment_descriptions:
            label_index = seg_info.get("label_index", 1)
            label_albanian = seg_info.get("label_albanian", f"Segment {label_index}")
            label_english = seg_info.get("label_english", f"segment_{label_index}")
            snomed_code = seg_info.get("snomed_code", "123037004")
            snomed_meaning = seg_info.get("snomed_meaning", "Body structure")
            
            # Create coded concept for anatomy
            anatomy_code = CodedConcept(
                value=snomed_code,
                scheme_designator="SCT",  # SNOMED CT
                meaning=snomed_meaning,
            )
            
            # Create algorithm identification
            algorithm_id = AlgorithmIdentificationSequence(
                name="MOH Albania AI Platform",
                version=self.software_version,
                family=CodedConcept(
                    value="123109",
                    scheme_designator="DCM",
                    meaning="Machine Learning",
                ),
            )
            
            # Create segment description with Albanian label
            seg_desc = SegmentDescription(
                segment_number=label_index,
                segment_label=label_albanian,  # Albanian label
                segmented_property_category=CodedConcept(
                    value="49755003",
                    scheme_designator="SCT",
                    meaning="Morphologically abnormal structure" 
                    if "tumor" in label_english.lower() 
                    else "Anatomical structure",
                ),
                segmented_property_type=anatomy_code,
                algorithm_type=SegmentAlgorithmTypeValues.AUTOMATIC,
                algorithm_identification=algorithm_id,
                tracking_uid=generate_uid(),
                tracking_id=f"MOH-AL-{label_index:03d}",
            )
            
            segment_descs.append(seg_desc)
            logger.info(f"  Segment {label_index}: {label_albanian} ({label_english})")
        
        # Prepare mask for highdicom
        # Ensure mask is in correct format: [frames, rows, cols] for multi-frame
        mask = self._prepare_mask(segmentation_mask, len(source_images))
        
        # Create DICOM SEG
        seg = Segmentation(
            source_images=source_images,
            pixel_array=mask,
            segmentation_type=SegmentationTypeValues.BINARY,
            segment_descriptions=segment_descs,
            series_instance_uid=generate_uid(),
            series_number=series_number,
            sop_instance_uid=generate_uid(),
            instance_number=1,
            manufacturer=self.manufacturer,
            manufacturer_model_name="MOH AI Platform",
            software_versions=self.software_version,
            device_serial_number="MOH-AL-001",
            series_description=series_description or self.series_description,
            institution_name=self.institution,
            institutional_department_name="Departamenti i Teknologjisë së Informacionit",
        )
        
        # Set additional Albanian metadata
        seg.InstitutionAddress = "Bulevardi Dëshmorët e Kombit, Tiranë, Shqipëri"
        seg.StationName = "MOH-AI-STATION-01"
        
        # Generate output path if not provided
        if output_path is None:
            output_dir = tempfile.mkdtemp(prefix="moh_seg_")
            output_path = os.path.join(
                output_dir, 
                f"seg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dcm"
            )
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write DICOM SEG
        seg.save_as(output_path)
        
        logger.info(f"DICOM SEG i shkruar: {output_path}")
        logger.info(f"  SeriesDescription: {series_description or self.series_description}")
        logger.info(f"  Numri i segmenteve: {len(segment_descs)}")
        
        return output_path

    def _load_source_dicom(self, path: str) -> List[pydicom.Dataset]:
        """
        Ngarkon imazhet DICOM burim.
        Load source DICOM images.
        
        Args:
            path: Path to DICOM file or directory
            
        Returns:
            List of pydicom Dataset objects
        """
        datasets = []
        
        if os.path.isfile(path):
            # Single file
            try:
                ds = pydicom.dcmread(path)
                datasets.append(ds)
            except Exception as e:
                logger.error(f"Gabim në leximin e skedarit DICOM: {e}")
        elif os.path.isdir(path):
            # Directory with DICOM files
            for filename in sorted(os.listdir(path)):
                filepath = os.path.join(path, filename)
                try:
                    ds = pydicom.dcmread(filepath)
                    datasets.append(ds)
                except Exception:
                    continue  # Skip non-DICOM files
        else:
            logger.warning(f"Rruga nuk ekziston: {path}")
        
        # Sort by InstanceNumber or ImagePositionPatient
        if datasets:
            try:
                datasets.sort(key=lambda x: int(x.InstanceNumber) 
                             if hasattr(x, 'InstanceNumber') else 0)
            except Exception:
                pass
        
        return datasets

    def _prepare_mask(
        self, 
        mask: np.ndarray, 
        num_frames: int
    ) -> np.ndarray:
        """
        Përgatit maskën për highdicom.
        Prepare mask for highdicom.
        
        Args:
            mask: Input segmentation mask
            num_frames: Number of DICOM frames
            
        Returns:
            Properly formatted mask array
        """
        # Handle different input shapes
        if mask.ndim == 4:
            # [batch, channels, height, width] or [batch, height, width, depth]
            mask = mask.squeeze()
        
        if mask.ndim == 3:
            # [depth, height, width] -> [frames, height, width]
            # Ensure frame count matches
            if mask.shape[0] != num_frames:
                logger.warning(
                    f"Numri i frame-ve të maskës ({mask.shape[0]}) "
                    f"nuk përputhet me numrin e imazheve ({num_frames})"
                )
                # Resize or pad
                if mask.shape[0] > num_frames:
                    mask = mask[:num_frames]
                else:
                    padding = np.zeros(
                        (num_frames - mask.shape[0], *mask.shape[1:]), 
                        dtype=mask.dtype
                    )
                    mask = np.concatenate([mask, padding], axis=0)
        elif mask.ndim == 2:
            # Single frame
            mask = mask[np.newaxis, ...]
        
        # Ensure binary
        mask = (mask > 0).astype(np.uint8)
        
        return mask


def save_as_dicom_seg_albanian(
    source_dicom_path: str,
    segmentation_mask: np.ndarray,
    segment_descriptions: List[Dict],
    series_description: str = "Analiza AI (Ministria)",
    series_number: int = 1000,
    output_path: Optional[str] = None,
) -> str:
    """
    Helper function to save DICOM SEG with Albanian metadata.
    
    Funksion ndihmës për ruajtjen e DICOM SEG me metadata shqiptare.
    
    Args:
        source_dicom_path: Path to source DICOM
        segmentation_mask: Segmentation mask array
        segment_descriptions: List of segment descriptions
        series_description: Series description
        series_number: Series number
        output_path: Optional output path
        
    Returns:
        Path to saved DICOM SEG file
    """
    writer = DicomSegmentationWriter(
        manufacturer="Republika e Shqipërisë",
        institution="Ministria e Shëndetësisë dhe Mbrojtjes Sociale",
        series_description=series_description,
    )
    
    return writer.write(
        source_dicom_path=source_dicom_path,
        segmentation_mask=segmentation_mask,
        segment_descriptions=segment_descriptions,
        output_path=output_path,
        series_description=series_description,
        series_number=series_number,
    )


def create_dicom_report_albanian(
    patient_name: str,
    patient_id: str,
    study_description: str,
    findings: List[Dict[str, Any]],
    conclusion: str,
    performing_physician: str = "Dr. AI Automatik",
) -> pydicom.Dataset:
    """
    Krijon raport DICOM SR me përmbajtje shqiptare.
    Create DICOM Structured Report with Albanian content.
    
    Args:
        patient_name: Patient name
        patient_id: Patient ID
        study_description: Study description
        findings: List of finding dictionaries
        conclusion: Report conclusion
        performing_physician: Physician name
        
    Returns:
        DICOM SR dataset
    """
    # Create basic DICOM SR dataset
    ds = Dataset()
    
    # Patient Module
    ds.PatientName = patient_name
    ds.PatientID = patient_id
    
    # Study Module
    ds.StudyInstanceUID = generate_uid()
    ds.StudyDate = datetime.now().strftime("%Y%m%d")
    ds.StudyTime = datetime.now().strftime("%H%M%S")
    ds.StudyDescription = study_description
    
    # Series Module
    ds.SeriesInstanceUID = generate_uid()
    ds.SeriesNumber = 999
    ds.SeriesDescription = "Raport AI - Ministria e Shëndetësisë"
    ds.Modality = "SR"
    
    # SOP Common Module
    ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.88.11"  # Basic Text SR
    ds.SOPInstanceUID = generate_uid()
    
    # SR Document General Module
    ds.InstanceNumber = 1
    ds.CompletionFlag = "COMPLETE"
    ds.VerificationFlag = "VERIFIED"
    
    # Institution
    ds.InstitutionName = "Ministria e Shëndetësisë dhe Mbrojtjes Sociale"
    ds.InstitutionAddress = "Bulevardi Dëshmorët e Kombit, Tiranë, Shqipëri"
    ds.InstitutionalDepartmentName = "Departamenti i Imazherisë Mjekësore"
    
    # Equipment
    ds.Manufacturer = "Republika e Shqipërisë"
    ds.ManufacturerModelName = "MOH AI Platform"
    ds.SoftwareVersions = "1.0.0"
    
    # Performing Physician
    ds.PerformingPhysicianName = performing_physician
    
    logger.info(f"Raport DICOM SR i krijuar për pacientin: {patient_id}")
    
    return ds
