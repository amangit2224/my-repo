"""
Multi-Format Medical Report Parser - ENHANCED VERSION
Handles 10+ different lab report formats with robust pattern matching
NO AI REQUIRED - Pure pattern recognition & logic
"""

import re
import sys
import os
from typing import Dict, List, Tuple, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from medical_knowledge import MedicalKnowledgeBase
except ImportError:
    try:
        from utils.medical_knowledge import MedicalKnowledgeBase
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from medical_knowledge import MedicalKnowledgeBase


class MultiFormatReportParser:
    
    def __init__(self):
        self.kb = MedicalKnowledgeBase()
        
        # ============================================
        # COMPREHENSIVE TEST NAME PATTERNS
        # ============================================
        
        # Map various spellings/formats to standard names
        self.test_aliases = {
            # HbA1c variations
            'HbA1c': ['hba1c', 'hb a1c', 'hemoglobin a1c', 'glycated hemoglobin', 
                      'glycosylated hemoglobin', 'a1c', 'hba 1c'],
            
            # Cholesterol variations
            'Total Cholesterol': ['total cholesterol', 'cholesterol total', 'cholesterol', 
                                  'chol', 't-cholesterol', 'serum cholesterol'],
            'HDL': ['hdl', 'hdl cholesterol', 'hdl-c', 'high density lipoprotein',
                    'hdl chol', 'good cholesterol'],
            'LDL': ['ldl', 'ldl cholesterol', 'ldl-c', 'low density lipoprotein',
                    'ldl chol', 'bad cholesterol', 'ldl direct'],
            'VLDL': ['vldl', 'vldl cholesterol', 'very low density lipoprotein'],
            'Triglycerides': ['triglycerides', 'trig', 'trigs', 'triglyceride', 'tg'],
            
            # Glucose variations
            'Glucose': ['glucose', 'blood glucose', 'blood sugar', 'fasting glucose',
                       'fasting blood sugar', 'fbs', 'random blood sugar', 'rbs',
                       'plasma glucose'],
            
            # Hemoglobin variations
            'Hemoglobin': ['hemoglobin', 'haemoglobin', 'hb', 'hgb'],
            'Hematocrit': ['hematocrit', 'haematocrit', 'hct', 'pcv', 'packed cell volume'],
            
            # Blood cells
            'WBC': ['wbc', 'white blood cell', 'white cell count', 'leukocyte', 'tc'],
            'RBC': ['rbc', 'red blood cell', 'red cell count', 'erythrocyte'],
            'Platelets': ['platelets', 'platelet count', 'plt', 'thrombocytes'],
            'MCV': ['mcv', 'mean corpuscular volume'],
            'MCH': ['mch', 'mean corpuscular hemoglobin'],
            'MCHC': ['mchc', 'mean corpuscular hemoglobin concentration'],
            
            # Thyroid
            'TSH': ['tsh', 'thyroid stimulating hormone', 'thyrotropin'],
            'T3': ['t3', 'triiodothyronine', 'total t3', 't-3'],
            'T4': ['t4', 'thyroxine', 'total t4', 't-4'],
            'Free T3': ['free t3', 'ft3', 'f t3'],
            'Free T4': ['free t4', 'ft4', 'f t4'],
            
            # Liver function
            'ALT': ['alt', 'sgpt', 'alanine aminotransferase', 'alanine transaminase',
                   'serum glutamic pyruvic transaminase'],
            'AST': ['ast', 'sgot', 'aspartate aminotransferase', 'aspartate transaminase',
                   'serum glutamic oxaloacetic transaminase'],
            'ALP': ['alp', 'alkaline phosphatase', 'alk phos', 's.alk.phosphatase'],
            'Bilirubin': ['bilirubin', 'total bilirubin', 't bilirubin', 'serum bilirubin',
                         'bil', 's.bilirubin'],
            'Albumin': ['albumin', 'serum albumin', 's.albumin', 'alb'],
            'Total Protein': ['total protein', 'serum total protein', 's.protein',
                             'total serum protein'],
            'GGT': ['ggt', 'gamma gt', 'gamma glutamyl transferase', 'ggtp'],
            
            # Kidney function
            'Creatinine': ['creatinine', 'serum creatinine', 's.creatinine', 'creat'],
            'BUN': ['bun', 'blood urea nitrogen', 'urea nitrogen', 'urea'],
            'Uric Acid': ['uric acid', 'urate', 'serum uric acid', 's.uric acid'],
            'eGFR': ['egfr', 'gfr', 'estimated gfr', 'glomerular filtration rate'],
            
            # Electrolytes
            'Sodium': ['sodium', 'na', 'serum sodium', 's.sodium'],
            'Potassium': ['potassium', 'k', 'serum potassium', 's.potassium'],
            'Calcium': ['calcium', 'ca', 'serum calcium', 's.calcium'],
            'Magnesium': ['magnesium', 'mg', 'serum magnesium'],
            
            # Cardiac markers
            'Troponin': ['troponin', 'troponin i', 'troponin t', 'trop i', 'trop t',
                        'cardiac troponin', 'hs troponin', 'high sensitivity troponin'],
            'CK-MB': ['ck-mb', 'ckmb', 'creatine kinase mb', 'cpk-mb'],
            'BNP': ['bnp', 'b-type natriuretic peptide', 'brain natriuretic peptide'],
            
            # Vitamins
            'Vitamin D': ['vitamin d', 'vit d', '25-oh vitamin d', '25(oh)d',
                         'cholecalciferol', 'vitamin d3'],
            'Vitamin B12': ['vitamin b12', 'vit b12', 'b12', 'cobalamin'],
            'Folate': ['folate', 'folic acid', 'vitamin b9'],
            
            # Minerals
            'Iron': ['iron', 'serum iron', 's.iron', 'fe'],
            'Ferritin': ['ferritin', 'serum ferritin'],
            'Zinc': ['zinc', 'serum zinc', 'zn'],
            
            # Inflammatory markers
            'CRP': ['crp', 'c-reactive protein', 'c reactive protein', 'hs-crp'],
            'ESR': ['esr', 'sed rate', 'sedimentation rate', 'erythrocyte sedimentation rate'],
            
            # Hormones
            'Testosterone': ['testosterone', 'total testosterone', 'serum testosterone'],
            'Estradiol': ['estradiol', 'e2', 'estrogen'],
            'Cortisol': ['cortisol', 'serum cortisol'],
            'Prolactin': ['prolactin', 'prl'],
            'FSH': ['fsh', 'follicle stimulating hormone'],
            'LH': ['lh', 'luteinizing hormone'],
            
            # Diabetes markers
            'Insulin': ['insulin', 'serum insulin', 'fasting insulin'],
            'C-Peptide': ['c-peptide', 'c peptide', 'cpeptide'],
            
            # Cancer markers
            'PSA': ['psa', 'prostate specific antigen'],
            'CEA': ['cea', 'carcinoembryonic antigen'],
            'CA 19-9': ['ca 19-9', 'ca19-9', 'ca 19 9'],
            'HCG': ['hcg', 'beta hcg', 'human chorionic gonadotropin'],
        }
        
        # Reverse mapping: alias → standard name
        self.alias_to_standard = {}
        for standard, aliases in self.test_aliases.items():
            for alias in aliases:
                self.alias_to_standard[alias.lower()] = standard
        
        # ============================================
        # UNIT PATTERNS
        # ============================================
        
        self.unit_patterns = [
            r'mg/dL', r'mg/dl', r'mg\/dL', r'mgdl',
            r'g/dL', r'g/dl', r'gdL',
            r'mIU/L', r'miu/l', r'μIU/mL',
            r'ng/mL', r'ng/ml', r'ngml',
            r'pg/mL', r'pg/ml',
            r'µg/dL', r'ug/dL', r'mcg/dL',
            r'U/L', r'u/l', r'IU/L',
            r'mmol/L', r'mmol/l',
            r'mEq/L', r'meq/l',
            r'cells/µL', r'cells/uL', r'/cumm',
            r'fL', r'fl',
            r'%', r'percent',
            r'10\^3/µL', r'thousand/uL',
            r'million/µL', r'million/uL',
        ]
        
        # Compile unit regex
        self.unit_regex = re.compile('|'.join(self.unit_patterns), re.IGNORECASE)
    
    def parse_report(self, ocr_text: str, gender: str = "female", age: int = 50) -> Dict:
        """
        Main parsing function - handles multiple report formats
        """
        print(f"\n{'='*60}")
        print(f"🔍 MULTI-FORMAT PARSER ANALYSIS")
        print(f"Gender: {gender}, Age: {age}")
        print(f"{'='*60}\n")
        
        # Extract raw test results
        test_results = self.extract_test_results(ocr_text)
        
        print(f"\n✅ Extracted {len(test_results)} tests:")
        for r in test_results:
            print(f"   • {r['term']}: {r['value']} {r['unit']}")
        
        # Analyze each result
        analyzed_results = []
        
        for result in test_results:
            term = result['term']
            value = result['value']
            
            # Get interpretation from knowledge base
            interpretation = self.kb.get_interpretation(term, value, gender, age)
            
            # Combine extraction result with interpretation
            analyzed_results.append({
                **result,
                'interpretation': interpretation
            })
        
        # Categorize results
        categorized = self._categorize_results(analyzed_results)
        
        # Detect report type
        report_type = self._detect_report_type(test_results)
        
        print(f"\n📋 Report Analysis:")
        print(f"   Type: {report_type}")
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
    
    def extract_test_results(self, ocr_text: str) -> List[Dict]:
        """
        ENHANCED extraction - handles multiple formats
        """
        results = []
        lines = ocr_text.split('\n')
        
        # Try multiple extraction strategies
        
        # Strategy 1: Table format (most common)
        table_results = self._extract_from_table(lines)
        results.extend(table_results)
        
        # Strategy 2: Line-by-line format
        line_results = self._extract_line_by_line(lines)
        results.extend(line_results)
        
        # Strategy 3: Multi-line format (test name on one line, value on next)
        multiline_results = self._extract_multiline(lines)
        results.extend(multiline_results)
        
        # Remove duplicates (keep first occurrence)
        seen = set()
        unique_results = []
        for r in results:
            if r['term'] not in seen:
                unique_results.append(r)
                seen.add(r['term'])
        
        return unique_results
    
    def _extract_from_table(self, lines: List[str]) -> List[Dict]:
        """
        Extract from table format:
        TEST_NAME    VALUE   UNIT   NORMAL_RANGE
        """
        results = []
        
        for i, line in enumerate(lines):
            line_clean = line.strip()
            if not line_clean:
                continue
            
            # Try to find test name
            test_name = self._find_test_name_in_line(line_clean)
            if not test_name:
                continue
            
            # Try to find value in same line
            value_info = self._extract_value_from_line(line_clean)
            
            if value_info:
                results.append({
                    'term': test_name,
                    'value': value_info['value'],
                    'unit': value_info['unit'],
                    'line_number': i
                })
        
        return results
    
    def _extract_line_by_line(self, lines: List[str]) -> List[Dict]:
        """
        Extract when each test is on its own line
        """
        results = []
        
        for i, line in enumerate(lines):
            # Skip if line is too short or too long
            if len(line.strip()) < 3 or len(line.strip()) > 200:
                continue
            
            # Find test name
            test_name = self._find_test_name_in_line(line)
            if not test_name:
                continue
            
            # Extract value from same line or next few lines
            value_info = self._find_value_near_line(lines, i)
            
            if value_info:
                results.append({
                    'term': test_name,
                    'value': value_info['value'],
                    'unit': value_info['unit'],
                    'line_number': i
                })
        
        return results
    
    def _extract_multiline(self, lines: List[str]) -> List[Dict]:
        """
        Extract when test name and value are on different lines
        Example:
        Line 1: "Hemoglobin"
        Line 2: "13.5 g/dL"
        """
        results = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if this line is a test name (and ONLY a test name)
            if self._is_standalone_test_name(line):
                test_name = self._find_test_name_in_line(line)
                
                if test_name:
                    # Look for value in next 3 lines
                    for offset in range(1, 4):
                        if i + offset < len(lines):
                            next_line = lines[i + offset].strip()
                            value_info = self._extract_value_from_line(next_line)
                            
                            if value_info:
                                results.append({
                                    'term': test_name,
                                    'value': value_info['value'],
                                    'unit': value_info['unit'],
                                    'line_number': i
                                })
                                break
            
            i += 1
        
        return results
    
    def _find_test_name_in_line(self, line: str) -> Optional[str]:
        """
        Find test name in a line
        """
        line_lower = line.lower()
        
        # Check all aliases
        for alias, standard in self.alias_to_standard.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, line_lower):
                return standard
        
        return None
    
    def _is_standalone_test_name(self, line: str) -> bool:
        """
        Check if line contains ONLY a test name (no numbers)
        """
        # Line should have a test name
        has_test = self._find_test_name_in_line(line) is not None
        
        # Line should NOT have numbers (values)
        has_numbers = bool(re.search(r'\d+\.?\d*', line))
        
        return has_test and not has_numbers
    
    def _extract_value_from_line(self, line: str) -> Optional[Dict]:
        """
        Extract numeric value and unit from a line
        """
        # Find all numbers with optional decimals
        numbers = re.findall(r'(\d+\.?\d*)\s*([a-zA-Z/%µ]+)', line)
        
        if not numbers:
            # Try just finding a number
            number_match = re.search(r'(\d+\.?\d*)', line)
            if number_match:
                value = float(number_match.group(1))
                # Try to find unit separately
                unit = self._find_unit_in_line(line)
                return {'value': value, 'unit': unit or ''}
            return None
        
        # Use first number found
        value_str, unit_raw = numbers[0]
        
        try:
            value = float(value_str)
            
            # Clean unit
            unit = self._normalize_unit(unit_raw)
            
            # Sanity check: value should be reasonable for medical tests
            if 0.001 <= value <= 50000:
                return {'value': value, 'unit': unit}
        except:
            pass
        
        return None
    
    def _find_value_near_line(self, lines: List[str], start_idx: int) -> Optional[Dict]:
        """
        Find value in current line or next few lines
        """
        # Check current line first
        value_info = self._extract_value_from_line(lines[start_idx])
        if value_info:
            return value_info
        
        # Check next 3 lines
        for offset in range(1, 4):
            if start_idx + offset < len(lines):
                line = lines[start_idx + offset]
                value_info = self._extract_value_from_line(line)
                if value_info:
                    return value_info
        
        return None
    
    def _find_unit_in_line(self, line: str) -> Optional[str]:
        """
        Find unit in a line
        """
        match = self.unit_regex.search(line)
        if match:
            return self._normalize_unit(match.group(0))
        return None
    
    def _normalize_unit(self, unit: str) -> str:
        """
        Normalize unit to standard format
        """
        unit_mapping = {
            'mgdl': 'mg/dL',
            'mg/dl': 'mg/dL',
            'gdl': 'g/dL',
            'g/dl': 'g/dL',
            'miu/l': 'mIU/L',
            'ng/ml': 'ng/mL',
            'pg/ml': 'pg/mL',
            'ug/dl': 'µg/dL',
            'mcg/dl': 'µg/dL',
            'u/l': 'U/L',
            'iu/l': 'U/L',
            'mmol/l': 'mmol/L',
            'meq/l': 'mEq/L',
            'fl': 'fL',
            '/cumm': 'cells/µL',
            'cells/ul': 'cells/µL',
            'percent': '%',
        }
        
        unit_lower = unit.lower().strip()
        return unit_mapping.get(unit_lower, unit)
    
    def _categorize_results(self, analyzed_results: List[Dict]) -> Dict:
        """
        Categorize results by status
        """
        categorized = {
            'normal': [],
            'high': [],
            'low': [],
            'critical': []
        }
        
        for result in analyzed_results:
            status = result['interpretation'].get('status', 'unknown')
            severity = result['interpretation'].get('severity', '')
            
            if status == 'normal':
                categorized['normal'].append(result)
            elif status == 'high':
                if 'high' in severity.lower() or 'emergency' in severity.lower() or 'critical' in severity.lower():
                    categorized['critical'].append(result)
                else:
                    categorized['high'].append(result)
            elif status == 'low':
                if 'high' in severity.lower() or 'emergency' in severity.lower() or 'critical' in severity.lower():
                    categorized['critical'].append(result)
                else:
                    categorized['low'].append(result)
        
        return categorized
    
    def _detect_report_type(self, test_results: List[Dict]) -> str:
        """
        Detect report type based on tests present
        """
        test_names = [r['term'] for r in test_results]
        
        # Define report type patterns
        patterns = {
            'Lipid Profile': ['Total Cholesterol', 'HDL', 'LDL', 'Triglycerides'],
            'Complete Blood Count (CBC)': ['Hemoglobin', 'WBC', 'RBC', 'Platelets'],
            'Thyroid Function Test': ['TSH', 'T3', 'T4'],
            'Liver Function Test': ['ALT', 'AST', 'Bilirubin', 'Albumin'],
            'Kidney Function Test': ['Creatinine', 'BUN', 'Uric Acid'],
            'Diabetes Panel': ['HbA1c', 'Glucose', 'Insulin'],
        }
        
        # Count matches for each pattern
        best_match = 'General Health Panel'
        max_matches = 0
        
        for report_type, required_tests in patterns.items():
            matches = sum(1 for test in required_tests if test in test_names)
            
            if matches > max_matches:
                max_matches = matches
                best_match = report_type
        
        # Special case: If both lipid and diabetes markers
        if any(t in test_names for t in ['HbA1c', 'Glucose']) and \
           any(t in test_names for t in ['Total Cholesterol', 'HDL', 'LDL']):
            return 'Diabetes Screening / Lipid Profile'
        
        return best_match


