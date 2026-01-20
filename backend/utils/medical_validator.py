"""
Medical Statistical Validator
Detects impossible/suspicious medical values using domain knowledge
NO AI - Pure medical logic and statistics
"""

class MedicalValidator:
    
    def __init__(self):
        self.suspicion_score = 0
        self.findings = []
        
        # Physiologically impossible ranges (would be fatal/impossible)
        self.impossible_ranges = {
            'Hemoglobin': {'min': 3.0, 'max': 25.0, 'unit': 'g/dL'},
            'Glucose': {'min': 20, 'max': 800, 'unit': 'mg/dL'},
            'HbA1c': {'min': 2.0, 'max': 20.0, 'unit': '%'},
            'Total Cholesterol': {'min': 50, 'max': 600, 'unit': 'mg/dL'},
            'HDL': {'min': 10, 'max': 150, 'unit': 'mg/dL'},
            'LDL': {'min': 10, 'max': 400, 'unit': 'mg/dL'},
            'Triglycerides': {'min': 20, 'max': 1000, 'unit': 'mg/dL'},
            'WBC': {'min': 0.5, 'max': 100.0, 'unit': '10^3/µL'},
            'RBC': {'min': 1.0, 'max': 10.0, 'unit': '10^6/µL'},
            'Platelets': {'min': 10, 'max': 1000, 'unit': '10^3/µL'},
            'Creatinine': {'min': 0.2, 'max': 25.0, 'unit': 'mg/dL'},
            'TSH': {'min': 0.01, 'max': 100.0, 'unit': 'mIU/L'},
            'ALT': {'min': 1, 'max': 5000, 'unit': 'U/L'},
            'AST': {'min': 1, 'max': 5000, 'unit': 'U/L'},
            'Troponin': {'min': 0, 'max': 100000, 'unit': 'ng/mL'},
        }
    
    def validate_report(self, parsed_data):
        """
        Validate medical values for statistical plausibility
        Returns suspicion score and findings
        """
        
        print(f"\n{'='*60}")
        print(f"🧪 MEDICAL STATISTICAL VALIDATION")
        print(f"{'='*60}\n")
        
        if not parsed_data or not parsed_data.get('all_results'):
            return {
                'valid': True,
                'suspicion_score': 0,
                'findings': ['No test results to validate'],
                'warnings': []
            }
        
        all_results = parsed_data['all_results']
        
        # Run validation checks
        self._check_impossible_values(all_results)
        self._check_value_relationships(all_results)
        self._check_statistical_outliers(all_results)
        
        # Generate warnings based on severity
        warnings = self._generate_warnings()
        
        print(f"\n{'='*60}")
        print(f"📊 VALIDATION SUMMARY:")
        print(f"   Medical Suspicion Score: {self.suspicion_score}")
        print(f"   Findings: {len(self.findings)}")
        print(f"   Warnings: {len(warnings)}")
        print(f"{'='*60}\n")
        
        return {
            'valid': self.suspicion_score < 30,
            'suspicion_score': self.suspicion_score,
            'findings': self.findings,
            'warnings': warnings
        }
    
    def _check_impossible_values(self, results):
        """Check for physiologically impossible values"""
        for result in results:
            term = result['term']
            value = result['value']
            
            if term in self.impossible_ranges:
                limits = self.impossible_ranges[term]
                
                if value < limits['min']:
                    self.suspicion_score += 30
                    self.findings.append(
                        f"🚨 {term} = {value} {result['unit']} is impossibly LOW "
                        f"(minimum survivable: {limits['min']} {limits['unit']})"
                    )
                    print(f"🚨 IMPOSSIBLE: {term} = {value} (too low) +30 suspicion")
                
                elif value > limits['max']:
                    self.suspicion_score += 30
                    self.findings.append(
                        f"🚨 {term} = {value} {result['unit']} is impossibly HIGH "
                        f"(maximum survivable: {limits['max']} {limits['unit']})"
                    )
                    print(f"🚨 IMPOSSIBLE: {term} = {value} (too high) +30 suspicion")
                
                else:
                    print(f"✅ {term} = {value} (within possible range)")
    
    def _check_value_relationships(self, results):
        """Check for medically inconsistent combinations"""
        
        # Create lookup dictionary
        values_dict = {r['term']: r['value'] for r in results}
        
        # Check HbA1c vs Glucose consistency
        if 'HbA1c' in values_dict and 'Glucose' in values_dict:
            hba1c = values_dict['HbA1c']
            glucose = values_dict['Glucose']
            
            # HbA1c to average glucose approximation
            # Formula: Average Glucose ≈ (HbA1c * 28.7) - 46.7
            estimated_glucose = (hba1c * 28.7) - 46.7
            
            # Allow 50% variance
            if abs(glucose - estimated_glucose) > estimated_glucose * 0.5:
                self.suspicion_score += 15
                self.findings.append(
                    f"⚠️ HbA1c ({hba1c}%) and Glucose ({glucose} mg/dL) are inconsistent. "
                    f"Expected glucose: ~{estimated_glucose:.0f} mg/dL"
                )
                print(f"⚠️  HbA1c-Glucose mismatch +15 suspicion")
            else:
                print(f"✅ HbA1c-Glucose correlation normal")
        
        # Check Total Cholesterol vs LDL+HDL+Triglycerides
        if all(k in values_dict for k in ['Total Cholesterol', 'LDL', 'HDL', 'Triglycerides']):
            total = values_dict['Total Cholesterol']
            ldl = values_dict['LDL']
            hdl = values_dict['HDL']
            trig = values_dict['Triglycerides']
            
            # Friedewald equation: Total ≈ LDL + HDL + (Trig/5)
            calculated_total = ldl + hdl + (trig / 5)
            
            # Allow 15% variance
            if abs(total - calculated_total) > calculated_total * 0.15:
                self.suspicion_score += 15
                self.findings.append(
                    f"⚠️ Lipid values don't match Friedewald equation. "
                    f"Total Cholesterol: {total}, Calculated: {calculated_total:.1f}"
                )
                print(f"⚠️  Lipid equation mismatch +15 suspicion")
            else:
                print(f"✅ Lipid profile mathematically consistent")
        
        # Check Hemoglobin vs Hematocrit (if available)
        if 'Hemoglobin' in values_dict and 'Hematocrit' in values_dict:
            hgb = values_dict['Hemoglobin']
            hct = values_dict['Hematocrit']
            
            # Rule of thumb: Hematocrit ≈ Hemoglobin * 3
            expected_hct = hgb * 3
            
            # Allow 15% variance
            if abs(hct - expected_hct) > expected_hct * 0.15:
                self.suspicion_score += 10
                self.findings.append(
                    f"⚠️ Hemoglobin ({hgb}) and Hematocrit ({hct}) ratio is unusual. "
                    f"Expected Hct: ~{expected_hct:.1f}"
                )
                print(f"⚠️  Hgb-Hct ratio unusual +10 suspicion")
            else:
                print(f"✅ Hemoglobin-Hematocrit ratio normal")
    
    def _check_statistical_outliers(self, results):
        """Check for statistically improbable patterns"""
        
        # Check for too many "perfect" round numbers
        round_numbers = 0
        for result in results:
            value = result['value']
            # Check if value is a round number (10, 50, 100, 150, 200)
            if value % 10 == 0 and value >= 10:
                round_numbers += 1
        
        # If more than 70% are perfect round numbers, suspicious
        if len(results) > 3 and round_numbers / len(results) > 0.7:
            self.suspicion_score += 10
            self.findings.append(
                f"⚠️ {round_numbers}/{len(results)} values are perfect round numbers - "
                f"statistically unusual for real lab results"
            )
            print(f"⚠️  Too many round numbers +10 suspicion")
        else:
            print(f"✅ Value distribution appears natural")
        
        # Check for duplicate values (different tests, same value)
        values_list = [r['value'] for r in results]
        unique_values = set(values_list)
        
        if len(results) > 5 and len(unique_values) < len(results) * 0.5:
            self.suspicion_score += 10
            self.findings.append(
                f"⚠️ Multiple tests have identical values - suspicious pattern"
            )
            print(f"⚠️  Suspicious duplicate values +10 suspicion")
        else:
            print(f"✅ No suspicious value patterns")
    
    def _generate_warnings(self):
        """Generate user-friendly warnings"""
        warnings = []
        
        if self.suspicion_score >= 40:
            warnings.append("🚨 CRITICAL: Medically impossible values detected")
            warnings.append("These results are physiologically impossible")
            warnings.append("Report is almost certainly fabricated")
        elif self.suspicion_score >= 25:
            warnings.append("⚠️ HIGH: Significant medical inconsistencies")
            warnings.append("Values don't follow expected medical relationships")
            warnings.append("Strongly recommend verification with lab")
        elif self.suspicion_score >= 10:
            warnings.append("⚠️ MODERATE: Some unusual patterns detected")
            warnings.append("Results may be legitimate but warrant scrutiny")
        else:
            warnings.append("✅ Medical values appear plausible")
            warnings.append("No statistical red flags detected")
        
        return warnings


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    # Test with sample data
    
    # Example 1: Normal values
    normal_data = {
        'all_results': [
            {'term': 'Hemoglobin', 'value': 14.5, 'unit': 'g/dL'},
            {'term': 'Glucose', 'value': 105, 'unit': 'mg/dL'},
            {'term': 'HbA1c', 'value': 5.7, 'unit': '%'},
        ]
    }
    
    # Example 2: Impossible values
    fake_data = {
        'all_results': [
            {'term': 'Hemoglobin', 'value': 50.0, 'unit': 'g/dL'},  # Impossible!
            {'term': 'Glucose', 'value': 1000, 'unit': 'mg/dL'},  # Impossible!
        ]
    }
    
    validator = MedicalValidator()
    
    print("="*60)
    print("TEST 1: Normal Values")
    print("="*60)
    result1 = validator.validate_report(normal_data)
    print(f"\nValid: {result1['valid']}")
    print(f"Suspicion: {result1['suspicion_score']}")
    
    print("\n" + "="*60)
    print("TEST 2: Impossible Values")
    print("="*60)
    validator2 = MedicalValidator()
    result2 = validator2.validate_report(fake_data)
    print(f"\nValid: {result2['valid']}")
    print(f"Suspicion: {result2['suspicion_score']}")
    print("\nFindings:")
    for finding in result2['findings']:
        print(f"  {finding}")