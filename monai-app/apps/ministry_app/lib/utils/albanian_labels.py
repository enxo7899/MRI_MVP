"""
============================================================================
MINISTRIA E SHËNDETËSISË DHE MBROJTJES SOCIALE
Platforma Kombëtare AI e Imazherisë Mjekësore

Albanian Anatomical Labels Dictionary
Fjalori i Etiketave Anatomike Shqipe

This module provides comprehensive English-to-Albanian mappings for
anatomical structures used in medical imaging segmentation.
============================================================================
"""

from typing import Dict, List, Tuple

# ============================================================================
# COMPREHENSIVE ENGLISH TO ALBANIAN ANATOMY MAPPING
# Hartëzimi i Plotë i Anatomisë nga Anglishtja në Shqip
# 
# Based on TotalSegmentator v2 labels (104+ structures)
# Bazuar në etiketat e TotalSegmentator v2 (104+ struktura)
# ============================================================================

ANATOMY_EN_TO_AL: Dict[str, str] = {
    # ========================================================================
    # CARDIOVASCULAR SYSTEM / SISTEMI KARDIOVASKULAR
    # ========================================================================
    "heart": "Zemra",
    "heart_myocardium": "Miokardi",
    "heart_atrium_left": "Atriumit i Majtë",
    "heart_atrium_right": "Atriumi i Djathtë",
    "heart_ventricle_left": "Ventrikuli i Majtë",
    "heart_ventricle_right": "Ventrikuli i Djathtë",
    "aorta": "Aorta",
    "aorta_ascending": "Aorta Ngjitëse",
    "aorta_descending": "Aorta Zbritëse",
    "aortic_arch": "Harku i Aortës",
    "pulmonary_artery": "Arteria Pulmonare",
    "pulmonary_vein": "Vena Pulmonare",
    "inferior_vena_cava": "Vena Kava Inferiore",
    "superior_vena_cava": "Vena Kava Superiore",
    "portal_vein_and_splenic_vein": "Vena Portale dhe Vena Splenitike",
    "iliac_artery_left": "Arteria Iliake e Majtë",
    "iliac_artery_right": "Arteria Iliake e Djathtë",
    "iliac_vena_left": "Vena Iliake e Majtë",
    "iliac_vena_right": "Vena Iliake e Djathtë",
    "carotid_artery_left": "Arteria Karotide e Majtë",
    "carotid_artery_right": "Arteria Karotide e Djathtë",
    "subclavian_artery_left": "Arteria Subklaviane e Majtë",
    "subclavian_artery_right": "Arteria Subklaviane e Djathtë",
    "brachiocephalic_trunk": "Trungu Brakiocefalik",
    "brachiocephalic_vein_left": "Vena Brakiocefalike e Majtë",
    "brachiocephalic_vein_right": "Vena Brakiocefalike e Djathtë",
    "atrial_appendage_left": "Apendiksi Atrial i Majtë",
    "coronary_artery_left": "Arteria Koronare e Majtë",
    "coronary_artery_right": "Arteria Koronare e Djathtë",

    # ========================================================================
    # RESPIRATORY SYSTEM / SISTEMI I FRYMËMARRJES
    # ========================================================================
    "lung_left": "Mushkëria e Majtë",
    "lung_right": "Mushkëria e Djathtë",
    "lung_upper_lobe_left": "Lobi i Sipërm i Mushkërisë së Majtë",
    "lung_lower_lobe_left": "Lobi i Poshtëm i Mushkërisë së Majtë",
    "lung_upper_lobe_right": "Lobi i Sipërm i Mushkërisë së Djathtë",
    "lung_middle_lobe_right": "Lobi i Mesëm i Mushkërisë së Djathtë",
    "lung_lower_lobe_right": "Lobi i Poshtëm i Mushkërisë së Djathtë",
    "trachea": "Trakea",
    "bronchus_left": "Bronku i Majtë",
    "bronchus_right": "Bronku i Djathtë",
    "pleural_effusion": "Efuzion Pleural",

    # ========================================================================
    # DIGESTIVE SYSTEM / SISTEMI TRETËS
    # ========================================================================
    "liver": "Mëlçia",
    "spleen": "Shpretka",
    "stomach": "Stomaku",
    "pancreas": "Pankreasi",
    "gallbladder": "Fshikëza e Tëmthit",
    "esophagus": "Ezofagu",
    "duodenum": "Duodeni",
    "small_bowel": "Zorra e Hollë",
    "colon": "Zorra e Trashë",
    "colon_ascending": "Zorra e Trashë Ngjitëse",
    "colon_descending": "Zorra e Trashë Zbritëse",
    "colon_transverse": "Zorra e Trashë Tërthore",
    "colon_sigmoid": "Zorra Sigmoidale",
    "rectum": "Rektumi",

    # ========================================================================
    # URINARY SYSTEM / SISTEMI URINAR
    # ========================================================================
    "kidney_left": "Veshka e Majtë",
    "kidney_right": "Veshka e Djathtë",
    "kidney_cyst_left": "Kista e Veshkës së Majtë",
    "kidney_cyst_right": "Kista e Veshkës së Djathtë",
    "urinary_bladder": "Fshikëza Urinare",
    "ureter_left": "Ureteri i Majtë",
    "ureter_right": "Ureteri i Djathtë",
    "adrenal_gland_left": "Gjëndra Mbiveshkore e Majtë",
    "adrenal_gland_right": "Gjëndra Mbiveshkore e Djathtë",

    # ========================================================================
    # SKELETAL SYSTEM / SISTEMI SKELETOR
    # ========================================================================
    "vertebrae_C1": "Vertebra C1 (Atlas)",
    "vertebrae_C2": "Vertebra C2 (Aksis)",
    "vertebrae_C3": "Vertebra C3",
    "vertebrae_C4": "Vertebra C4",
    "vertebrae_C5": "Vertebra C5",
    "vertebrae_C6": "Vertebra C6",
    "vertebrae_C7": "Vertebra C7",
    "vertebrae_T1": "Vertebra T1",
    "vertebrae_T2": "Vertebra T2",
    "vertebrae_T3": "Vertebra T3",
    "vertebrae_T4": "Vertebra T4",
    "vertebrae_T5": "Vertebra T5",
    "vertebrae_T6": "Vertebra T6",
    "vertebrae_T7": "Vertebra T7",
    "vertebrae_T8": "Vertebra T8",
    "vertebrae_T9": "Vertebra T9",
    "vertebrae_T10": "Vertebra T10",
    "vertebrae_T11": "Vertebra T11",
    "vertebrae_T12": "Vertebra T12",
    "vertebrae_L1": "Vertebra L1",
    "vertebrae_L2": "Vertebra L2",
    "vertebrae_L3": "Vertebra L3",
    "vertebrae_L4": "Vertebra L4",
    "vertebrae_L5": "Vertebra L5",
    "vertebrae_S1": "Vertebra S1 (Sakrumi)",
    "sacrum": "Sakrumi",
    "coccyx": "Koksiku",
    "rib_left_1": "Brinja e Majtë 1",
    "rib_left_2": "Brinja e Majtë 2",
    "rib_left_3": "Brinja e Majtë 3",
    "rib_left_4": "Brinja e Majtë 4",
    "rib_left_5": "Brinja e Majtë 5",
    "rib_left_6": "Brinja e Majtë 6",
    "rib_left_7": "Brinja e Majtë 7",
    "rib_left_8": "Brinja e Majtë 8",
    "rib_left_9": "Brinja e Majtë 9",
    "rib_left_10": "Brinja e Majtë 10",
    "rib_left_11": "Brinja e Majtë 11",
    "rib_left_12": "Brinja e Majtë 12",
    "rib_right_1": "Brinja e Djathtë 1",
    "rib_right_2": "Brinja e Djathtë 2",
    "rib_right_3": "Brinja e Djathtë 3",
    "rib_right_4": "Brinja e Djathtë 4",
    "rib_right_5": "Brinja e Djathtë 5",
    "rib_right_6": "Brinja e Djathtë 6",
    "rib_right_7": "Brinja e Djathtë 7",
    "rib_right_8": "Brinja e Djathtë 8",
    "rib_right_9": "Brinja e Djathtë 9",
    "rib_right_10": "Brinja e Djathtë 10",
    "rib_right_11": "Brinja e Djathtë 11",
    "rib_right_12": "Brinja e Djathtë 12",
    "sternum": "Sternumi",
    "clavicula_left": "Klavikula e Majtë",
    "clavicula_right": "Klavikula e Djathtë",
    "scapula_left": "Skapula e Majtë",
    "scapula_right": "Skapula e Djathtë",
    "humerus_left": "Humerusi i Majtë",
    "humerus_right": "Humerusi i Djathtë",
    "hip_left": "Kofsha e Majtë",
    "hip_right": "Kofsha e Djathtë",
    "femur_left": "Femuri i Majtë",
    "femur_right": "Femuri i Djathtë",
    "gluteus_maximus_left": "Muskuli Gluteus Maximus i Majtë",
    "gluteus_maximus_right": "Muskuli Gluteus Maximus i Djathtë",
    "gluteus_medius_left": "Muskuli Gluteus Medius i Majtë",
    "gluteus_medius_right": "Muskuli Gluteus Medius i Djathtë",
    "gluteus_minimus_left": "Muskuli Gluteus Minimus i Majtë",
    "gluteus_minimus_right": "Muskuli Gluteus Minimus i Djathtë",
    "iliopsoas_left": "Muskuli Iliopsoas i Majtë",
    "iliopsoas_right": "Muskuli Iliopsoas i Djathtë",

    # ========================================================================
    # NERVOUS SYSTEM / SISTEMI NERVOR
    # ========================================================================
    "brain": "Truri",
    "brainstem": "Trungu i Trurit",
    "cerebellum": "Cerebeli (Truri i Vogël)",
    "spinal_cord": "Palca Kurrizore",
    
    # ========================================================================
    # HEAD AND NECK / KOKA DHE QAFA
    # ========================================================================
    "skull": "Kafka",
    "mandible": "Nofulla e Poshtme",
    "thyroid_gland": "Gjëndra Tiroide",
    "eye_left": "Syri i Majtë",
    "eye_right": "Syri i Djathtë",
    "optic_nerve_left": "Nervi Optik i Majtë",
    "optic_nerve_right": "Nervi Optik i Djathtë",
    "parotid_gland_left": "Gjëndra Parotide e Majtë",
    "parotid_gland_right": "Gjëndra Parotide e Djathtë",
    "submandibular_gland_left": "Gjëndra Submandibulare e Majtë",
    "submandibular_gland_right": "Gjëndra Submandibulare e Djathtë",
    "larynx": "Laringja",
    "pharynx": "Faringja",

    # ========================================================================
    # MUSCLES / MUSKUJT
    # ========================================================================
    "autochthon_left": "Muskujt Autoktonë të Majtë",
    "autochthon_right": "Muskujt Autoktonë të Djathtë",
    "erector_spinae_left": "Muskuli Erector Spinae i Majtë",
    "erector_spinae_right": "Muskuli Erector Spinae i Djathtë",

    # ========================================================================
    # OTHER STRUCTURES / STRUKTURA TË TJERA
    # ========================================================================
    "skin": "Lëkura",
    "fat": "Indi Dhjamor",
    "subcutaneous_fat": "Indi Dhjamor Nënlëkuror",
    "visceral_fat": "Indi Dhjamor Visceral",
    "mediastinum": "Mediastini",
    "pericardium": "Perikardi",
    "diaphragm": "Diafragma",
    "prostate": "Prostata",
    "uterus": "Mitra",
    "ovary_left": "Vezorja e Majtë",
    "ovary_right": "Vezorja e Djathtë",

    # ========================================================================
    # LYMPH NODES / NYJET LIMFATIKE
    # ========================================================================
    "lymph_node": "Nyja Limfatike",
    "lymph_nodes_cervical": "Nyjet Limfatike Cervikale",
    "lymph_nodes_axillary": "Nyjet Limfatike Aksilare",
    "lymph_nodes_mediastinal": "Nyjet Limfatike Mediastinale",
    "lymph_nodes_abdominal": "Nyjet Limfatike Abdominale",
    "lymph_nodes_pelvic": "Nyjet Limfatike Pelvike",

    # ========================================================================
    # PATHOLOGICAL STRUCTURES / STRUKTURA PATOLOGJIKE
    # ========================================================================
    "tumor": "Tumori",
    "lesion": "Lezion",
    "nodule": "Noduli",
    "mass": "Masa",
    "cyst": "Kista",
    "calcification": "Kalcifikimi",
    "hemorrhage": "Hemorragjia",
    "edema": "Edema",
    "necrosis": "Nekroza",
    "inflammation": "Inflamacioni",
    
    # ========================================================================
    # MEDSAM INTERACTIVE LABELS / ETIKETAT INTERAKTIVE MEDSAM
    # ========================================================================
    "selected_region": "Zonë e Përzgjedhur",
    "user_annotation": "Shënim i Përdoruesit",
    "roi": "Rajoni i Interesit",
}


