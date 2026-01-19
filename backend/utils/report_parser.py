"""
Medical Report Parser - ENHANCED VERSION
Extracts medical values from OCR text with better patterns
NO AI REQUIRED - Pure pattern matching & regex
"""

import re
import os
import sys

# Try different import paths for flexibility
try:
    from utils.medical_knowledge import MedicalKnowledgeBase
    print("✅ MedicalKnowledgeBase imported from utils.medical_knowledge")
except ImportError:
    try:
        from medical_knowledge import MedicalKnowledgeBase
        print("✅ MedicalKnowledgeBase imported from medical_knowledge")
    except ImportError:
        try:
            # Add current directory to Python path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            sys.path.append(current_dir)
            sys.path.append(parent_dir)
            from medical_knowledge import MedicalKnowledgeBase
            print("✅ MedicalKnowledgeBase imported with sys.path adjustment")
        except ImportError as e:
            print(f"❌ Failed to import MedicalKnowledgeBase: {e}")
            # Create a dummy class to prevent crashes
            class MedicalKnowledgeBase:
                @staticmethod
                def get_term_info(term):
                    return None
                @staticmethod
                def get_interpretation(term, value, gender="all"):
                    return {"error": "Knowledge base not available"}
                @staticmethod
                def get_normal_range(term_name, gender="all", age_group="adult"):
                    return None
            print("⚠️ Using dummy MedicalKnowledgeBase")

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
        ENHANCED VERSION - catches more patterns
        """
        results = []
        
        # Clean up text
        text = ocr_text.replace('\n', ' ')
        text = ' '.join(text.split())  # Normalize whitespace
        
        # All known test patterns
        test_patterns = {
            # HbA1c patterns
            r'HbA1c[:\s-]*(\d+\.?\d*)\s*%': 'HbA1c',
            r'Hb\s*A1c[:\s-]*(\d+\.?\d*)\s*%': 'HbA1c',
            r'GLYCATED HEMOGLOBIN[:\s-]*(\d+\.?\d*)\s*%': 'HbA1c',
            
            # Cholesterol patterns
            r'TOTAL\s*CHOLESTEROL[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Total Cholesterol',
            r'CHOLESTEROL\s*TOTAL[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Total Cholesterol',
            r'CHOLESTEROL[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Total Cholesterol',
            
            # HDL patterns
            r'HDL\s*CHOLESTEROL[:\s-]*(\d+\.?\d*)\s*mg/dL': 'HDL',
            r'HDL[:\s-]*(\d+\.?\d*)\s*mg/dL': 'HDL',
            
            # LDL patterns  
            r'LDL\s*CHOLESTEROL[:\s-]*(\d+\.?\d*)\s*mg/dL': 'LDL',
            r'LDL[:\s-]*(\d+\.?\d*)\s*mg/dL': 'LDL',
            
            # Triglycerides patterns
            r'TRIGLYCERIDES[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Triglycerides',
            r'TRIG[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Triglycerides',
            
            # Glucose patterns
            r'GLUCOSE[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Glucose',
            r'BLOOD\s*SUGAR[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Glucose',
            
            # Hemoglobin patterns
            r'HEMOGLOBIN[:\s-]*(\d+\.?\d*)\s*g/dL': 'Hemoglobin',
            r'HB[:\s-]*(\d+\.?\d*)\s*g/dL': 'Hemoglobin',
            
            # Other common tests
            r'TSH[:\s-]*(\d+\.?\d*)\s*mIU/L': 'TSH',
            r'CREATININE[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Creatinine',
            r'URIC\s*ACID[:\s-]*(\d+\.?\d*)\s*mg/dL': 'Uric Acid',
        }
        
        # Try each pattern
        found_terms = set()
        for pattern, term_name in test_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if term_name not in found_terms:
                    value = float(match.group(1))
                    
                    # Get unit from knowledge base
                    term_info = self.kb.get_term_info(term_name)
                    if term_info:
                        normal_range = self.kb.get_normal_range(term_name)
                        unit = normal_range.get('unit', '') if normal_range else ''
                        
                        results.append({
                            'term': term_name,
                            'raw_term': match.group(0),
                            'value': value,
                            'unit': unit,
                            'line_number': 0
                        })
                        found_terms.add(term_name)
        
        # Also try the original line-by-line method as fallback
        if not results:
            return self._extract_line_by_line(ocr_text)
        
        return results
    
    def _extract_line_by_line(self, ocr_text):
        """Original line-by-line extraction as fallback"""
        results = []
        lines = ocr_text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Pattern 1: "TEST NAME VALUE UNIT" format
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
            if i < len(lines) - 1:
                next_line = lines[i + 1].strip()
                
                # Check if current line looks like a test name
                if any(keyword in line.lower() for keyword in ['cholesterol', 'glucose', 'hemoglobin', 'thyroid', 'hba1c', 'hdl', 'ldl', 'triglycerides']):
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
    print("TESTING ENHANCED REPORT PARSER")
    print("=" * 60)
    
    # Parse the report
    analysis = parser.parse_report(sample_text, gender="female", age=50)
    
    print(f"\nReport Type: {analysis['report_type']}")
    print(f"Total Tests Found: {analysis['total_tests']}")
    
    if analysis['total_tests'] > 0:
        print("\n" + "=" * 60)
        print("DETAILED RESULTS:")
        print("=" * 60)
        
        for result in analysis['all_results']:
            term = result['term']
            value = result['value']
            unit = result['unit']
            status = result['interpretation']['status']
            print(f"\n{term}: {value} {unit} ({status})")
            print(f"   Normal Range: {result['interpretation']['normal_range']}")
    else:
        print("\n❌ NO TESTS FOUND! Check extraction patterns.")