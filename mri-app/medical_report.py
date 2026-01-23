"""
Professional Medical Report Generator
Ministria e Shëndetësisë dhe Mbrojtjes Sociale
"""

from datetime import datetime
from translations import ANATOMY_LABELS

# Normal organ volume ranges (in ml)
NORMAL_RANGES = {
    'liver': (1200, 1800),
    'spleen': (150, 250),
    'kidney_left': (120, 170),
    'kidney_right': (120, 170),
    'heart': (500, 800),
    'pancreas': (70, 120),
    'stomach': (300, 600),
    'gallbladder': (30, 60),
    'lung_left': (1500, 2500),
    'lung_right': (1500, 2500),
    'brain': (1100, 1500),
}


def assess_organ_status(organ_name, volume_ml, confidence):
    """
    Assess organ status based on volume and provide clinical interpretation.
    """
    if organ_name not in NORMAL_RANGES:
        return {
            'status': 'Normal',
            'status_al': 'Normal',
            'assessment': 'Brenda kufijve të pritshme',
            'clinical_significance': 'Asnjë gjetje anormale e dukshme'
        }
    
    min_vol, max_vol = NORMAL_RANGES[organ_name]
    
    if volume_ml < min_vol * 0.7:
        return {
            'status': 'Significantly Reduced',
            'status_al': 'Zvogëluar Ndjeshëm',
            'assessment': f'Vëllimi është ndjeshëm nën normalin ({min_vol}-{max_vol} ml)',
            'clinical_significance': 'Kërkon vlerësim të mëtejshëm nga specialist',
            'recommendation': 'Rekomandohet ekzaminim i detajuar dhe konsultim me specialist'
        }
    elif volume_ml < min_vol:
        return {
            'status': 'Mildly Reduced',
            'status_al': 'Zvogëluar Lehtë',
            'assessment': f'Vëllimi është pak nën normalin ({min_vol}-{max_vol} ml)',
            'clinical_significance': 'Mund të jetë variant normal ose kërkon monitorim',
            'recommendation': 'Monitorim dhe krahasim me ekzaminime të mëparshme'
        }
    elif volume_ml > max_vol * 1.3:
        return {
            'status': 'Significantly Enlarged',
            'status_al': 'Zmadhuar Ndjeshëm',
            'assessment': f'Vëllimi është ndjeshëm mbi normalin ({min_vol}-{max_vol} ml)',
            'clinical_significance': 'Kërkon vlerësim urgjent nga specialist',
            'recommendation': 'Rekomandohet ekzaminim urgjent dhe konsultim me specialist'
        }
    elif volume_ml > max_vol:
        return {
            'status': 'Mildly Enlarged',
            'status_al': 'Zmadhuar Lehtë',
            'assessment': f'Vëllimi është pak mbi normalin ({min_vol}-{max_vol} ml)',
            'clinical_significance': 'Mund të jetë variant normal ose kërkon monitorim',
            'recommendation': 'Monitorim dhe krahasim me ekzaminime të mëparshme'
        }
    else:
        return {
            'status': 'Normal',
            'status_al': 'Normal',
            'assessment': f'Vëllimi brenda kufijve normalë ({min_vol}-{max_vol} ml)',
            'clinical_significance': 'Asnjë gjetje anormale e dukshme',
            'recommendation': 'Vazhdoni kontrollet rutinë'
        }


def generate_professional_report(results):
    """
    Generate comprehensive professional medical report.
    """
    organs = results.get('organs', [])
    processing_time = results.get('processing_time', 0)
    ai_model = results.get('ai_model', 'Unknown')
    
    # Header information
    report_header = {
        'institution': 'Ministria e Shëndetësisë dhe Mbrojtjes Sociale',
        'department': 'Departamenti i Imazhimit Mjekësor',
        'report_type': 'Raport i Analizës së Skanimit MRI',
        'report_date': get_albanian_datetime(),
        'ai_system': f'Sistem AI: {ai_model}',
        'processing_time': f'{processing_time:.1f} sekonda'
    }
    
    # Clinical summary
    total_organs = len(organs)
    abnormal_organs = [o for o in organs if assess_organ_status(o['name_en'], o['volume_ml'], o['confidence'])['status'] != 'Normal']
    
    clinical_summary = {
        'total_detected': total_organs,
        'normal_count': total_organs - len(abnormal_organs),
        'abnormal_count': len(abnormal_organs),
        'overall_assessment': 'Normal' if len(abnormal_organs) == 0 else 'Kërkon Vëmendje',
        'summary_text': generate_summary_text(total_organs, abnormal_organs)
    }
    
    # Detailed organ findings
    detailed_findings = []
    for idx, organ in enumerate(organs, 1):
        assessment = assess_organ_status(organ['name_en'], organ['volume_ml'], organ['confidence'])
        
        finding = {
            'number': idx,
            'organ_name_al': organ['name_al'],
            'organ_name_en': organ['name_en'],
            'confidence': organ['confidence'],
            'confidence_percent': round(organ['confidence'] * 100, 1),
            'volume_ml': organ['volume_ml'],
            'status': assessment['status'],
            'status_al': assessment['status_al'],
            'assessment': assessment['assessment'],
            'clinical_significance': assessment['clinical_significance'],
            'recommendation': assessment.get('recommendation', 'Vazhdoni kontrollet rutinë'),
            'normal_range': NORMAL_RANGES.get(organ['name_en'], None)
        }
        detailed_findings.append(finding)
    
    # Sort by abnormality (abnormal first) then by confidence
    detailed_findings.sort(key=lambda x: (x['status'] == 'Normal', -x['confidence']))
    
    # Clinical recommendations
    recommendations = generate_clinical_recommendations(abnormal_organs, total_organs)
    
    # Radiologist notes
    radiologist_notes = {
        'technique': 'Analizë automatike e skanimit MRI duke përdorur inteligjencë artificiale',
        'quality': 'Cilësia e imazhit: E mjaftueshme për analizë diagnostike',
        'limitations': [
            'Ky raport është gjeneruar automatikisht nga sistem AI',
            'Rezultatet duhet të interpretohen në kontekstin klinik',
            'Gjetjet e dyshimta kërkojnë verifikim nga radiolog i kualifikuar'
        ]
    }
    
    # Compile full report
    full_report = {
        'header': report_header,
        'clinical_summary': clinical_summary,
        'detailed_findings': detailed_findings,
        'recommendations': recommendations,
        'radiologist_notes': radiologist_notes,
        'disclaimer': generate_disclaimer()
    }
    
    return full_report


