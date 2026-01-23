"""
============================================================================
MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
Platforma Kombëtare AI e Imazherisë Mjekësore

MedSAM/LiteMedSAM Interactive Segmentation Engine
Segmentimi Interaktiv me Bounding Box Prompts
============================================================================
"""

import logging
import os
import tempfile
import time
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import torch
import torch.nn.functional as F
from monailabel.interfaces.tasks.infer_v2 import InferType
from monailabel.tasks.infer.basic_infer import BasicInferTask

from lib.utils.albanian_labels import ANATOMY_EN_TO_AL
from lib.utils.dicom_utils import save_as_dicom_seg_albanian

logger = logging.getLogger("MedSAMInfer")


class MedSAMInfer(BasicInferTask):
    """
    MedSAM/LiteMedSAM Interactive Segmentation Task.
    
    Ofron segmentim interaktiv bazuar në kutinë kufizuese (bounding box).
    Përdoruesi specifikon një kuti rreth rajonit të interesit dhe
    modeli gjeneron automatikisht maskën e segmentimit.
    
    Provides interactive segmentation based on bounding box prompts.
    User specifies a bounding box around the region of interest and
    the model automatically generates the segmentation mask.
    
    Output labeled as "Zonë e Përzgjedhur" (Selected Region) in Albanian.
    """

    def __init__(
        self,
        path: str,
        config: Any,
        network: Optional[Any] = None,
        type: InferType = InferType.DEEPEDIT,  # Interactive type
        labels: Optional[Union[str, Sequence[str]]] = None,
        dimension: int = 3,
        description: str = "Segmentimi Interaktiv (MedSAM)",
        **kwargs,
    ):
        """
        Initialize MedSAM inference task.
        
        Args:
            path: Model directory path
            config: Application configuration
            network: Neural network (loaded from checkpoint)
            type: Inference type (DEEPEDIT for interactive)
            labels: Label names
            dimension: Spatial dimension
            description: Task description in Albanian
        """
        self.model_path = path
        self.app_config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Albanian labels for interactive segmentation
        self.labels_albanian = [
            "background",
            "Zonë e Përzgjedhur",  # Selected Region
        ]
        
        # Model will be loaded lazily
        self.model = None
        self.model_loaded = False
        
        super().__init__(
            path=path,
            network=network,
            type=type,
            labels=self.labels_albanian,
            dimension=dimension,
            description=description,
            **kwargs,
        )
        
        logger.info("MedSAM Interaktiv inicializuar")
        logger.info(f"Pajisja: {self.device}")

    def _load_model(self):
        """
        Ngarkon modelin MedSAM/LiteMedSAM.
        Load MedSAM/LiteMedSAM model.
        """
        if self.model_loaded:
            return
        
        logger.info("Duke ngarkuar modelin MedSAM...")
        
        try:
            # Try to load LiteMedSAM (lighter version)
            model_checkpoint = os.path.join(
                self.model_path, 
                "lite_medsam.pth"
            )
            
            if os.path.exists(model_checkpoint):
                self.model = self._build_lite_medsam()
                checkpoint = torch.load(model_checkpoint, map_location=self.device)
                self.model.load_state_dict(checkpoint["model"])
                logger.info("LiteMedSAM ngarkuar nga checkpoint lokal")
            else:
                # Download or use default SAM
                self.model = self._build_sam_model()
                logger.info("SAM model ngarkuar")
            
            self.model.to(self.device)
            self.model.eval()
            self.model_loaded = True
            
            logger.info("Modeli MedSAM gati për inferim")
            
        except Exception as e:
            logger.error(f"Gabim në ngarkimin e modelit: {e}")
            raise

    def _build_lite_medsam(self) -> torch.nn.Module:
        """
        Ndërton arkitekturën LiteMedSAM.
        Build LiteMedSAM architecture.
        
        Returns:
            LiteMedSAM model
        """
        # Simplified LiteMedSAM architecture
        # In production, use the full LiteMedSAM implementation
        
        class LiteMedSAMEncoder(torch.nn.Module):
            """Lightweight image encoder for medical images."""
            
            def __init__(self, img_size: int = 256, embed_dim: int = 256):
                super().__init__()
                self.img_size = img_size
                self.embed_dim = embed_dim
                
                # Convolutional encoder
                self.encoder = torch.nn.Sequential(
                    torch.nn.Conv2d(1, 64, 3, padding=1),
                    torch.nn.BatchNorm2d(64),
                    torch.nn.ReLU(inplace=True),
                    torch.nn.MaxPool2d(2),
                    
                    torch.nn.Conv2d(64, 128, 3, padding=1),
                    torch.nn.BatchNorm2d(128),
                    torch.nn.ReLU(inplace=True),
                    torch.nn.MaxPool2d(2),
                    
                    torch.nn.Conv2d(128, 256, 3, padding=1),
                    torch.nn.BatchNorm2d(256),
                    torch.nn.ReLU(inplace=True),
                    torch.nn.MaxPool2d(2),
                    
                    torch.nn.Conv2d(256, embed_dim, 3, padding=1),
                    torch.nn.BatchNorm2d(embed_dim),
                    torch.nn.ReLU(inplace=True),
                )
            
            def forward(self, x: torch.Tensor) -> torch.Tensor:
                return self.encoder(x)

        class LiteMedSAMDecoder(torch.nn.Module):
            """Mask decoder with prompt embeddings."""
            
            def __init__(self, embed_dim: int = 256):
                super().__init__()
                self.embed_dim = embed_dim
                
                # Box prompt encoder
                self.box_encoder = torch.nn.Sequential(
                    torch.nn.Linear(4, 128),
                    torch.nn.ReLU(inplace=True),
                    torch.nn.Linear(128, embed_dim),
                )
                
                # Decoder
                self.decoder = torch.nn.Sequential(
                    torch.nn.ConvTranspose2d(embed_dim * 2, 128, 4, stride=2, padding=1),
                    torch.nn.BatchNorm2d(128),
                    torch.nn.ReLU(inplace=True),
                    
                    torch.nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
                    torch.nn.BatchNorm2d(64),
                    torch.nn.ReLU(inplace=True),
                    
                    torch.nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),
                    torch.nn.BatchNorm2d(32),
                    torch.nn.ReLU(inplace=True),
                    
                    torch.nn.Conv2d(32, 1, 1),
                )
            
            def forward(
                self, 
                image_embeddings: torch.Tensor, 
                box_coords: torch.Tensor
            ) -> torch.Tensor:
                # Encode box prompt
                box_embed = self.box_encoder(box_coords)
                box_embed = box_embed.unsqueeze(-1).unsqueeze(-1)
                box_embed = box_embed.expand(-1, -1, 
                                            image_embeddings.shape[2], 
                                            image_embeddings.shape[3])
                
                # Concatenate and decode
                combined = torch.cat([image_embeddings, box_embed], dim=1)
                mask = self.decoder(combined)
                
                return mask

        class LiteMedSAM(torch.nn.Module):
            """Complete LiteMedSAM model."""
            
            def __init__(self, img_size: int = 256, embed_dim: int = 256):
                super().__init__()
                self.img_size = img_size
                self.encoder = LiteMedSAMEncoder(img_size, embed_dim)
                self.decoder = LiteMedSAMDecoder(embed_dim)
            
            def forward(
                self, 
                image: torch.Tensor, 
                box_coords: torch.Tensor
            ) -> torch.Tensor:
                # Normalize box coordinates to [0, 1]
                box_normalized = box_coords / self.img_size
                
                # Encode image
                image_embed = self.encoder(image)
                
                # Decode with box prompt
                mask = self.decoder(image_embed, box_normalized)
                
                # Resize to original size
                mask = F.interpolate(
                    mask, 
                    size=(self.img_size, self.img_size), 
                    mode='bilinear', 
                    align_corners=False
                )
                
                return mask
        
        return LiteMedSAM()

    def _build_sam_model(self) -> torch.nn.Module:
        """
        Ndërton modelin SAM standard.
        Build standard SAM model (fallback).
        
        Returns:
            SAM model or simplified version
        """
        try:
            from segment_anything import sam_model_registry, SamPredictor
            
            # Try to load SAM vit_b (smallest variant)
            sam_checkpoint = os.path.join(self.model_path, "sam_vit_b.pth")
            
            if os.path.exists(sam_checkpoint):
                sam = sam_model_registry["vit_b"](checkpoint=sam_checkpoint)
                return sam
            else:
                logger.warning("SAM checkpoint nuk u gjet, duke përdorur model të thjeshtuar")
                return self._build_lite_medsam()
                
        except ImportError:
            logger.warning("segment-anything nuk është instaluar, duke përdorur LiteMedSAM")
            return self._build_lite_medsam()

    def pre_transforms(self, data: Optional[Dict] = None) -> Sequence[Callable]:
        """
        Transformimet para-përpunuese.
        Preprocessing transforms.
        """
        from monai.transforms import (
            LoadImaged,
            EnsureChannelFirstd,
            Orientationd,
            ScaleIntensityRanged,
            Resized,
        )
        
        return [
            LoadImaged(keys="image", reader="ITKReader"),
            EnsureChannelFirstd(keys="image"),
            Orientationd(keys="image", axcodes="RAS"),
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
        Transformimet pas-përpunuese.
        Postprocessing transforms.
        """
        from monai.transforms import AsDiscreted
        
        return [
            AsDiscreted(keys="pred", threshold=0.5),
        ]

    def inferer(self, data: Optional[Dict] = None) -> Callable:
        """
        Kthen funksionin inferer për MedSAM.
        Return inferer function for MedSAM.
        """
        def run_medsam(
            inputs: torch.Tensor,
            box_coords: Optional[torch.Tensor] = None,
        ) -> torch.Tensor:
            """
            Ekzekuton MedSAM me bounding box prompt.
            Execute MedSAM with bounding box prompt.
            
            Args:
                inputs: Input image tensor [B, C, H, W] or [B, C, H, W, D]
                box_coords: Bounding box [x1, y1, x2, y2] or [x1, y1, z1, x2, y2, z2]
                
            Returns:
                Segmentation mask tensor
            """
            # Ensure model is loaded
            self._load_model()
            
            # Handle 3D volumes by processing slice by slice
            is_3d = len(inputs.shape) == 5
            
            if is_3d:
                # Get the slice specified by box_coords z coordinate
                batch_size, channels, height, width, depth = inputs.shape
                
                # Process middle slice if no specific slice given
                if box_coords is None:
                    z_slice = depth // 2
                    box_2d = None
                else:
                    # Extract z coordinate and 2D box
                    z_slice = int(box_coords[2].item() if len(box_coords) > 4 else depth // 2)
                    box_2d = box_coords[:4] if len(box_coords) >= 4 else None
                
                # Extract 2D slice
                inputs_2d = inputs[..., z_slice]  # [B, C, H, W]
            else:
                inputs_2d = inputs
                box_2d = box_coords
            
            # Resize to model expected size
            original_size = inputs_2d.shape[-2:]
            target_size = (256, 256)
            
            inputs_resized = F.interpolate(
                inputs_2d.float(),
                size=target_size,
                mode='bilinear',
                align_corners=False
            )
            
            # Default box if not provided (full image)
            if box_2d is None:
                box_2d = torch.tensor(
                    [10, 10, target_size[0] - 10, target_size[1] - 10],
                    device=self.device,
                    dtype=torch.float32
                )
            else:
                # Scale box coordinates
                scale_x = target_size[1] / original_size[1]
                scale_y = target_size[0] / original_size[0]
                box_2d = box_2d.clone().float()
                box_2d[0] *= scale_x
                box_2d[1] *= scale_y
                box_2d[2] *= scale_x
                box_2d[3] *= scale_y
            
            # Run model
            with torch.no_grad():
                inputs_resized = inputs_resized.to(self.device)
                box_2d = box_2d.to(self.device)
                
                # Handle batch
                if len(box_2d.shape) == 1:
                    box_2d = box_2d.unsqueeze(0).expand(inputs_resized.shape[0], -1)
                
                mask = self.model(inputs_resized, box_2d)
                mask = torch.sigmoid(mask)
            
            # Resize back to original size
            mask = F.interpolate(
                mask,
                size=original_size,
                mode='bilinear',
                align_corners=False
            )
            
            # If 3D, create volume mask
            if is_3d:
                # Create empty volume
                volume_mask = torch.zeros(
                    (batch_size, 1, height, width, depth),
                    device=mask.device,
                    dtype=mask.dtype
                )
                volume_mask[..., z_slice] = mask
                return volume_mask
            
            return mask
        
        return run_medsam

    def __call__(
        self,
        request: Dict,
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Dict:
        """
        Ekzekuton segmentimin interaktiv.
        Execute interactive segmentation.
        
        Args:
            request: Request with image and bounding box
            callbacks: Optional callbacks
            
        Returns:
            Segmentation result
        """
        begin = time.time()
        
        logger.info("=" * 50)
        logger.info("MEDSAM - Segmentimi Interaktiv")
        logger.info("=" * 50)
        
        # Extract bounding box from request
        box_coords = request.get("box", request.get("bounding_box"))
        if box_coords is not None:
            if isinstance(box_coords, list):
                box_coords = torch.tensor(box_coords, dtype=torch.float32)
            logger.info(f"Kutia kufizuese: {box_coords.tolist()}")
        else:
            logger.warning("Kutia kufizuese nuk u specifikua, duke përdorur të paracaktuar")
        
        # Store box coords for inferer
        request["_box_coords"] = box_coords
        
        # Run base inference
        result = super().__call__(request, callbacks)
        
        # Add Albanian metadata
        result["label"] = "Zonë e Përzgjedhur"
        result["label_english"] = "Selected Region"
        result["manufacturer"] = "Republika e Shqipërisë"
        result["institution"] = "Ministria e Shëndetësisë dhe Mbrojtjes Sociale"
        result["model"] = "MedSAM Interaktiv"
        
        # Generate DICOM SEG if requested
        if request.get("output_dicom_seg", False):
            try:
                image_path = request.get("image")
                dicom_seg_path = save_as_dicom_seg_albanian(
                    source_dicom_path=image_path,
                    segmentation_mask=result.get("pred"),
                    segment_descriptions=[{
                        "label_index": 1,
                        "label_albanian": "Zonë e Përzgjedhur",
                        "label_english": "selected_region",
                        "snomed_code": "123037004",
                        "snomed_meaning": "Body structure",
                    }],
                    series_description="Analiza AI (Ministria) - Segmentim Interaktiv",
                    series_number=1002,
                )
                result["dicom_seg_path"] = dicom_seg_path
                logger.info(f"DICOM SEG i gjeneruar: {dicom_seg_path}")
            except Exception as e:
                logger.error(f"Gabim në gjenerimin e DICOM SEG: {e}")
        
        elapsed = time.time() - begin
        logger.info(f"Segmentimi interaktiv përfundoi në {elapsed:.2f} sekonda")
        
        return result
