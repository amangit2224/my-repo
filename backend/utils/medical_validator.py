"""
Medical Validator - Statistical Anomaly Detection
Detects impossible or suspicious medical values
NO AI REQUIRED - Pure medical logic and statistics
"""

import statistics
from typing import Dict, List, Any

class MedicalValidator:
    
    def __init__(self):
        # Known medical correlations and rules
        self.correlations = {
            'HbA1c_Glucose': self._validate_hba1c_glucose,
            'Cholesterol_Components': self._validate_cholesterol_math,
            'Liver_Enzymes': self._validate_liver_enzymes,
            'Thyroid_Hormones': self._validate_thyroid_correlation,
        }
        
        # Physiologically impossible ranges (incompatible with life)
        self.impossible_ranges = {
            'Total Cholesterol': {'min': 50, 'max': 600},
            'Glucose': {'min': 20, 'max': 600},
            'HbA1c': {'min': 3.0, 'max': 18.0},
            'HDL': {'min': 10, 'max': 150},
            'LDL': {'min': 10, 'max': 400},
            'Triglycerides': {'min': 20, 'max': 1000},
            'TSH': {'min': 0.01, 'max': 100},
            'Hemoglobin': {'min': 3.0, 'max': 25.0},
            'Creatinine': {'min': 0.1, 'max': 20.0},
            'ALT': {'min': 1, 'max': 5000},
            'AST': {'min': 1, 'max': 5000},
        }
    
    def validate_report(self, parsed_data: Dict) -> Dict:
        """
        Main validation function
        Returns suspicion score and detailed findings
        """
        print(f"\n{'='*60}")
        print(f"🔬 MEDICAL VALIDATION")
        print(f"{'='*60}\n")
        
        suspicion_score = 0
        findings = []
        
        all_results = parsed_data.get('all_results', [])
        
        if not all_results:
            return {
                'suspicion_score': 0,
                'findings': ['No test results to validate'],
                'validated': False
            }
        
        # Check 1: Physiologically impossible values
        impossible_checks = self._check_impossible_values(all_results)
        suspicion_score += impossible_checks['score']
        findings.extend(impossible_checks['findings'])
        
        # Check 2: Statistical outliers
        outlier_checks = self._check_statistical_outliers(all_results)
        suspicion_score += outlier_checks['score']
        findings.extend(outlier_checks['findings'])
        
        # Check 3: Cross-value correlations
        correlation_checks = self._check_correlations(all_results)
        suspicion_score += correlation_checks['score']
        findings.extend(correlation_checks['findings'])
        
        # Check 4: Value precision (fake reports often have "too perfect" values)
        precision_checks = self._check_value_precision(all_results)
        suspicion_score += precision_checks['score']
        findings.extend(precision_checks['findings'])
        
        print(f"\n📊 Medical Validation Summary:")
        print(f"   Suspicion Score: {suspicion_score}")
        print(f"   Findings: {len(findings)}")
        print(f"{'='*60}\n")
        
        return {
            'suspicion_score': suspicion_score,
            'findings': findings,
            'validated': suspicion_score < 30,
            'details': {
                'impossible_values': impossible_checks['count'],
                'statistical_outliers': outlier_checks['count'],
                'correlation_issues': correlation_checks['count'],
                'precision_issues': precision_checks['count']
            }
        }
    
    def _check_impossible_values(self, results: List[Dict]) -> Dict:
        """Check for physiologically impossible values"""
        score = 0
        findings = []
        count = 0
        
        for result in results:
            term = result['term']
            value = result['value']
            
            if term in self.impossible_ranges:
                range_check = self.impossible_ranges[term]
                
                if value < range_check['min']:
                    score += 30
                    count += 1
                    findings.append(
                        f"🚨 CRITICAL: {term} = {value} is impossibly low "
                        f"(minimum compatible with life: {range_check['min']})"
                    )
                    print(f"🚨 Impossible value: {term} = {value} (too low)")
                    
                elif value > range_check['max']:
                    score += 30
                    count += 1
                    findings.append(
                        f"🚨 CRITICAL: {term} = {value} is impossibly high "
                        f"(maximum compatible with life: {range_check['max']})"
                    )
                    print(f"🚨 Impossible value: {term} = {value} (too high)")
        
        if count == 0:
            print("✅ All values within physiologically possible ranges")
        
        return {'score': score, 'findings': findings, 'count': count}
    
    def _check_statistical_outliers(self, results: List[Dict]) -> Dict:
        """Check for extreme statistical outliers"""
        score = 0
        findings = []
        count = 0
        
        # Known population statistics (mean ± 3 std dev covers 99.7% of normal population)
        population_stats = {
            'Total Cholesterol': {'mean': 190, 'std': 40},
            'HDL': {'mean': 55, 'std': 15},
            'LDL': {'mean': 115, 'std': 35},
            'Triglycerides': {'mean': 120, 'std': 60},
            'Glucose': {'mean': 95, 'std': 25},
            'HbA1c': {'mean': 5.5, 'std': 1.0},
        }
        
        for result in results:
            term = result['term']
            value = result['value']
            
            if term in population_stats:
                stats = population_stats[term]
                z_score = abs((value - stats['mean']) / stats['std'])
                
                # Z-score > 4 means extremely rare (1 in 15,787 chance)
                if z_score > 4:
                    score += 15
                    count += 1
                    findings.append(
                        f"⚠️ {term} = {value} is an extreme outlier "
                        f"(Z-score: {z_score:.2f} - occurs in <0.01% of population)"
                    )
                    print(f"⚠️ Extreme outlier: {term} = {value} (Z={z_score:.2f})")
                elif z_score > 3:
                    score += 5
                    findings.append(
                        f"⚠️ {term} = {value} is unusual "
                        f"(Z-score: {z_score:.2f} - occurs in <0.3% of population)"
                    )
                    print(f"⚠️ Unusual value: {term} = {value} (Z={z_score:.2f})")
        
        if count == 0:
            print("✅ No extreme statistical outliers detected")
        
        return {'score': score, 'findings': findings, 'count': count}
    
    def _check_correlations(self, results: List[Dict]) -> Dict:
        """Check medical correlations between values"""
        score = 0
        findings = []
        count = 0
        
        # Extract values into a dict for easier lookup
        values_dict = {r['term']: r['value'] for r in results}
        
        # Check HbA1c vs Glucose correlation
        if 'HbA1c' in values_dict and 'Glucose' in values_dict:
            check = self._validate_hba1c_glucose(values_dict['HbA1c'], values_dict['Glucose'])
            if not check['valid']:
                score += check['suspicion']
                count += 1
                findings.append(check['message'])
                print(f"⚠️ {check['message']}")
        
        # Check cholesterol math
        if all(k in values_dict for k in ['Total Cholesterol', 'HDL', 'LDL', 'Triglycerides']):
            check = self._validate_cholesterol_math(
                values_dict['Total Cholesterol'],
                values_dict['HDL'],
                values_dict['LDL'],
                values_dict['Triglycerides']
            )
            if not check['valid']:
                score += check['suspicion']
                count += 1
                findings.append(check['message'])
                print(f"⚠️ {check['message']}")
        
        # Check liver enzyme ratio
        if 'AST' in values_dict and 'ALT' in values_dict:
            check = self._validate_liver_enzymes(values_dict['AST'], values_dict['ALT'])
            if not check['valid']:
                score += check['suspicion']
                count += 1
                findings.append(check['message'])
                print(f"⚠️ {check['message']}")
        
        # Check thyroid hormone correlation
        if all(k in values_dict for k in ['TSH', 'T3', 'T4']):
            check = self._validate_thyroid_correlation(
                values_dict['TSH'],
                values_dict['T3'],
                values_dict['T4']
            )
            if not check['valid']:
                score += check['suspicion']
                count += 1
                findings.append(check['message'])
                print(f"⚠️ {check['message']}")
        
        if count == 0:
            print("✅ All value correlations appear consistent")
        
        return {'score': score, 'findings': findings, 'count': count}
    
    def _validate_hba1c_glucose(self, hba1c: float, glucose: float) -> Dict:
        """
        Validate HbA1c and Glucose correlation
        HbA1c reflects average glucose over 3 months
        """
        # Approximate conversion: HbA1c% → Average Glucose (mg/dL)
        # Formula: Average Glucose ≈ (HbA1c × 28.7) - 46.7
        expected_glucose = (hba1c * 28.7) - 46.7
        
        # Allow 30% tolerance (since glucose fluctuates)
        tolerance = 0.30
        lower_bound = expected_glucose * (1 - tolerance)
        upper_bound = expected_glucose * (1 + tolerance)
        
        if glucose < lower_bound or glucose > upper_bound:
            return {
                'valid': False,
                'suspicion': 20,
                'message': (
                    f"🚨 HbA1c ({hba1c}%) and Glucose ({glucose} mg/dL) don't correlate. "
                    f"Expected glucose: {expected_glucose:.0f} mg/dL (±30%). "
                    f"This mismatch is medically suspicious."
                )
            }
        
        return {'valid': True, 'suspicion': 0, 'message': ''}
    
    def _validate_cholesterol_math(self, total: float, hdl: float, ldl: float, trig: float) -> Dict:
        """
        Validate cholesterol math: Total ≈ HDL + LDL + (Triglycerides/5)
        """
        calculated_total = hdl + ldl + (trig / 5)
        difference = abs(total - calculated_total)
        
        # Allow 10% tolerance for measurement variance
        tolerance = total * 0.10
        
        if difference > tolerance:
            return {
                'valid': False,
                'suspicion': 25,
                'message': (
                    f"🚨 Cholesterol math doesn't add up! "
                    f"Total Cholesterol ({total}) ≠ HDL ({hdl}) + LDL ({ldl}) + VLDL ({trig/5:.1f}). "
                    f"Calculated total: {calculated_total:.1f}. Difference: {difference:.1f}. "
                    f"This suggests data fabrication."
                )
            }
        
        return {'valid': True, 'suspicion': 0, 'message': ''}
    
    def _validate_liver_enzymes(self, ast: float, alt: float) -> Dict:
        """
        Validate AST/ALT ratio
        Normal ratio: 0.8 - 1.5
        Very high or very low ratios are suspicious
        """
        if alt == 0:
            return {'valid': True, 'suspicion': 0, 'message': ''}
        
        ratio = ast / alt
        
        # Extreme ratios (>5 or <0.2) are very unusual
        if ratio > 5 or ratio < 0.2:
            return {
                'valid': False,
                'suspicion': 15,
                'message': (
                    f"⚠️ AST/ALT ratio ({ratio:.2f}) is extremely unusual. "
                    f"Normal ratio: 0.8-1.5. This pattern is rare and suspicious."
                )
            }
        
        return {'valid': True, 'suspicion': 0, 'message': ''}
    
    def _validate_thyroid_correlation(self, tsh: float, t3: float, t4: float) -> Dict:
        """
        Validate thyroid hormone correlation
        High TSH should correlate with low T3/T4 (hypothyroid)
        Low TSH should correlate with high T3/T4 (hyperthyroid)
        """
        # TSH > 4.5 = hypothyroid (expect low T3/T4)
        # TSH < 0.5 = hyperthyroid (expect high T3/T4)
        
        # Normal ranges (approximate)
        t3_normal = (0.8, 2.0)  # ng/mL
        t4_normal = (4.5, 11.2)  # µg/dL
        
        issues = []
        
        # High TSH with high T3/T4 (contradictory)
        if tsh > 4.5 and (t3 > t3_normal[1] or t4 > t4_normal[1]):
            issues.append("High TSH but high T3/T4 (contradictory)")
        
        # Low TSH with low T3/T4 (contradictory)
        if tsh < 0.5 and (t3 < t3_normal[0] or t4 < t4_normal[0]):
            issues.append("Low TSH but low T3/T4 (contradictory)")
        
        if issues:
            return {
                'valid': False,
                'suspicion': 20,
                'message': (
                    f"⚠️ Thyroid hormones show contradictory pattern: {', '.join(issues)}. "
                    f"TSH={tsh}, T3={t3}, T4={t4}. This is medically inconsistent."
                )
            }
        
        return {'valid': True, 'suspicion': 0, 'message': ''}
    
    def _check_value_precision(self, results: List[Dict]) -> Dict:
        """
        Check if values have suspicious precision
        Fake reports often use round numbers or too many decimal places
        """
        score = 0
        findings = []
        count = 0
        
        round_values = 0
        
        for result in results:
            value = result['value']
            term = result['term']
            
            # Check if value is suspiciously round (like exactly 100, 200, etc.)
            if value == int(value) and value % 10 == 0 and value != 0:
                round_values += 1
        
        # If >50% of values are round numbers, it's suspicious
        if len(results) > 0:
            round_percentage = (round_values / len(results)) * 100
            
            if round_percentage > 50:
                score += 10
                count += 1
                findings.append(
                    f"⚠️ {round_percentage:.0f}% of values are suspiciously round numbers. "
                    f"Real lab results typically have decimal precision."
                )
                print(f"⚠️ {round_percentage:.0f}% values are round numbers (suspicious)")
        
        if count == 0:
            print("✅ Value precision appears normal")
        
        return {'score': score, 'findings': findings, 'count': count}


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    # Test with sample data
    validator = MedicalValidator()
    
    # Example 1: Consistent report (should pass)
    good_report = {
        'all_results': [
            {'term': 'HbA1c', 'value': 5.7},
            {'term': 'Glucose', 'value': 110},
            {'term': 'Total Cholesterol', 'value': 200},
            {'term': 'HDL', 'value': 50},
            {'term': 'LDL', 'value': 120},
            {'term': 'Triglycerides', 'value': 150},
        ]
    }
    
    print("Testing GOOD REPORT:")
    result1 = validator.validate_report(good_report)
    print(f"\nResult: Suspicion={result1['suspicion_score']}, Valid={result1['validated']}")
    
    print("\n" + "="*60 + "\n")
    
    # Example 2: Suspicious report (should fail)
    bad_report = {
        'all_results': [
            {'term': 'HbA1c', 'value': 12.0},  # Very high (diabetic)
            {'term': 'Glucose', 'value': 85},   # Normal (contradictory!)
            {'term': 'Total Cholesterol', 'value': 300},  # High
            {'term': 'HDL', 'value': 30},       # Low
            {'term': 'LDL', 'value': 150},      # High
            {'term': 'Triglycerides', 'value': 200},  # High
            # Math: 30 + 150 + 40 = 220, but total is 300 (doesn't match!)
        ]
    }
    
    print("Testing SUSPICIOUS REPORT:")
    result2 = validator.validate_report(bad_report)
    print(f"\nResult: Suspicion={result2['suspicion_score']}, Valid={result2['validated']}")
    print("\nFindings:")
    for finding in result2['findings']:
        print(f"  - {finding}")