# ============================================================================
# REVERSE MAPPING: Albanian to English
# ============================================================================
ANATOMY_AL_TO_EN: Dict[str, str] = {v: k for k, v in ANATOMY_EN_TO_AL.items()}


# ============================================================================
# SNOMED CT Codes for Major Organs (for DICOM SEG compliance)
# ============================================================================
SNOMED_CODES: Dict[str, Tuple[str, str]] = {
    # (SNOMED CT Code, Code Meaning)
    "liver": ("10200004", "Liver"),
    "spleen": ("78961009", "Spleen"),
    "kidney_left": ("64033007", "Left kidney"),
    "kidney_right": ("9846003", "Right kidney"),
    "lung_left": ("44029006", "Left lung"),
    "lung_right": ("3341006", "Right lung"),
    "heart": ("80891009", "Heart"),
    "pancreas": ("15776009", "Pancreas"),
    "stomach": ("69695003", "Stomach"),
    "gallbladder": ("28231008", "Gallbladder"),
    "aorta": ("15825003", "Aorta"),
    "brain": ("12738006", "Brain"),
    "urinary_bladder": ("89837001", "Urinary bladder"),
    "prostate": ("41216001", "Prostate"),
    "uterus": ("35039007", "Uterus"),
    "esophagus": ("32849002", "Esophagus"),
    "trachea": ("44567001", "Trachea"),
    "thyroid_gland": ("69748006", "Thyroid gland"),
    "adrenal_gland_left": ("61819007", "Left adrenal gland"),
    "adrenal_gland_right": ("68505006", "Right adrenal gland"),
}


