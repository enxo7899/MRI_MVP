"""
============================================================================
MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
Platforma Kombëtare AI e Imazherisë Mjekësore

Application Configuration
Konfigurimi i Aplikacionit
============================================================================
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MinistryAppConfig:
    """
    Konfigurimi kryesor i aplikacionit MONAI Label.
    Main configuration for MONAI Label application.
    """
    
    # ========================================================================
    # GENERAL SETTINGS / PARAMETRAT E PËRGJITHSHME
    # ========================================================================
    
    # Application name in Albanian
    app_name: str = "Platforma AI e Imazherisë Mjekësore"
    
    # Application name in English
    app_name_en: str = "Medical Imaging AI Platform"
    
    # Version
    version: str = "1.0.0"
    
    # Language
    language: str = "sq-AL"  # Albanian locale
    
    # Institution information
    institution_name: str = "Ministria e Shëndetësisë dhe Mbrojtjes Sociale"
    institution_name_en: str = "Ministry of Health and Social Protection"
    institution_address: str = "Bulevardi Dëshmorët e Kombit, Tiranë, Shqipëri"
    institution_country: str = "Shqipëri"
    institution_country_code: str = "AL"
    
    # ========================================================================
    # MODEL SETTINGS / PARAMETRAT E MODELEVE
    # ========================================================================
    
    # TotalSegmentator settings
    totalsegmentator_fast: bool = True  # Use fast model for quicker inference
    totalsegmentator_task: str = "total"  # Full body segmentation
    totalsegmentator_roi_subset: Optional[List[str]] = None  # Limit to specific organs
    
    # MedSAM settings
    medsam_model_type: str = "lite"  # "lite" or "full"
    medsam_image_size: int = 256
    medsam_embed_dim: int = 256
    
    # ========================================================================
    # INFERENCE SETTINGS / PARAMETRAT E INFERIMIT
    # ========================================================================
    
    # Device settings
    device: str = "cuda"  # "cuda" or "cpu"
    
    # Batch size
    batch_size: int = 1
    
    # Number of workers for data loading
    num_workers: int = 4
    
    # Timeout for inference (seconds)
    inference_timeout: int = 900  # 15 minutes
    
    # ========================================================================
    # PREPROCESSING SETTINGS / PARAMETRAT E PARA-PËRPUNIMIT
    # ========================================================================
    
    # Target spacing for preprocessing (mm)
    target_spacing: tuple = (1.5, 1.5, 1.5)
    
    # Intensity range for CT images (HU)
    ct_intensity_min: int = -1024
    ct_intensity_max: int = 3071
    
    # Orientation code
    orientation: str = "RAS"
    
    # ========================================================================
    # DICOM SETTINGS / PARAMETRAT DICOM
    # ========================================================================
    
    # DICOM SEG settings
    dicom_seg_manufacturer: str = "Republika e Shqipërisë"
    dicom_seg_software_version: str = "1.0.0"
    dicom_seg_series_number_base: int = 1000
    
    # DICOM SR settings (for reports)
    dicom_sr_template: str = "basic_text"
    
    # ========================================================================
    # LOGGING SETTINGS / PARAMETRAT E REGJISTRIMEVE
    # ========================================================================
    
    # Log level
    log_level: str = "INFO"
    
    # Log format with Albanian context
    log_format: str = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    
    # Log date format
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    
    # ========================================================================
    # API SETTINGS / PARAMETRAT E API-s
    # ========================================================================
    
    # CORS settings
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    cors_methods: List[str] = field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE"])
    cors_headers: List[str] = field(default_factory=lambda: ["*"])
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds
    
    # ========================================================================
    # ENVIRONMENT-BASED CONFIGURATION
    # ========================================================================
    
    def __post_init__(self):
        """
        Override settings from environment variables.
        """
        # Device from environment
        if os.environ.get("MONAI_DEVICE"):
            self.device = os.environ["MONAI_DEVICE"]
        
        # Check CUDA availability
        try:
            import torch
            if self.device == "cuda" and not torch.cuda.is_available():
                self.device = "cpu"
        except ImportError:
            self.device = "cpu"
        
        # TotalSegmentator fast mode from environment
        if os.environ.get("TOTALSEG_FAST"):
            self.totalsegmentator_fast = os.environ["TOTALSEG_FAST"].lower() == "true"
        
        # Log level from environment
        if os.environ.get("LOG_LEVEL"):
            self.log_level = os.environ["LOG_LEVEL"].upper()

    @property
    def is_gpu_available(self) -> bool:
        """Check if GPU is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    @property
    def gpu_name(self) -> Optional[str]:
        """Get GPU name if available."""
        try:
            import torch
            if torch.cuda.is_available():
                return torch.cuda.get_device_name(0)
        except ImportError:
            pass
        return None
    
    def to_dict(self) -> Dict:
        """
        Convert configuration to dictionary.
        Konverto konfigurimin në fjalor.
        """
        return {
            "app_name": self.app_name,
            "app_name_en": self.app_name_en,
            "version": self.version,
            "language": self.language,
            "institution": {
                "name": self.institution_name,
                "name_en": self.institution_name_en,
                "address": self.institution_address,
                "country": self.institution_country,
            },
            "models": {
                "totalsegmentator": {
                    "fast": self.totalsegmentator_fast,
                    "task": self.totalsegmentator_task,
                },
                "medsam": {
                    "type": self.medsam_model_type,
                    "image_size": self.medsam_image_size,
                },
            },
            "inference": {
                "device": self.device,
                "gpu_available": self.is_gpu_available,
                "gpu_name": self.gpu_name,
                "batch_size": self.batch_size,
                "timeout": self.inference_timeout,
            },
            "dicom": {
                "manufacturer": self.dicom_seg_manufacturer,
                "software_version": self.dicom_seg_software_version,
            },
        }
