import spacy
import re

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    print("spaCy model loaded successfully!")
except:
    print("spaCy model not found.")
    nlp = None

# Comprehensive medical terms dictionary
MEDICAL_TERMS = {
    # Thyroid
    't3': 'T3 (thyroid hormone that controls metabolism)',
    't4': 'T4 (main thyroid hormone)',
    'tsh': 'TSH (brain signal to thyroid gland)',
    'thyroid': 'thyroid (gland that controls body energy)',
    'ft3': 'Free T3 (active thyroid hormone)',
    'ft4': 'Free T4 (active thyroid hormone)',
    
    # Liver
    'sgot': 'SGOT (liver enzyme, also called AST)',
    'sgpt': 'SGPT (liver enzyme, also called ALT)',
    'alt': 'ALT (liver health indicator)',
    'ast': 'AST (liver health indicator)',
    'bilirubin': 'bilirubin (yellow pigment from liver)',
    'alkaline phosphatase': 'alkaline phosphatase (liver/bone enzyme)',
    'albumin': 'albumin (protein made by liver)',
    'total protein': 'total protein (overall protein in blood)',
    
    # Kidney
    'creatinine': 'creatinine (kidney waste product)',
    'urea': 'urea (kidney waste product)',
    'bun': 'BUN (blood urea nitrogen, kidney function test)',
    'uric acid': 'uric acid (waste product filtered by kidneys)',
    
    # Blood / Hematology
    'hemoglobin': 'hemoglobin (oxygen carrier in blood)',
    'hb': 'hemoglobin (oxygen carrier in blood)',
    'wbc': 'white blood cells (infection fighters)',
    'rbc': 'red blood cells (oxygen carriers)',
    'platelets': 'platelets (help blood clot)',
    'hematocrit': 'hematocrit (proportion of red blood cells)',
    'mcv': 'MCV (mean corpuscular volume of red cells)',
    'mch': 'MCH (average hemoglobin per red cell)',
    'mchc': 'MCHC (concentration of hemoglobin in red cells)',
    
    # Blood sugar / Metabolism
    'glucose': 'blood sugar',
    'hba1c': 'HbA1c (average blood sugar over 3 months)',
    'fasting glucose': 'fasting blood sugar',
    'postprandial glucose': 'blood sugar after meal',
    
    # Lipid profile
    'cholesterol': 'cholesterol (fat in blood)',
    'hdl': 'HDL (good cholesterol)',
    'ldl': 'LDL (bad cholesterol)',
    'triglycerides': 'triglycerides (blood fat)',
    'vldl': 'VLDL (very low-density lipoprotein)',
    
    # Heart / Cardiac markers
    'troponin': 'troponin (heart muscle injury marker)',
    'ckmb': 'CK-MB (heart enzyme)',
    'ldh': 'LDH (lactate dehydrogenase, tissue damage marker)',
    'ecg': 'ECG (electrocardiogram, heart activity)',
    
    # General / Conditions
    'hypertension': 'high blood pressure',
    'diabetes': 'diabetes (high blood sugar condition)',
    'edema': 'swelling',
    'dyspnea': 'difficulty breathing',
    'fever': 'elevated body temperature',
    'infection': 'infection (caused by bacteria, virus, or fungus)',
    'anemia': 'anemia (low red blood cell count)',
    'dehydration': 'dehydration (low body fluids)',
    
    # Vitamins / Minerals
    'vitamin d': 'Vitamin D (bone and immune health)',
    'vitamin b12': 'Vitamin B12 (nerve and blood cell health)',
    'calcium': 'Calcium (bone and muscle health)',
    'iron': 'Iron (for hemoglobin synthesis)',
    'magnesium': 'Magnesium (muscle and nerve function)',
    
    # Electrolytes
    'sodium': 'Sodium (electrolyte balance)',
    'potassium': 'Potassium (electrolyte for heart/muscles)',
    'chloride': 'Chloride (electrolyte balance)',
    'bicarbonate': 'Bicarbonate (blood pH balance)',
    
    # Other lab tests
    'crp': 'C-reactive protein (inflammation marker)',
    'esr': 'ESR (erythrocyte sedimentation rate, inflammation)',
    'd dimer': 'D-dimer (blood clot marker)',
    'ldl/hdl ratio': 'LDL/HDL ratio (cardiovascular risk indicator)',
}


