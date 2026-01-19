"""
Medical Report Parser
Extracts medical values from OCR text
NO AI REQUIRED - Pure pattern matching & regex
"""

import re
import os
import sys

# Try different import paths for flexibility
try:
    from utils.medical_knowledge import MedicalKnowledgeBase
except ImportError:
    try:
        from medical_knowledge import MedicalKnowledgeBase
    except ImportError:
        # Add current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.append(current_dir)
        sys.path.append(parent_dir)
        from medical_knowledge import MedicalKnowledgeBase

class MedicalReportParser:
    
    def __init__(self):
        self.kb = MedicalKnowledgeBase()
        
        # Common test name variations and abbreviations
        self.term_mappings = {
            # HbA1c variations
            "hba1c": "HbA1c",
            "hb a1c": "HbA1c",
            "glycated hemoglobin": "HbA1c",
            "glycosylated hemoglobin": "HbA1c",
            
            # Hemoglobin variations
            "hemoglobin": "Hemoglobin",
            "hb": "Hemoglobin",
            "haemoglobin": "Hemoglobin",
            
            # Cholesterol variations
            "total cholesterol": "Total Cholesterol",
            "cholesterol total": "Total Cholesterol",
            "chol": "Total Cholesterol",
            "t cholesterol": "Total Cholesterol",
            
            # HDL variations
            "hdl cholesterol": "HDL",
            "hdl": "HDL",
            "hdl cholesterol - direct": "HDL",
            "high density lipoprotein": "HDL",
            
            # LDL variations
            "ldl cholesterol": "LDL",
            "ldl": "LDL",
            "ldl cholesterol - direct": "LDL",
            "low density lipoprotein": "LDL",
            
            # Triglycerides variations
            "triglycerides": "Triglycerides",
            "trig": "Triglycerides",
            "trigs": "Triglycerides",
            
            # Glucose variations
            "glucose": "Glucose",
            "blood glucose": "Glucose",
            "fasting blood glucose": "Glucose",
            "fbs": "Glucose",
            "blood sugar": "Glucose",
            
            # TSH variations
            "tsh": "TSH",
            "thyroid stimulating hormone": "TSH",
            "tsh ultrasensitive": "TSH",
            
            # T3/T4 variations
            "t3": "T3",
            "total triiodothyronine": "T3",
            "triiodothyronine": "T3",
            "t4": "T4",
            "total thyroxine": "T4",
            "thyroxine": "T4",
            
            # Liver enzymes
            "sgot": "AST",
            "ast": "AST",
            "aspartate aminotransferase": "AST",
            "sgpt": "ALT",
            "alt": "ALT",
            "alanine transaminase": "ALT",
            "alanine aminotransferase": "ALT",
            
            # Other common tests
            "creatinine": "Creatinine",
            "bun": "BUN",
            "uric acid": "Uric Acid",
            "troponin": "Troponin",
            "troponin i": "Troponin",
            "bilirubin": "Bilirubin",
            "calcium": "Calcium",
            "sodium": "Sodium",
            "potassium": "Potassium",
            "vitamin d": "Vitamin D",
            "vitamin b12": "Vitamin B12",
            "iron": "Iron",
            
            # CBC
            "wbc": "WBC",
            "white blood cell": "WBC",
            "rbc": "RBC",
            "red blood cell": "RBC",
            "platelets": "Platelets",
            "platelet count": "Platelets",
            "hematocrit": "Hematocrit",
            "hct": "Hematocrit",
        }
    
    def normalize_term(self, term):
        """Convert various term formats to standard name"""
        term_lower = term.lower().strip()
        return self.term_mappings.get(term_lower, term)
    
    def extract_test_results(self, ocr_text):
        """
        Extract test name-value pairs from OCR text
        Returns: list of dicts with {term, value, unit, status}
        """
        results = []
        
        # Split text into lines
        lines = ocr_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Pattern 1: "TEST NAME VALUE UNIT" format
            # Example: "HbA1c 5.9 %"
            # Example: "TOTAL CHOLESTEROL 195 mg/dL"
            pattern1 = r'([A-Za-z\s\-/]+?)\s+(\d+\.?\d*)\s*([a-zA-Z/%]+)'
            match1 = re.search(pattern1, line)
            
            if match1:
                term_raw = match1.group(1).strip()
                value = float(match1.group(2))
                unit = match1.group(3).strip()
                
                # Normalize the term
                term = self.normalize_term(term_raw)
                
                # Check if this is a known medical term
                if self.kb.get_term_info(term):
                    results.append({
                        'term': term,
                        'raw_term': term_raw,
                        'value': value,
                        'unit': unit,
                        'line_number': i
                    })
                    continue
            
            # Pattern 2: Test name on one line, value on next line
            # Common in structured reports
            if i < len(lines) - 1:
                next_line = lines[i + 1].strip()
                
                # Check if current line looks like a test name
                if any(keyword in line.lower() for keyword in ['cholesterol', 'glucose', 'hemoglobin', 'thyroid']):
                    # Check if next line has a number
                    pattern2 = r'(\d+\.?\d*)\s*([a-zA-Z/%]+)?'
                    match2 = re.search(pattern2, next_line)
                    
                    if match2:
                        term = self.normalize_term(line)
                        value = float(match2.group(1))
                        unit = match2.group(2).strip() if match2.group(2) else ""
                        
                        if self.kb.get_term_info(term):
                            results.append({
                                'term': term,
                                'raw_term': line,
                                'value': value,
                                'unit': unit,
                                'line_number': i
                            })
        
        # Remove duplicates (keep first occurrence)
        seen_terms = set()
        unique_results = []
        for result in results:
            if result['term'] not in seen_terms:
                unique_results.append(result)
                seen_terms.add(result['term'])
        
        return unique_results
    
    def parse_report(self, ocr_text, gender="female", age=50):
        """
        Main parsing function
        Returns complete analysis with interpretations
        """
        # Extract raw test results
        test_results = self.extract_test_results(ocr_text)
        
        # Analyze each result
        analyzed_results = []
        
        for result in test_results:
            term = result['term']
            value = result['value']
            
            # Get interpretation from knowledge base
            interpretation = self.kb.get_interpretation(term, value, gender)
            
            # Combine extraction result with interpretation
            analyzed_results.append({
                **result,
                'interpretation': interpretation
            })
        
        # Categorize results
        categorized = {
            'normal': [],
            'high': [],
            'low': [],
            'critical': []
        }
        
        for result in analyzed_results:
            status = result['interpretation']['status']
            severity = result['interpretation'].get('severity', '')
            
            if status == 'normal':
                categorized['normal'].append(result)
            elif status == 'high':
                if 'high' in severity.lower() or 'emergency' in severity.lower():
                    categorized['critical'].append(result)
                else:
                    categorized['high'].append(result)
            elif status == 'low':
                if 'high' in severity.lower() or 'emergency' in severity.lower():
                    categorized['critical'].append(result)
                else:
                    categorized['low'].append(result)
        
        # Detect report type
        report_type = self.detect_report_type(test_results)
        
        return {
            'report_type': report_type,
            'total_tests': len(test_results),
            'all_results': analyzed_results,
            'categorized': categorized,
            'patient_info': {
                'gender': gender,
                'age': age
            }
        }
    
    def detect_report_type(self, test_results):
        """Detect what type of medical report this is"""
        test_names = [r['term'] for r in test_results]
        
        # Check for common report type patterns
        if any(t in test_names for t in ['Total Cholesterol', 'HDL', 'LDL', 'Triglycerides']):
            return "Lipid Profile"
        
        if any(t in test_names for t in ['Hemoglobin', 'WBC', 'RBC', 'Platelets']):
            return "Complete Blood Count (CBC)"
        
        if any(t in test_names for t in ['TSH', 'T3', 'T4']):
            return "Thyroid Function Test"
        
        if any(t in test_names for t in ['AST', 'ALT', 'Bilirubin']):
            return "Liver Function Test"
        
        if any(t in test_names for t in ['Creatinine', 'BUN']):
            return "Kidney Function Test"
        
        if 'Glucose' in test_names or 'HbA1c' in test_names:
            return "Diabetes Screening"
        
        return "General Health Panel"


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    # Test with sample OCR text from your actual report
    sample_text = """
    HbA1c - (HPLC)
    H.P.L.C 5.9 %
    
    TOTAL CHOLESTEROL 195 mg/dL
    HDL CHOLESTEROL - DIRECT 46 mg/dL
    LDL CHOLESTEROL - DIRECT 118 mg/dL
    TRIGLYCERIDES 210 mg/dL
    
    TROPONIN I HEART ATTACK RISK 1.4 pg/mL
    """
    
    parser = MedicalReportParser()
    
    print("=" * 60)
    print("TESTING REPORT PARSER")
    print("=" * 60)
    
    # Parse the report
    analysis = parser.parse_report(sample_text, gender="female", age=50)
    
    print(f"\nReport Type: {analysis['report_type']}")
    print(f"Total Tests Found: {analysis['total_tests']}")
    
    print("\n" + "=" * 60)
    print("ABNORMAL RESULTS:")
    print("=" * 60)
    
    for result in analysis['categorized']['high']:
        print(f"\n{result['term']}: {result['value']} {result['unit']}")
        print(f"   Status: {result['interpretation']['status'].upper()}")
        print(f"   Normal Range: {result['interpretation']['normal_range']}")
        print(f"   Condition: {result['interpretation'].get('condition', 'N/A')}")
    
    for result in analysis['categorized']['low']:
        print(f"\n{result['term']}: {result['value']} {result['unit']}")
        print(f"   Status: {result['interpretation']['status'].upper()}")
        print(f"   Normal Range: {result['interpretation']['normal_range']}")
        print(f"   Condition: {result['interpretation'].get('condition', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("NORMAL RESULTS:")
    print("=" * 60)
    
    for result in analysis['categorized']['normal']:
        print(f"{result['term']}: {result['value']} {result['unit']}")