"""
============================================================================
MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
Platforma Kombëtare AI e Imazherisë Mjekësore

TotalSegmentator Inference Engine
With Albanian Anatomical Labels and DICOM SEG Output
============================================================================
"""

import logging
import os
import tempfile
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import nibabel as nib
import torch
from monai.transforms import (
    Compose,
    LoadImaged,
    EnsureChannelFirstd,
    Orientationd,
    Spacingd,
    ScaleIntensityRanged,
    CropForegroundd,
)
from monailabel.interfaces.tasks.infer_v2 import InferType
from monailabel.tasks.infer.basic_infer import BasicInferTask
from monailabel.interfaces.utils.transform import run_transforms

from lib.utils.albanian_labels import ANATOMY_EN_TO_AL, get_snomed_code
from lib.utils.dicom_utils import save_as_dicom_seg_albanian

logger = logging.getLogger("TotalSegmentatorInfer")


class TotalSegmentatorInfer(BasicInferTask):
    """
    TotalSegmentator Inference Task with Albanian Localization.
    
    Segmenton automatikisht 104+ struktura anatomike duke përdorur
    TotalSegmentator v2 dhe gjeneron DICOM SEG me etiketa shqiptare.
    
    Automatically segments 104+ anatomical structures using
    TotalSegmentator v2 and generates DICOM SEG with Albanian labels.
    """

    # TotalSegmentator label to index mapping (v2)
    TOTALSEGMENTATOR_LABELS: Dict[int, str] = {
        1: "spleen",
        2: "kidney_right",
        3: "kidney_left",
        4: "gallbladder",
        5: "liver",
        6: "stomach",
        7: "pancreas",
        8: "adrenal_gland_right",
        9: "adrenal_gland_left",
        10: "lung_upper_lobe_left",
        11: "lung_lower_lobe_left",
        12: "lung_upper_lobe_right",
        13: "lung_middle_lobe_right",
        14: "lung_lower_lobe_right",
        15: "esophagus",
        16: "trachea",
        17: "thyroid_gland",
        18: "small_bowel",
        19: "duodenum",
        20: "colon",
        21: "urinary_bladder",
        22: "prostate",
        23: "kidney_cyst_left",
        24: "kidney_cyst_right",
        25: "sacrum",
        26: "vertebrae_S1",
        27: "vertebrae_L5",
        28: "vertebrae_L4",
        29: "vertebrae_L3",
        30: "vertebrae_L2",
        31: "vertebrae_L1",
        32: "vertebrae_T12",
        33: "vertebrae_T11",
        34: "vertebrae_T10",
        35: "vertebrae_T9",
        36: "vertebrae_T8",
        37: "vertebrae_T7",
        38: "vertebrae_T6",
        39: "vertebrae_T5",
        40: "vertebrae_T4",
        41: "vertebrae_T3",
        42: "vertebrae_T2",
        43: "vertebrae_T1",
        44: "vertebrae_C7",
        45: "vertebrae_C6",
        46: "vertebrae_C5",
        47: "vertebrae_C4",
        48: "vertebrae_C3",
        49: "vertebrae_C2",
        50: "vertebrae_C1",
        51: "heart",
        52: "aorta",
        53: "pulmonary_artery",
        54: "brachiocephalic_trunk",
        55: "subclavian_artery_right",
        56: "subclavian_artery_left",
        57: "carotid_artery_right",
        58: "carotid_artery_left",
        59: "brachiocephalic_vein_left",
        60: "brachiocephalic_vein_right",
        61: "atrial_appendage_left",
        62: "superior_vena_cava",
        63: "inferior_vena_cava",
        64: "portal_vein_and_splenic_vein",
        65: "iliac_artery_left",
        66: "iliac_artery_right",
        67: "iliac_vena_left",
        68: "iliac_vena_right",
        69: "humerus_left",
        70: "humerus_right",
        71: "scapula_left",
        72: "scapula_right",
        73: "clavicula_left",
        74: "clavicula_right",
        75: "femur_left",
        76: "femur_right",
        77: "hip_left",
        78: "hip_right",
        79: "spinal_cord",
        80: "gluteus_maximus_left",
        81: "gluteus_maximus_right",
        82: "gluteus_medius_left",
        83: "gluteus_medius_right",
        84: "gluteus_minimus_left",
        85: "gluteus_minimus_right",
        86: "autochthon_left",
        87: "autochthon_right",
        88: "iliopsoas_left",
        89: "iliopsoas_right",
        90: "brain",
        91: "skull",
        92: "rib_left_1",
        93: "rib_left_2",
        94: "rib_left_3",
        95: "rib_left_4",
        96: "rib_left_5",
        97: "rib_left_6",
        98: "rib_left_7",
        99: "rib_left_8",
        100: "rib_left_9",
        101: "rib_left_10",
        102: "rib_left_11",
        103: "rib_left_12",
        104: "rib_right_1",
        105: "rib_right_2",
        106: "rib_right_3",
        107: "rib_right_4",
        108: "rib_right_5",
        109: "rib_right_6",
        110: "rib_right_7",
        111: "rib_right_8",
        112: "rib_right_9",
        113: "rib_right_10",
        114: "rib_right_11",
        115: "rib_right_12",
        116: "sternum",
        117: "costal_cartilages",
    }

    def __init__(
        self,
        path: str,
        label_map: Dict[str, str],
        config: Any,
        network: Optional[Any] = None,
        type: InferType = InferType.SEGMENTATION,
        labels: Optional[Union[str, Sequence[str]]] = None,
        dimension: int = 3,
        description: str = "TotalSegmentator - Segmentimi Automatik",
        **kwargs,
    ):
        """
        Initialize TotalSegmentator inference task.
        
        Args:
            path: Model directory path
            label_map: Albanian label mapping dictionary
            config: Application configuration
            network: Neural network (optional, uses TotalSegmentator directly)
            type: Inference type
            labels: Label names
            dimension: Spatial dimension (3D)
            description: Task description in Albanian
        """
        self.model_path = path
        self.label_map_al = label_map
        self.app_config = config
        
        # Create Albanian labels list
        self.labels_albanian = self._create_albanian_labels()
        
        super().__init__(
            path=path,
            network=network,
            type=type,
            labels=self.labels_albanian,
            dimension=dimension,
            description=description,
            **kwargs,
        )
        
        logger.info(f"TotalSegmentator inicializuar me {len(self.labels_albanian)} etiketa")

    def _create_albanian_labels(self) -> List[str]:
        """
        Krijon listën e etiketave shqiptare.
        Create Albanian labels list from TotalSegmentator labels.
        
        Returns:
            List of Albanian anatomical labels
        """
        labels = ["background"]  # Index 0
        
        for idx in sorted(self.TOTALSEGMENTATOR_LABELS.keys()):
            eng_label = self.TOTALSEGMENTATOR_LABELS[idx]
            alb_label = self.label_map_al.get(eng_label, eng_label)
            labels.append(alb_label)
        
        return labels

    def pre_transforms(self, data: Optional[Dict] = None) -> Sequence[Callable]:
        """
        Transformimet para-përpunuese për imazhin hyrës.
        Preprocessing transforms for input image.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Sequence of transforms
        """
        return [
            LoadImaged(keys="image", reader="ITKReader"),
            EnsureChannelFirstd(keys="image"),
            Orientationd(keys="image", axcodes="RAS"),
            Spacingd(
                keys="image",
                pixdim=(1.5, 1.5, 1.5),
                mode="bilinear"
            ),
            ScaleIntensityRanged(
                keys="image",
                a_min=-1024,
                a_max=3071,
                b_min=0.0,
                b_max=1.0,
                clip=True,
            ),
        ]

    def post_transforms(self, data: Optional[Dict] = None) -> Sequence[Callable]:
        """
        Transformimet pas-përpunuese për rezultatin.
        Postprocessing transforms for output.
        
        Args:
            data: Output data dictionary
            
        Returns:
            Sequence of transforms
        """
        from monai.transforms import (
            Activationsd,
            AsDiscreted,
            Invertd,
            SaveImaged,
        )
        
        return [
            Activationsd(keys="pred", softmax=True),
            AsDiscreted(keys="pred", argmax=True),
        ]

    def inferer(self, data: Optional[Dict] = None) -> Callable:
        """
        Kthen funksionin inferer që thirret TotalSegmentator.
        Return the inferer function that calls TotalSegmentator.
        
        Args:
            data: Input data dictionary
            
        Returns:
            Inferer callable
        """
        def run_totalsegmentator(inputs: torch.Tensor) -> torch.Tensor:
            """
            Ekzekuton TotalSegmentator në imazhin hyrës.
            Execute TotalSegmentator on input image.
            
            Args:
                inputs: Input tensor [B, C, H, W, D]
                
            Returns:
                Segmentation mask tensor
            """
            try:
                from totalsegmentator.python_api import totalsegmentator
            except ImportError:
                logger.error("TotalSegmentator nuk është instaluar!")
                raise ImportError(
                    "TotalSegmentator nuk u gjet. Instaloni me: pip install TotalSegmentator"
                )
            
            # Convert tensor to numpy for TotalSegmentator
            input_np = inputs.cpu().numpy()
            
            # Process batch
            batch_size = input_np.shape[0]
            outputs = []
            
            for i in range(batch_size):
                # Create temporary NIfTI file
                with tempfile.TemporaryDirectory() as tmpdir:
                    input_path = os.path.join(tmpdir, "input.nii.gz")
                    output_path = os.path.join(tmpdir, "output.nii.gz")
                    
                    # Save input as NIfTI
                    # Remove channel dimension for NIfTI
                    img_data = input_np[i, 0]  # [H, W, D]
                    nifti_img = nib.Nifti1Image(img_data, np.eye(4))
                    nib.save(nifti_img, input_path)
                    
                    # Run TotalSegmentator
                    logger.info(f"Duke ekzekutuar TotalSegmentator për imazhin {i+1}/{batch_size}...")
                    
                    totalsegmentator(
                        input=input_path,
                        output=output_path,
                        task="total",  # Full body segmentation
                        fast=True,  # Use faster model
                        device="gpu" if torch.cuda.is_available() else "cpu",
                        quiet=True,
                    )
                    
                    # Load output
                    output_nifti = nib.load(output_path)
                    output_data = output_nifti.get_fdata()
                    
                    # Add channel dimension back
                    outputs.append(output_data[np.newaxis, ...])
                    
                    logger.info(f"Segmentimi i imazhit {i+1} përfundoi me sukses")
            
            # Stack outputs
            output_np = np.stack(outputs, axis=0)
            output_tensor = torch.from_numpy(output_np).float()
            
            return output_tensor
        
        return run_totalsegmentator

    def __call__(
        self,
        request: Dict,
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Dict:
        """
        Ekzekuton inferimin mbi imazhin e dhënë.
        Execute inference on given image.
        
        Args:
            request: Request dictionary with image path
            callbacks: Optional callbacks
            
        Returns:
            Dictionary with segmentation result
        """
        begin = time.time()
        
        logger.info("=" * 50)
        logger.info("TOTALSEGMENTATOR - Fillimi i Segmentimit")
        logger.info("=" * 50)
        
        # Get image from request
        image_path = request.get("image")
        if not image_path:
            raise ValueError("Imazhi nuk u gjet në kërkesë")
        
        logger.info(f"Imazhi hyrës: {image_path}")
        
        # Run base inference
        result = super().__call__(request, callbacks)
        
        # Add Albanian metadata
        result["labels_albanian"] = self.labels_albanian
        result["manufacturer"] = "Republika e Shqipërisë"
        result["institution"] = "Ministria e Shëndetësisë dhe Mbrojtjes Sociale"
        
        # Generate DICOM SEG if requested
        if request.get("output_dicom_seg", True):
            try:
                dicom_seg_path = self._generate_dicom_seg(
                    image_path=image_path,
                    segmentation=result.get("pred"),
                    result=result,
                )
                result["dicom_seg_path"] = dicom_seg_path
                logger.info(f"DICOM SEG i gjeneruar: {dicom_seg_path}")
            except Exception as e:
                logger.error(f"Gabim në gjenerimin e DICOM SEG: {e}")
        
        elapsed = time.time() - begin
        logger.info(f"Segmentimi përfundoi në {elapsed:.2f} sekonda")
        
        return result

    def _generate_dicom_seg(
        self,
        image_path: str,
        segmentation: np.ndarray,
        result: Dict,
    ) -> str:
        """
        Gjeneron DICOM SEG me etiketa shqiptare.
        Generate DICOM SEG with Albanian labels.
        
        Args:
            image_path: Path to source DICOM
            segmentation: Segmentation mask
            result: Result dictionary
            
        Returns:
            Path to generated DICOM SEG file
        """
        # Prepare segment descriptions with Albanian labels
        segment_descriptions = []
        
        for idx, alb_label in enumerate(self.labels_albanian):
            if idx == 0:  # Skip background
                continue
            
            eng_label = self.TOTALSEGMENTATOR_LABELS.get(idx, f"segment_{idx}")
            snomed_code, snomed_meaning = get_snomed_code(eng_label)
            
            segment_descriptions.append({
                "label_index": idx,
                "label_albanian": alb_label,
                "label_english": eng_label,
                "snomed_code": snomed_code,
                "snomed_meaning": snomed_meaning,
            })
        
        # Call DICOM SEG writer
        output_path = save_as_dicom_seg_albanian(
            source_dicom_path=image_path,
            segmentation_mask=segmentation,
            segment_descriptions=segment_descriptions,
            series_description="Analiza AI (Ministria) - TotalSegmentator",
            series_number=1001,
        )
        
        return output_path


import time  # Import at module level for timing