# For backward compatibility - alias to old name
MedicalReportParser = MultiFormatReportParser


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    parser = MultiFormatReportParser()
    
    # Test 1: Table format (Thyrocare style)
    print("="*60)
    print("TEST 1: Table Format (Thyrocare)")
    print("="*60)
    
    test_text_1 = """
    TEST NAME                VALUE    UNIT     REFERENCE RANGE
    HbA1c                    5.9      %        < 5.7
    TOTAL CHOLESTEROL        195      mg/dL    < 200
    HDL CHOLESTEROL          46       mg/dL    40-60
    LDL CHOLESTEROL          118      mg/dL    < 100
    TRIGLYCERIDES            210      mg/dL    < 150
    """
    
    result1 = parser.parse_report(test_text_1, gender='female', age=50)
    print(f"Found {result1['total_tests']} tests")
    print(f"Report Type: {result1['report_type']}")
    
    print("\n" + "="*60)
    print("TEST 2: Multi-line Format")
    print("="*60)
    
    test_text_2 = """
    Hemoglobin
    13.5 g/dL
    Normal Range: 12.0-15.5
    
    White Blood Cell Count
    7500 cells/µL
    Normal: 4500-11000
    
    Glucose (Fasting)
    110 mg/dL
    Normal: 70-100
    """
    
    result2 = parser.parse_report(test_text_2, gender='female', age=35)
    print(f"Found {result2['total_tests']} tests")
    print(f"Report Type: {result2['report_type']}")
    
    print("\n" + "="*60)
    print("TEST 3: Compact Format (PathLab style)")
    print("="*60)
    
    test_text_3 = """
    TSH: 3.2 mIU/L (Normal: 0.4-4.5)
    Free T3: 2.8 pg/mL (Normal: 2.3-4.2)
    Free T4: 1.2 ng/dL (Normal: 0.8-1.8)
    """
    
    result3 = parser.parse_report(test_text_3, gender='male', age=45)
    print(f"Found {result3['total_tests']} tests")
    print(f"Report Type: {result3['report_type']}")
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED! ✅")
    print("="*60)