"""
Medical Report Parser - BULLETPROOF VERSION
Handles messy OCR text with values on different lines
NO AI REQUIRED - Pure pattern matching & logic
"""

import re
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try different import paths
try:
    from utils.medical_knowledge import MedicalKnowledgeBase
except ImportError:
    try:
        from medical_knowledge import MedicalKnowledgeBase
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from medical_knowledge import MedicalKnowledgeBase

class MedicalReportParser:
    
    def __init__(self):
        self.kb = MedicalKnowledgeBase()
        
        # Test name patterns (case-insensitive)
        self.test_patterns = {
            # HbA1c
            r'HbA1c': 'HbA1c',
            r'Hb\s*A1c': 'HbA1c',
            r'GLYCATED\s*HEMOGLOBIN': 'HbA1c',
            
            # Cholesterol
            r'TOTAL\s*CHOLESTEROL': 'Total Cholesterol',
            r'CHOLESTEROL\s*TOTAL': 'Total Cholesterol',
            
            # HDL
            r'HDL\s*CHOLESTEROL': 'HDL',
            r'HIGH\s*DENSITY\s*LIPOPROTEIN': 'HDL',
            
            # LDL
            r'LDL\s*CHOLESTEROL': 'LDL',
            r'LOW\s*DENSITY\s*LIPOPROTEIN': 'LDL',
            
            # Triglycerides
            r'TRIGLYCERIDES': 'Triglycerides',
            
            # Glucose
            r'GLUCOSE': 'Glucose',
            r'BLOOD\s*SUGAR': 'Glucose',
            r'FASTING\s*BLOOD\s*GLUCOSE': 'Glucose',
            
            # Hemoglobin
            r'HEMOGLOBIN': 'Hemoglobin',
            r'HAEMOGLOBIN': 'Hemoglobin',
            
            # Thyroid
            r'TSH': 'TSH',
            r'THYROID\s*STIMULATING\s*HORMONE': 'TSH',
            r'T3': 'T3',
            r'TRIIODOTHYRONINE': 'T3',
            r'T4': 'T4',
            r'THYROXINE': 'T4',
            
            # Liver
            r'SGOT': 'AST',
            r'AST': 'AST',
            r'ASPARTATE\s*AMINOTRANSFERASE': 'AST',
            r'SGPT': 'ALT',
            r'ALT': 'ALT',
            r'ALANINE\s*TRANSAMINASE': 'ALT',
            r'BILIRUBIN': 'Bilirubin',
            
            # Kidney
            r'CREATININE': 'Creatinine',
            r'BUN': 'BUN',
            r'UREA': 'BUN',
            
            # Others
            r'URIC\s*ACID': 'Uric Acid',
            r'TROPONIN': 'Troponin',
            r'WBC': 'WBC',
            r'RBC': 'RBC',
            r'PLATELETS': 'Platelets',
            r'VITAMIN\s*D': 'Vitamin D',
            r'VITAMIN\s*B12': 'Vitamin B12',
            r'CALCIUM': 'Calcium',
            r'SODIUM': 'Sodium',
            r'POTASSIUM': 'Potassium',
            r'IRON': 'Iron',
        }
    
    def extract_test_results(self, ocr_text):
        """
        BULLETPROOF extraction that handles messy OCR
        Strategy: Find test names, then find values near them
        """
        results = []
        lines = ocr_text.split('\n')
        
        # Step 1: Find all test names and their line numbers
        test_locations = []
        for i, line in enumerate(lines):
            line_upper = line.upper().strip()
            for pattern, standard_name in self.test_patterns.items():
                if re.search(pattern, line_upper, re.IGNORECASE):
                    test_locations.append({
                        'name': standard_name,
                        'line_num': i,
                        'original_line': line
                    })
                    break  # Only one match per line
        
        # Step 2: For each test, find its value
        for test_loc in test_locations:
            value_found = self._find_value_for_test(
                test_loc, 
                lines, 
                ocr_text
            )
            if value_found:
                results.append(value_found)
        
        # Remove duplicates (keep first occurrence)
        seen = set()
        unique_results = []
        for r in results:
            if r['term'] not in seen:
                unique_results.append(r)
                seen.add(r['term'])
        
        return unique_results
    
    def _find_value_for_test(self, test_loc, lines, full_text):
        """
        Find the numeric value for a specific test
        Looks in: same line, next 3 lines, structured table format
        """
        test_name = test_loc['name']
        start_line = test_loc['line_num']
        
        # Strategy 1: Check same line for value
        same_line = lines[start_line]
        value = self._extract_number_from_line(same_line)
        if value:
            unit = self._get_unit_for_test(test_name, same_line)
            return self._create_result(test_name, value, unit, start_line)
        
        # Strategy 2: Check next 3 lines for standalone number
        for offset in range(1, 4):
            if start_line + offset < len(lines):
                next_line = lines[start_line + offset].strip()
                value = self._extract_number_from_line(next_line)
                if value:
                    unit = self._get_unit_for_test(test_name, next_line)
                    return self._create_result(test_name, value, unit, start_line)
        
        # Strategy 3: Look for table format
        # Example: "TEST_NAME    VALUE   UNIT"
        # Find test name, then look for numbers in nearby columns
        test_line = lines[start_line]
        
        # Extract all numbers from the surrounding context (10 lines after test name)
        context_lines = lines[start_line:start_line+10]
        context_text = ' '.join(context_lines)
        
        # Find all numbers with units
        number_matches = re.findall(r'(\d+\.?\d*)\s*(mg/dL|%|g/dL|mIU/L|pg/mL|µg/dL|U/L|mmol/L)', context_text)
        
        if number_matches:
            # Use first number found (most likely to be the value)
            value_str, unit = number_matches[0]
            value = float(value_str)
            
            # Verify unit matches expected unit for this test
            expected_unit = self._get_expected_unit(test_name)
            if expected_unit and unit.lower() == expected_unit.lower():
                return self._create_result(test_name, value, unit, start_line)
            elif not expected_unit:  # No expected unit, accept any
                return self._create_result(test_name, value, unit, start_line)
        
        return None
    
    def _extract_number_from_line(self, line):
        """Extract first valid number from a line"""
        # Look for number with optional decimal
        match = re.search(r'(\d+\.?\d*)', line)
        if match:
            try:
                value = float(match.group(1))
                # Sanity check: medical values are usually between 0.1 and 10000
                if 0.1 <= value <= 10000:
                    return value
            except:
                pass
        return None
    
    def _get_unit_for_test(self, test_name, text):
        """Get unit from text or from knowledge base"""
        # Try to find unit in text
        units = ['mg/dL', '%', 'g/dL', 'mIU/L', 'pg/mL', 'µg/dL', 'U/L', 'mmol/L']
        for unit in units:
            if unit in text:
                return unit
        
        # Fallback to knowledge base
        return self._get_expected_unit(test_name)
    
    def _get_expected_unit(self, test_name):
        """Get expected unit from knowledge base"""
        normal_range = self.kb.get_normal_range(test_name)
        if normal_range:
            return normal_range.get('unit', '')
        return ''
    
    def _create_result(self, test_name, value, unit, line_num):
        """Create a result dictionary"""
        return {
            'term': test_name,
            'raw_term': test_name,
            'value': value,
            'unit': unit,
            'line_number': line_num
        }
    
    def parse_report(self, ocr_text, gender="female", age=50):
        """
        Main parsing function
        Returns complete analysis with interpretations
        """
        print(f"\n{'='*60}")
        print(f"PARSING REPORT (Gender: {gender}, Age: {age})")
        print(f"{'='*60}")
        
        # Extract raw test results
        test_results = self.extract_test_results(ocr_text)
        
        print(f"\n✅ Found {len(test_results)} tests:")
        for r in test_results:
            print(f"   • {r['term']}: {r['value']} {r['unit']}")
        
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
        
        print(f"\n📋 Report Type: {report_type}")
        print(f"   Normal: {len(categorized['normal'])}")
        print(f"   High: {len(categorized['high'])}")
        print(f"   Low: {len(categorized['low'])}")
        print(f"   Critical: {len(categorized['critical'])}")
        print(f"{'='*60}\n")
        
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
            return "Diabetes Screening / Lipid Profile"
        
        return "General Health Panel"


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    # Test with ACTUAL messy OCR text from Test_Report2.pdf
    sample_text = """
    HbA1c - (HPLC)
    H.P.L.C 5.9 %
    
    TOTAL CHOLESTEROL PHOTOMETRY mg/dL < 200
    HDL CHOLESTEROL - DIRECT PHOTOMETRY mg/dL 40-60
    LDL CHOLESTEROL - DIRECT PHOTOMETRY mg/dL < 100
    TRIGLYCERIDES PHOTOMETRY mg/dL < 150
    
    195
    46
    118
    210
    
    TROPONIN I HEART ATTACK RISK 1.4 pg/mL
    """
    
    parser = MedicalReportParser()
    
    print("=" * 60)
    print("TESTING BULLETPROOF PARSER")
    print("=" * 60)
    
    # Parse the report
    analysis = parser.parse_report(sample_text, gender="female", age=50)
    
    print(f"\nReport Type: {analysis['report_type']}")
    print(f"Total Tests Found: {analysis['total_tests']}")
    
    print("\n" + "=" * 60)
    print("ALL RESULTS:")
    print("=" * 60)
    
    for result in analysis['all_results']:
        status_emoji = "✅" if result['interpretation']['status'] == 'normal' else "⚠️"
        print(f"\n{status_emoji} {result['term']}: {result['value']} {result['unit']}")
        print(f"   Status: {result['interpretation']['status'].upper()}")
        print(f"   Normal Range: {result['interpretation']['normal_range']}")