# ============================================================================
# Label Groups for UI Organization
# ============================================================================
LABEL_GROUPS_AL: Dict[str, List[str]] = {
    "Sistemi Kardiovaskular": [
        "Zemra", "Aorta", "Vena Kava Inferiore", "Vena Kava Superiore",
        "Arteria Pulmonare", "Vena Portale dhe Vena Splenitike"
    ],
    "Sistemi i Frymëmarrjes": [
        "Mushkëria e Majtë", "Mushkëria e Djathtë", "Trakea",
        "Bronku i Majtë", "Bronku i Djathtë"
    ],
    "Sistemi Tretës": [
        "Mëlçia", "Shpretka", "Stomaku", "Pankreasi",
        "Fshikëza e Tëmthit", "Ezofagu", "Zorra e Hollë", "Zorra e Trashë"
    ],
    "Sistemi Urinar": [
        "Veshka e Majtë", "Veshka e Djathtë", "Fshikëza Urinare",
        "Gjëndra Mbiveshkore e Majtë", "Gjëndra Mbiveshkore e Djathtë"
    ],
    "Sistemi Nervor": [
        "Truri", "Trungu i Trurit", "Cerebeli (Truri i Vogël)", "Palca Kurrizore"
    ],
    "Sistemi Skeletor": [
        "Vertebra", "Brinja", "Sternumi", "Klavikula", "Skapula",
        "Humerusi", "Femuri", "Sakrumi", "Koksiku"
    ],
}


