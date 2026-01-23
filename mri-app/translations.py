"""
Albanian Translations for MRI Analysis
Ministria e Shëndetësisë dhe Mbrojtjes Sociale
"""

# Albanian Anatomy Labels
ANATOMY_LABELS = {
    # Major Organs
    'liver': 'Mëlçia',
    'spleen': 'Shpretka',
    'kidney_left': 'Veshka e Majtë',
    'kidney_right': 'Veshka e Djathtë',
    'heart': 'Zemra',
    'pancreas': 'Pankreasi',
    'stomach': 'Stomaku',
    'gallbladder': 'Fshikëza e Tëmthit',
    
    # Lungs
    'lung_left': 'Mushkëria e Majtë',
    'lung_right': 'Mushkëria e Djathtë',
    
    # Brain
    'brain': 'Truri',
    'cerebellum': 'Cerebeli',
    'brainstem': 'Trungu i Trurit',
    
    # Cardiovascular
    'aorta': 'Aorta',
    'pulmonary_artery': 'Arteria Pulmonare',
    'vena_cava': 'Vena Kava',
    
    # Digestive
    'esophagus': 'Ezofagu',
    'duodenum': 'Dymbëdhjetëgishti',
    'small_intestine': 'Zorra e Hollë',
    'colon': 'Zorra e Trashë',
    
    # Skeletal
    'vertebrae': 'Kurrizorja',
    'ribs': 'Brinjët',
    'sternum': 'Gjoksi',
    
    # Muscles
    'diaphragm': 'Diafragma',
    'psoas_left': 'Psoas i Majtë',
    'psoas_right': 'Psoas i Djathtë',
    
    # Urinary
    'bladder': 'Fshikëza',
    'ureter_left': 'Uretri i Majtë',
    'ureter_right': 'Uretri i Djathtë',
    
    # Reproductive
    'uterus': 'Mitra',
    'ovary_left': 'Vezorja e Majtë',
    'ovary_right': 'Vezorja e Djathtë',
    'prostate': 'Prostata',
    
    # Glands
    'adrenal_left': 'Mbiveshkja e Majtë',
    'adrenal_right': 'Mbiveshkja e Djathtë',
    'thyroid': 'Tiroida',
}


def generate_report(results):
    """
    Generate Albanian medical report from analysis results.
    
    Args:
        results: Dictionary with analysis results
    
    Returns:
        dict: Formatted Albanian report
    """
    organs = results.get('organs', [])
    organs_detected = results.get('organs_detected', 0)
    processing_time = results.get('processing_time', 0)
    
    # Generate summary
    summary = f"Analiza identifikoi {organs_detected} organe në skanimin MRI."
    
    # Generate detailed findings
    findings = []
    for organ in organs:
        finding = {
            'organ_al': organ['name_al'],
            'organ_en': organ['name_en'],
            'confidence': organ['confidence'],
            'confidence_percent': round(organ['confidence'] * 100, 1),
            'volume_ml': organ.get('volume_ml', 'N/A'),
            'status': organ.get('status', 'Normal'),
            'status_al': translate_status(organ.get('status', 'Normal'))
        }
        findings.append(finding)
    
    # Generate recommendations
    recommendations = generate_recommendations(organs)
    
    report = {
        'summary': summary,
        'findings': findings,
        'recommendations': recommendations,
        'processing_time': processing_time,
        'total_organs': organs_detected,
        'report_date': get_current_date_albanian(),
        'institution': 'Ministria e Shëndetësisë dhe Mbrojtjes Sociale',
        'disclaimer': 'Ky raport është gjeneruar automatikisht nga një sistem AI dhe duhet të rishikohet nga një radiolog i kualifikuar.'
    }
    
    return report


def translate_status(status):
    """Translate organ status to Albanian."""
    status_map = {
        'Normal': 'Normal',
        'Abnormal': 'Anormal',
        'Enlarged': 'I Zmadhuar',
        'Reduced': 'I Zvogëluar',
        'Not Detected': 'Nuk u Zbulua',
        'Unclear': 'I Paqartë'
    }
    return status_map.get(status, status)


def generate_recommendations(organs):
    """Generate medical recommendations based on findings."""
    recommendations = [
        'Rezultatet duhet të rishikohen nga një radiolog i kualifikuar.',
        'Nëse ka shenja të anormaliteteve, rekomandohet konsultim mjekësor.',
        'Ruani këtë raport për referencë të ardhshme.'
    ]
    
    # Add specific recommendations based on findings
    for organ in organs:
        if organ['confidence'] < 0.7:
            recommendations.append(f"Konfirmoni gjetjet për {organ['name_al']} me ekzaminime shtesë.")
        
        if organ.get('status') != 'Normal':
            recommendations.append(f"Vëmendje e veçantë për {organ['name_al']} - status: {organ['status']}.")
    
    return recommendations


def get_current_date_albanian():
    """Get current date formatted in Albanian."""
    from datetime import datetime
    
    months_al = {
        1: 'Janar', 2: 'Shkurt', 3: 'Mars', 4: 'Prill',
        5: 'Maj', 6: 'Qershor', 7: 'Korrik', 8: 'Gusht',
        9: 'Shtator', 10: 'Tetor', 11: 'Nëntor', 12: 'Dhjetor'
    }
    
    now = datetime.now()
    return f"{now.day} {months_al[now.month]} {now.year}"