def extract_test_results(text):
    """
    Extract test names and their values from medical report
    """
    results = []
    lines = text.split('\n')
    
    # Pattern to match test results: TEST_NAME : VALUE UNIT RANGE
    patterns = [
        r'([A-Z][A-Za-z0-9\s\-]+)\s*[:=]\s*([0-9.]+)\s*([a-zA-Z/%]+)?',
        r'([A-Z][A-Za-z0-9\s]+)\s+([0-9.]+)\s*([a-zA-Z/%]+)?',
    ]
    
    for line in lines:
        for pattern in patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                test_name = match[0].strip()
                value = match[1].strip()
                unit = match[2].strip() if len(match) > 2 else ''
                
                if len(test_name) > 2 and len(value) > 0:
                    results.append({
                        'test': test_name,
                        'value': value,
                        'unit': unit
                    })
    
    return results

def generate_plain_summary(text):
    """
    Generate a patient-friendly summary in simple language
    """
    # Extract test results
    test_results = extract_test_results(text)
    
    # Identify patient info
    patient_name = re.search(r'Patient Name\s*[:=]\s*([A-Z\s]+)', text, re.IGNORECASE)
    age_sex = re.search(r'\((\d+)Y?/([MF])\)', text, re.IGNORECASE)
    
    summary_parts = []
    
    # Patient info
    if patient_name:
        summary_parts.append(f"Patient: {patient_name.group(1).strip()}")
    
    if age_sex:
        age = age_sex.group(1)
        sex = "Male" if age_sex.group(2).upper() == 'M' else "Female"
        summary_parts.append(f"Age: {age} years, Gender: {sex}")
    
    # Tests done
    tests_done = re.search(r'Tests Done\s*[:=]\s*([^\n]+)', text, re.IGNORECASE)
    if tests_done:
        summary_parts.append(f"\nTests Performed: {tests_done.group(1).strip()}")
    
    # Simplified results
    if test_results:
        summary_parts.append("\n📊 Your Test Results (Simplified):")
        
        for i, result in enumerate(test_results[:10]):  # Limit to first 10
            test_name = result['test'].lower()
            value = result['value']
            unit = result['unit']
            
            # Simplify test name
            simplified_name = test_name
            for term, explanation in MEDICAL_TERMS.items():
                if term in test_name.lower():
                    simplified_name = explanation
                    break
            
            summary_parts.append(f"  • {simplified_name}: {value} {unit}")
    
    # General advice
    summary_parts.append("\n💡 What This Means:")
    summary_parts.append("These are your lab test results. Each value shows how different parts of your body are functioning.")
    summary_parts.append("\n⚠️ Important: Always discuss these results with your doctor. They can explain what's normal for you and if any action is needed.")
    
    return "\n".join(summary_parts)

def create_plain_language_summary(text):
    """
    Main function to create patient-friendly summary
    """
    if not text or len(text.strip()) < 50:
        return "Unable to generate summary. Not enough information extracted from the report."
    
    return generate_plain_summary(text)

def summarize_report(text):
    """
    Create a detailed summary with all analysis
    """
    if not text or len(text.strip()) < 10:
        return {"error": "No meaningful text extracted"}
    
    test_results = extract_test_results(text)
    plain_summary = create_plain_language_summary(text)
    
    summary = {
        'plain_language_summary': plain_summary,
        'test_results': test_results,
        'word_count': len(text.split()),
        'status': 'success'
    }
    
    return summary