def get_albanian_label(english_label: str) -> str:
    """
    Merr etiketën shqiptare për një strukturë anatomike.
    Get Albanian label for an anatomical structure.
    
    Args:
        english_label: English anatomical term
        
    Returns:
        Albanian translation, or original if not found
    """
    # Normalize the label (lowercase, replace spaces with underscores)
    normalized = english_label.lower().replace(" ", "_").replace("-", "_")
    return ANATOMY_EN_TO_AL.get(normalized, english_label)


def get_english_label(albanian_label: str) -> str:
    """
    Merr etiketën angleze për një strukturë anatomike.
    Get English label for an anatomical structure.
    
    Args:
        albanian_label: Albanian anatomical term
        
    Returns:
        English translation, or original if not found
    """
    return ANATOMY_AL_TO_EN.get(albanian_label, albanian_label)


def get_snomed_code(english_label: str) -> Tuple[str, str]:
    """
    Merr kodin SNOMED CT për një strukturë anatomike.
    Get SNOMED CT code for an anatomical structure.
    
    Args:
        english_label: English anatomical term
        
    Returns:
        Tuple of (code, meaning), or default if not found
    """
    normalized = english_label.lower().replace(" ", "_").replace("-", "_")
    return SNOMED_CODES.get(normalized, ("123037004", "Body structure"))
