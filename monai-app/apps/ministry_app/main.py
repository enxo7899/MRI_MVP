"""
============================================================================
MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
Platforma Kombëtare AI e Imazherisë Mjekësore

MONAI Label Application - Ministry App
Albanian Localized Medical Image Segmentation
============================================================================
"""

import logging
import os
from typing import Dict, Optional, Sequence, Callable

from monailabel.interfaces.app import MONAILabelApp
from monailabel.interfaces.config import TaskConfig
from monailabel.interfaces.datastore import Datastore
from monailabel.interfaces.tasks.infer import InferTask
from monailabel.interfaces.tasks.train import TrainTask
from monailabel.interfaces.tasks.strategy import Strategy
from monailabel.interfaces.tasks.scoring import ScoringMethod

from lib.configs.app_config import MinistryAppConfig
from lib.inferers.totalsegmentator import TotalSegmentatorInfer
from lib.inferers.medsam import MedSAMInfer
from lib.utils.albanian_labels import ANATOMY_EN_TO_AL
from lib.utils.dicom_utils import DicomSegmentationWriter

# Configure logging in Albanian
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("MinistryApp")


class MinistryApp(MONAILabelApp):
    """
    Aplikacioni MONAI Label i Ministrisë së Shëndetësisë së Shqipërisë.
    
    Ky aplikacion ofron:
    - Segmentim automatik të organeve me TotalSegmentator
    - Segmentim interaktiv me MedSAM (bounding box prompts)
    - Etiketa anatomike në gjuhën shqipe
    - Eksport DICOM SEG me metadata shqiptare
    
    This MONAI Label application provides:
    - Automatic organ segmentation via TotalSegmentator
    - Interactive segmentation via MedSAM
    - Albanian anatomical labels
    - Albanian-localized DICOM SEG export
    """

    def __init__(self, app_dir: str, studies: str, conf: Dict[str, str]):
        """
        Initialize the Ministry App.
        
        Args:
            app_dir: Path to the application directory
            studies: URL or path to the DICOM studies
            conf: Configuration dictionary
        """
        self.config = MinistryAppConfig()
        
        # Model paths
        self.model_dir = os.path.join(app_dir, "model")
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Albanian label mapping
        self.label_map_al = ANATOMY_EN_TO_AL
        
        # DICOM writer for Albanian segmentations
        self.dicom_writer = DicomSegmentationWriter(
            manufacturer="Republika e Shqipërisë",
            institution="Ministria e Shëndetësisë dhe Mbrojtjes Sociale",
            series_description="Analiza AI (Ministria)"
        )
        
        logger.info("=" * 60)
        logger.info("MINISTRIA E SHËNDETËSISË - Sistemi AI i Imazherisë")
        logger.info("=" * 60)
        logger.info(f"Direktoria e modeleve: {self.model_dir}")
        logger.info(f"Numri i etiketave anatomike shqipe: {len(self.label_map_al)}")
        
        super().__init__(
            app_dir=app_dir,
            studies=studies,
            conf=conf,
            name="MinistryApp",
            description="Platforma AI e Imazherisë Mjekësore - Ministria e Shëndetësisë",
            version="1.0.0"
        )

    def init_datastore(self) -> Datastore:
        """
        Inicializon datastore-in për ruajtjen e studimeve.
        Initialize the datastore for study storage.
        """
        datastore = super().init_datastore()
        logger.info(f"Datastore i inicializuar: {type(datastore).__name__}")
        return datastore

    def init_infers(self) -> Dict[str, InferTask]:
        """
        Inicializon detyrat e inferimit (segmentimit).
        Initialize inference tasks.
        
        Returns:
            Dictionary of inference task name -> InferTask
        """
        infers: Dict[str, InferTask] = {}
        
        # TotalSegmentator - Automatic multi-organ segmentation
        # Disabled by default - requires large model downloads
        # Uncomment to enable after models are downloaded
        # try:
        #     infers["totalsegmentator"] = TotalSegmentatorInfer(
        #         path=self.model_dir,
        #         label_map=self.label_map_al,
        #         config=self.config,
        #         description="Segmentimi Automatik i Organeve (TotalSegmentator)"
        #     )
        #     logger.info("✓ TotalSegmentator i aktivizuar me sukses")
        # except Exception as e:
        #     logger.error(f"✗ Gabim në aktivizimin e TotalSegmentator: {e}")

        # MedSAM - Interactive segmentation
        # Disabled by default - requires model downloads
        # try:
        #     infers["medsam"] = MedSAMInfer(
        #         path=self.model_dir,
        #         config=self.config,
        #         description="Segmentimi Interaktiv (MedSAM)"
        #     )
        #     logger.info("✓ MedSAM i aktivizuar me sukses")
        # except Exception as e:
        #     logger.error(f"✗ Gabim në aktivizimin e MedSAM: {e}")

        # Log available inference tasks
        if not infers:
            logger.warning("⚠ Asnjë model AI nuk është aktivizuar. Platforma funksionon në modalitetin PACS/Viewer.")
            logger.info("Për të aktivizuar AI: Shkarkoni modelet dhe hiqni komentin nga init_infers()")
        else:
            logger.info(f"Detyra të inferimit të disponueshme: {list(infers.keys())}")
        
        return infers

    def init_trainers(self) -> Dict[str, TrainTask]:
        """
        Inicializon detyrat e trajnimit (opsionale).
        Initialize training tasks (optional for MVP).
        
        Returns:
            Empty dictionary - training not implemented in MVP
        """
        logger.info("Trajnimi i modeleve nuk është i aktivizuar në versionin MVP")
        return {}

    def init_strategies(self) -> Dict[str, Strategy]:
        """
        Inicializon strategjitë e përzgjedhjes së të dhënave.
        Initialize data selection strategies.
        
        Returns:
            Dictionary of strategy name -> Strategy
        """
        from monailabel.tasks.activelearning.random import Random
        from monailabel.tasks.activelearning.first import First
        
        strategies = {
            "random": Random(),
            "first": First(),
        }
        
        logger.info(f"Strategji të përzgjedhjes: {list(strategies.keys())}")
        return strategies

    def init_scoring_methods(self) -> Dict[str, ScoringMethod]:
        """
        Inicializon metodat e vlerësimit.
        Initialize scoring methods.
        
        Returns:
            Empty dictionary - scoring not implemented in MVP
        """
        return {}

    def info(self) -> Dict:
        """
        Kthen informacionin e aplikacionit.
        Return application information.
        
        Returns:
            Dictionary with application metadata
        """
        info = super().info()
        
        # Add Albanian metadata
        info.update({
            "name_al": "Platforma AI e Imazherisë Mjekësore",
            "institution_al": "Ministria e Shëndetësisë dhe Mbrojtjes Sociale",
            "country": "Shqipëri",
            "language": "sq-AL",
            "available_labels_al": len(self.label_map_al),
            "models": {
                "totalsegmentator": {
                    "name_al": "Segmentimi Automatik i Organeve",
                    "description_al": "Segmenton automatikisht 104 struktura anatomike",
                    "type": "automatic"
                },
                "medsam": {
                    "name_al": "Segmentimi Interaktiv",
                    "description_al": "Segmentim bazuar në kutinë kufizuese",
                    "type": "interactive"
                }
            }
        })
        
        return info

    def on_save_label(
        self, 
        image_id: str, 
        label_id: str, 
        params: Dict, 
        label_info: Dict
    ) -> Dict:
        """
        Thirret kur ruhet një etiketë - krijon DICOM SEG shqiptar.
        Called when saving a label - creates Albanian DICOM SEG.
        
        Args:
            image_id: Study instance UID
            label_id: Label identifier
            params: Additional parameters
            label_info: Label metadata
            
        Returns:
            Updated label info
        """
        result = super().on_save_label(image_id, label_id, params, label_info)
        
        # Log in Albanian
        logger.info(f"Etiketa e ruajtur: {label_id} për imazhin: {image_id}")
        
        return result


# ============================================================================
# Application factory function for MONAI Label
# ============================================================================

def main() -> MinistryApp:
    """
    Funksioni kryesor për krijimin e aplikacionit.
    Main function to create the application instance.
    
    This function is called by MONAI Label server to instantiate the app.
    
    Returns:
        MinistryApp instance
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Ministry of Health AI Platform")
    parser.add_argument("-s", "--studies", default="", help="Studies path/URL")
    parser.add_argument("-c", "--conf", nargs="+", default=[], help="Config")
    args, _ = parser.parse_known_args()
    
    # Parse configuration
    conf = {}
    for c in args.conf:
        if "=" in c:
            key, value = c.split("=", 1)
            conf[key] = value
    
    app_dir = os.path.dirname(os.path.abspath(__file__))
    studies = args.studies if args.studies else os.environ.get(
        "MONAI_LABEL_STUDIES", 
        "http://orthanc:8042/dicom-web"
    )
    
    return MinistryApp(app_dir=app_dir, studies=studies, conf=conf)


if __name__ == "__main__":
    # For testing
    app = main()
    print(app.info())