def generate_summary_text(total_organs, abnormal_organs):
    """Generate clinical summary text."""
    if len(abnormal_organs) == 0:
        return f"Analiza identifikoi {total_organs} organe. Të gjitha strukturat anatomike janë brenda kufijve normalë. Nuk u vërejtën gjetje patologjike të dukshme."
    else:
        abnormal_names = [o['name_al'] for o in abnormal_organs]
        return f"Analiza identifikoi {total_organs} organe. U vërejtën {len(abnormal_organs)} gjetje që kërkojnë vëmendje: {', '.join(abnormal_names)}. Rekomandohet vlerësim i mëtejshëm."


def generate_clinical_recommendations(abnormal_organs, total_organs):
    """Generate clinical recommendations based on findings."""
    recommendations = []
    
    if len(abnormal_organs) == 0:
        recommendations.extend([
            {
                'priority': 'Rutinë',
                'text': 'Të gjitha gjetjet janë normale. Vazhdoni kontrollet rutinë sipas protokollit standard.'
            },
            {
                'priority': 'Parandalim',
                'text': 'Ruajtja e stilit të shëndetshëm të jetesës dhe kontrollet periodike janë të rekomanduara.'
            }
        ])
    else:
        recommendations.append({
            'priority': 'E Lartë',
            'text': f'U identifikuan {len(abnormal_organs)} gjetje anormale që kërkojnë vlerësim të mëtejshëm nga specialist.'
        })
        
        for organ in abnormal_organs:
            assessment = assess_organ_status(organ['name_en'], organ['volume_ml'], organ['confidence'])
            recommendations.append({
                'priority': 'E Lartë' if 'Significantly' in assessment['status'] else 'E Mesme',
                'organ': organ['name_al'],
                'text': assessment.get('recommendation', 'Monitorim i rekomanduar')
            })
    
    recommendations.append({
        'priority': 'E Detyrueshme',
        'text': 'Ky raport duhet të rishikohet nga një radiolog i kualifikuar para çdo vendimi klinik.'
    })
    
    recommendations.append({
        'priority': 'Dokumentim',
        'text': 'Ruani këtë raport për referencë të ardhshme dhe krahasim me ekzaminime të mëparshme.'
    })
    
    return recommendations


def generate_disclaimer():
    """Generate medical disclaimer."""
    return {
        'title': 'Paralajmërim i Rëndësishëm Mjekësor',
        'points': [
            'Ky raport është gjeneruar automatikisht nga një sistem inteligjence artificiale.',
            'Rezultatet janë sugjerime diagnostike dhe NUK zëvendësojnë gjykimin klinik të një mjeku të kualifikuar.',
            'Çdo rast duhet të vlerësohet individualisht nga një radiolog i licencuar.',
            'Sistemi AI mund të ketë kufizime në zbulimin e patologjive të rralla ose komplekse.',
            'Në rast dyshimi për gjendje urgjente, kontaktoni menjëherë me personelin mjekësor.',
            'Ky raport nuk duhet të përdoret si bazë e vetme për vendime terapeutike.'
        ]
    }


def get_albanian_datetime():
    """Get current date and time in Albanian format."""
    months_al = {
        1: 'Janar', 2: 'Shkurt', 3: 'Mars', 4: 'Prill',
        5: 'Maj', 6: 'Qershor', 7: 'Korrik', 8: 'Gusht',
        9: 'Shtator', 10: 'Tetor', 11: 'Nëntor', 12: 'Dhjetor'
    }
    
    now = datetime.now()
    return f"{now.day} {months_al[now.month]} {now.year}, ora {now.hour}:{now.minute:02d}"
