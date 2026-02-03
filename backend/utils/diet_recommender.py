"""
UNIVERSAL Diet Recommender System
✅ Works for ALL report types (Lipid, Liver, Thyroid, CBC, Kidney, etc.)
✅ Only analyzes tests that ACTUALLY EXIST in the report
✅ Easily extendable for new test types
✅ Medically accurate recommendations
"""

class UniversalDietRecommender:
    """
    Universal diet recommender that works with ANY medical report
    Analyzes only the tests that are present in the report
    """
    
    def __init__(self):
        """Initialize the diet recommender"""
        # Define normal ranges for ALL possible tests
        self.normal_ranges = {
            # Lipid Profile
            'total_cholesterol': {'min': 0, 'max': 200, 'unit': 'mg/dL'},
            'hdl': {'min': 40, 'max': 999, 'unit': 'mg/dL'},  # Higher is better
            'ldl': {'min': 0, 'max': 100, 'unit': 'mg/dL'},
            'triglycerides': {'min': 0, 'max': 150, 'unit': 'mg/dL'},
            'vldl': {'min': 5, 'max': 40, 'unit': 'mg/dL'},
            
            # Diabetes Markers
            'hba1c': {'min': 4.0, 'max': 5.6, 'unit': '%'},
            'glucose': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
            'fasting_glucose': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
            
            # Liver Function
            'sgot': {'min': 8, 'max': 48, 'unit': 'U/L'},
            'sgpt': {'min': 7, 'max': 45, 'unit': 'U/L'},
            'alp': {'min': 40, 'max': 130, 'unit': 'U/L'},
            'bilirubin_total': {'min': 0.1, 'max': 1.2, 'unit': 'mg/dL'},
            'bilirubin_direct': {'min': 0, 'max': 0.3, 'unit': 'mg/dL'},
            'ggt': {'min': 0, 'max': 65, 'unit': 'U/L'},
            'albumin': {'min': 3.5, 'max': 5.5, 'unit': 'g/dL'},
            'total_protein': {'min': 6.0, 'max': 8.3, 'unit': 'g/dL'},
            
            # Thyroid Function
            'tsh': {'min': 0.4, 'max': 4.5, 'unit': 'µIU/mL'},
            't3': {'min': 80, 'max': 200, 'unit': 'ng/dL'},
            't4': {'min': 4.8, 'max': 12.7, 'unit': 'µg/dL'},
            'free_t3': {'min': 2.3, 'max': 4.2, 'unit': 'pg/mL'},
            'free_t4': {'min': 0.8, 'max': 1.8, 'unit': 'ng/dL'},
            
            # Kidney Function
            'creatinine': {'min': 0.7, 'max': 1.3, 'unit': 'mg/dL'},
            'urea': {'min': 8, 'max': 24, 'unit': 'mg/dL'},
            'bun': {'min': 8, 'max': 24, 'unit': 'mg/dL'},
            'uric_acid': {'min': 3.4, 'max': 7.0, 'unit': 'mg/dL'},
            
            # CBC
            'hemoglobin': {'min': 12.0, 'max': 17.5, 'unit': 'g/dL'},
            'wbc': {'min': 4500, 'max': 11000, 'unit': 'cells/µL'},
            'platelets': {'min': 150000, 'max': 400000, 'unit': 'cells/µL'},
            
            # Vitamins & Minerals
            'iron': {'min': 50, 'max': 175, 'unit': 'µg/dL'},
            'ferritin': {'min': 11, 'max': 336, 'unit': 'ng/mL'},
            'vitamin_d': {'min': 30, 'max': 100, 'unit': 'ng/mL'},
            'vitamin_b12': {'min': 200, 'max': 900, 'unit': 'pg/mL'},
            'calcium': {'min': 8.5, 'max': 10.5, 'unit': 'mg/dL'},
            'sodium': {'min': 136, 'max': 145, 'unit': 'mEq/L'},
            'potassium': {'min': 3.5, 'max': 5.0, 'unit': 'mEq/L'},
        }
    
    def generate_diet_plan(self, parsed_data):
        """
        Generate diet plan based on ACTUAL tests in the report
        
        Args:
            parsed_data: Dictionary containing test results
            
        Returns:
            Complete diet plan dictionary
        """
        
        # Extract test values (only tests that exist)
        test_values = self._extract_test_values(parsed_data)
        
        print(f"\n{'='*60}")
        print(f"🍎 DIET PLAN GENERATION")
        print(f"{'='*60}")
        print(f"Found {len(test_values)} tests in report:")
        for test_name, value in test_values.items():
            print(f"  • {test_name}: {value}")
        print(f"{'='*60}\n")
        
        # Identify ACTUAL health conditions (only from tests that exist)
        conditions = self._identify_conditions(test_values)
        
        print(f"📋 Conditions Detected: {conditions}\n")
        
        # Generate dietary goals
        goals = self._generate_dietary_goals(conditions, test_values)
        
        # Generate foods to eat
        foods_to_eat = self._generate_foods_to_eat(conditions)
        
        # Generate foods to avoid
        foods_to_avoid = self._generate_foods_to_avoid(conditions)
        
        # Generate meal suggestions
        meal_suggestions = self._generate_meal_suggestions(conditions)
        
        # Generate lifestyle tips
        lifestyle_tips = self._generate_lifestyle_tips(conditions)
        
        # Generate nutritional targets
        nutritional_targets = self._generate_nutritional_targets(conditions, test_values)
        
        return {
            'conditions_detected': conditions,
            'dietary_goals': goals,
            'foods_to_eat': foods_to_eat,
            'foods_to_avoid': foods_to_avoid,
            'meal_suggestions': meal_suggestions,
            'lifestyle_tips': lifestyle_tips,
            'nutritional_targets': nutritional_targets,
            'general_notes': self._generate_general_notes(),
            'tests_analyzed': list(test_values.keys()),  # Show which tests were used
            'report_summary': self._generate_report_summary(test_values)
        }
    
    def _extract_test_values(self, parsed_data):
        """
        Extract test values - UNIVERSAL for all test types
        """
        test_values = {}
        
        if not parsed_data or 'all_results' not in parsed_data:
            return test_values
        
        tests = parsed_data.get('all_results', [])
        
        # Define mapping for ALL possible test names
        test_mapping = {
            # Lipid Profile
            'total cholesterol': 'total_cholesterol',
            'cholesterol total': 'total_cholesterol',
            'hdl cholesterol': 'hdl',
            'hdl': 'hdl',
            'ldl cholesterol': 'ldl',
            'ldl': 'ldl',
            'triglycerides': 'triglycerides',
            'vldl cholesterol': 'vldl',
            'vldl': 'vldl',
            
            # Diabetes
            'hba1c': 'hba1c',
            'glycosylated hemoglobin': 'hba1c',
            'hemoglobin a1c': 'hba1c',
            'glucose': 'glucose',
            'fasting glucose': 'fasting_glucose',
            'blood glucose': 'glucose',
            
            # Liver Function
            'sgot': 'sgot',
            'ast': 'sgot',
            'aspartate aminotransferase': 'sgot',
            'sgpt': 'sgpt',
            'alt': 'sgpt',
            'alanine transaminase': 'sgpt',
            'alkaline phosphatase': 'alp',
            'alp': 'alp',
            'bilirubin - total': 'bilirubin_total',
            'bilirubin total': 'bilirubin_total',
            'total bilirubin': 'bilirubin_total',
            'bilirubin -direct': 'bilirubin_direct',
            'bilirubin direct': 'bilirubin_direct',
            'direct bilirubin': 'bilirubin_direct',
            'ggt': 'ggt',
            'gamma glutamyl transferase': 'ggt',
            'albumin': 'albumin',
            'serum albumin': 'albumin',
            'albumin - serum': 'albumin',
            'protein - total': 'total_protein',
            'total protein': 'total_protein',
            
            # Thyroid Function
            'tsh': 'tsh',
            'thyroid stimulating hormone': 'tsh',
            'total triiodothyronine': 't3',
            't3': 't3',
            'triiodothyronine': 't3',
            'total thyroxine': 't4',
            't4': 't4',
            'thyroxine': 't4',
            'free t3': 'free_t3',
            'free t4': 'free_t4',
            
            # Kidney Function
            'creatinine': 'creatinine',
            'serum creatinine': 'creatinine',
            'urea': 'urea',
            'blood urea nitrogen': 'urea',
            'bun': 'bun',
            'uric acid': 'uric_acid',
            
            # CBC
            'hemoglobin': 'hemoglobin',
            'hb': 'hemoglobin',
            'wbc': 'wbc',
            'white blood cells': 'wbc',
            'platelets': 'platelets',
            
            # Vitamins & Minerals
            'iron': 'iron',
            'serum iron': 'iron',
            'ferritin': 'ferritin',
            'vitamin d': 'vitamin_d',
            'vitamin d3': 'vitamin_d',
            'vitamin b12': 'vitamin_b12',
            'calcium': 'calcium',
            'sodium': 'sodium',
            'potassium': 'potassium',
        }
        
        for test in tests:
            test_name = str(test.get('term', '')).lower().strip()
            test_value = test.get('value')
            
            if test_value is None or test_name == '':
                continue
            
            # Convert to float
            try:
                if isinstance(test_value, str):
                    test_value = float(test_value.strip().replace(',', ''))
                else:
                    test_value = float(test_value)
            except:
                continue
            
            # Map test name to standard key
            for pattern, standard_name in test_mapping.items():
                if pattern in test_name:
                    test_values[standard_name] = test_value
                    break
        
        return test_values
    
    def _identify_conditions(self, test_values):
        """
        Identify conditions ONLY from tests that actually exist
        ✅ KEY FIX: Only check tests that are in test_values
        """
        conditions = []
        
        # ============================================
        # LIPID PROFILE CONDITIONS
        # ============================================
        
        # High Total Cholesterol (ONLY if test exists)
        if 'total_cholesterol' in test_values:
            if test_values['total_cholesterol'] >= 200:
                conditions.append('high_cholesterol')
        
        # High LDL (ONLY if test exists)
        if 'ldl' in test_values:
            if test_values['ldl'] >= 130:
                conditions.append('high_ldl')
        
        # Low HDL (ONLY if test exists)
        if 'hdl' in test_values:
            if test_values['hdl'] < 40:
                conditions.append('low_hdl')
        
        # High Triglycerides (ONLY if test exists)
        if 'triglycerides' in test_values:
            if test_values['triglycerides'] >= 150:
                conditions.append('high_triglycerides')
        
        # ============================================
        # DIABETES CONDITIONS
        # ============================================
        
        # Check HbA1c (ONLY if test exists)
        if 'hba1c' in test_values:
            hba1c = test_values['hba1c']
            if hba1c >= 6.5:
                conditions.append('diabetes')
            elif hba1c >= 5.7:
                conditions.append('prediabetes')
        
        # Check Glucose (ONLY if test exists)
        glucose = test_values.get('fasting_glucose') or test_values.get('glucose')
        if glucose:
            if glucose >= 126:
                if 'diabetes' not in conditions:
                    conditions.append('diabetes')
            elif glucose >= 100:
                if 'prediabetes' not in conditions and 'diabetes' not in conditions:
                    conditions.append('prediabetes')
        
        # ============================================
        # LIVER CONDITIONS (Only flag if SIGNIFICANTLY abnormal)
        # ============================================
        
        liver_abnormal = False
        
        # SGOT/AST - Use upper limit with buffer
        if 'sgot' in test_values:
            if test_values['sgot'] > 60:  # Significantly elevated (normal <48)
                liver_abnormal = True
        
        # SGPT/ALT - More specific to liver, use stricter limit
        if 'sgpt' in test_values:
            if test_values['sgpt'] > 55:  # Significantly elevated (normal <45)
                liver_abnormal = True
        
        # Bilirubin - Only if clearly high
        if 'bilirubin_total' in test_values:
            if test_values['bilirubin_total'] > 1.5:  # Clearly elevated (normal <1.2)
                liver_abnormal = True
        
        # GGT - Sensitive marker
        if 'ggt' in test_values:
            if test_values['ggt'] > 80:  # Significantly elevated (normal <65)
                liver_abnormal = True
        
        # Albumin - Low indicates poor liver function
        if 'albumin' in test_values:
            if test_values['albumin'] < 3.2:  # Clearly low (normal >3.5)
                liver_abnormal = True
        
        # ALP - Very high indicates bile duct issues
        if 'alp' in test_values:
            if test_values['alp'] > 150:  # Significantly elevated (normal <130)
                liver_abnormal = True
        
        if liver_abnormal:
            conditions.append('liver_concern')
        
        # ============================================
        # THYROID CONDITIONS
        # ============================================
        
        if 'tsh' in test_values:
            tsh = test_values['tsh']
            if tsh > 4.5:
                conditions.append('hypothyroid')
            elif tsh < 0.4:
                conditions.append('hyperthyroid')
        
        # ============================================
        # KIDNEY CONDITIONS
        # ============================================
        
        if 'creatinine' in test_values and test_values['creatinine'] > 1.3:
            conditions.append('kidney_concern')
        
        if 'urea' in test_values and test_values['urea'] > 24:
            conditions.append('kidney_concern')
        
        if 'bun' in test_values and test_values['bun'] > 24:
            conditions.append('kidney_concern')
        
        # ============================================
        # ANEMIA / IRON CONDITIONS
        # ============================================
        
        if 'hemoglobin' in test_values and test_values['hemoglobin'] < 12.0:
            conditions.append('anemia')
        
        if 'iron' in test_values and test_values['iron'] < 50:
            conditions.append('low_iron')
        
        if 'ferritin' in test_values and test_values['ferritin'] < 11:
            conditions.append('low_iron')
        
        # ============================================
        # VITAMIN DEFICIENCIES
        # ============================================
        
        if 'vitamin_d' in test_values and test_values['vitamin_d'] < 20:
            conditions.append('vitamin_d_deficiency')
        
        if 'vitamin_b12' in test_values and test_values['vitamin_b12'] < 200:
            conditions.append('vitamin_b12_deficiency')
        
        # ============================================
        # GOUT / URIC ACID
        # ============================================
        
        if 'uric_acid' in test_values and test_values['uric_acid'] > 7:
            conditions.append('high_uric_acid')
        
        # ============================================
        # IF NO CONDITIONS, MARK AS HEALTHY
        # ============================================
        
        if not conditions:
            conditions.append('all_normal')
        
        return conditions
    
    def _generate_report_summary(self, test_values):
        """Generate a summary of what was analyzed"""
        categories = {
            'Lipid Profile': [],
            'Diabetes Markers': [],
            'Liver Function': [],
            'Thyroid Function': [],
            'Kidney Function': [],
            'Blood Count': [],
            'Vitamins & Minerals': []
        }
        
        # Categorize tests
        lipid_tests = ['total_cholesterol', 'hdl', 'ldl', 'triglycerides', 'vldl']
        diabetes_tests = ['hba1c', 'glucose', 'fasting_glucose']
        liver_tests = ['sgot', 'sgpt', 'alp', 'bilirubin_total', 'bilirubin_direct', 'ggt', 'albumin', 'total_protein']
        thyroid_tests = ['tsh', 't3', 't4', 'free_t3', 'free_t4']
        kidney_tests = ['creatinine', 'urea', 'bun', 'uric_acid']
        blood_tests = ['hemoglobin', 'wbc', 'platelets']
        vitamin_tests = ['iron', 'ferritin', 'vitamin_d', 'vitamin_b12', 'calcium', 'sodium', 'potassium']
        
        for test_name in test_values.keys():
            if test_name in lipid_tests:
                categories['Lipid Profile'].append(test_name)
            elif test_name in diabetes_tests:
                categories['Diabetes Markers'].append(test_name)
            elif test_name in liver_tests:
                categories['Liver Function'].append(test_name)
            elif test_name in thyroid_tests:
                categories['Thyroid Function'].append(test_name)
            elif test_name in kidney_tests:
                categories['Kidney Function'].append(test_name)
            elif test_name in blood_tests:
                categories['Blood Count'].append(test_name)
            elif test_name in vitamin_tests:
                categories['Vitamins & Minerals'].append(test_name)
        
        # Remove empty categories
        categories = {k: v for k, v in categories.items() if v}
        
        return categories
    
    # ============================================
    # REST OF THE FUNCTIONS (goals, foods, meals, etc.)
    # ============================================
    # Keep your existing functions but add support for new conditions:
    # - liver_concern
    # - hypothyroid
    # - hyperthyroid
    # - all_normal
    
    def _generate_dietary_goals(self, conditions, test_values):
        """Generate dietary goals based on conditions"""
        goals = []
        
        if 'all_normal' in conditions:
            goals.append("✅ All test results are within normal ranges!")
            goals.append("🎯 Maintain current healthy status through balanced nutrition")
            goals.append("🛡️ Prevent future health issues through preventive diet")
            return goals
        
        if 'high_cholesterol' in conditions or 'high_ldl' in conditions:
            goals.append("Lower LDL (bad) cholesterol through diet")
            goals.append("Reduce saturated fat and trans fat intake")
        
        if 'low_hdl' in conditions:
            goals.append("Increase HDL (good) cholesterol naturally")
        
        if 'high_triglycerides' in conditions:
            goals.append("Reduce triglyceride levels through diet")
            goals.append("Limit simple sugars and refined carbohydrates")
        
        if 'diabetes' in conditions:
            goals.append("Manage blood sugar levels through diet")
            goals.append("Control carbohydrate intake and portion sizes")
            goals.append("Choose low glycemic index foods")
        
        if 'prediabetes' in conditions:
            goals.append("Prevent progression to diabetes")
            goals.append("Achieve modest weight loss (5-10% if overweight)")
            goals.append("Improve insulin sensitivity through diet")
        
        if 'liver_concern' in conditions:
            goals.append("Support liver health and function")
            goals.append("Reduce inflammation through anti-inflammatory foods")
            goals.append("Eliminate alcohol and hepatotoxic substances")
        
        if 'hypothyroid' in conditions:
            goals.append("Support thyroid function through nutrition")
            goals.append("Ensure adequate iodine and selenium intake")
            goals.append("Maintain healthy metabolism")
        
        if 'hyperthyroid' in conditions:
            goals.append("Support thyroid regulation")
            goals.append("Reduce metabolic stress through balanced nutrition")
        
        if 'anemia' in conditions or 'low_iron' in conditions:
            goals.append("Increase iron levels through diet")
            goals.append("Improve iron absorption with Vitamin C")
        
        if 'kidney_concern' in conditions:
            goals.append("Support kidney health through diet")
            goals.append("Control protein and sodium intake")
        
        if 'high_uric_acid' in conditions:
            goals.append("Lower uric acid levels to prevent gout")
            goals.append("Reduce purine-rich foods")
        
        if 'vitamin_d_deficiency' in conditions:
            goals.append("Increase Vitamin D through diet and sunlight")
        
        if 'vitamin_b12_deficiency' in conditions:
            goals.append("Increase Vitamin B12 through diet")
        
        return goals
    
    # [CONTINUE WITH OTHER FUNCTIONS - I'll add liver/thyroid support]
    
    def _generate_foods_to_eat(self, conditions):
        """Generate foods to eat - UPDATED with liver & thyroid support"""
        foods = {
            'proteins': [],
            'vegetables': [],
            'fruits': [],
            'grains': [],
            'healthy_fats': [],
            'beverages': [],
            'supplements': []
        }
        
        # ALL NORMAL
        if 'all_normal' in conditions:
            foods['proteins'] = [
                "✅ Variety of lean proteins (fish, chicken, eggs)",
                "✅ Plant proteins (beans, lentils, tofu)",
                "✅ Greek yogurt and low-fat dairy"
            ]
            foods['vegetables'] = [
                "✅ Rainbow of colorful vegetables daily",
                "✅ Leafy greens (spinach, kale)",
                "✅ Cruciferous vegetables (broccoli, cauliflower)"
            ]
            foods['fruits'] = [
                "✅ 2-3 servings of fresh fruits daily",
                "✅ Berries, citrus fruits",
                "✅ Seasonal fruits"
            ]
            foods['grains'] = [
                "✅ Whole grains (quinoa, brown rice)",
                "✅ Steel-cut oats",
                "✅ Whole wheat bread"
            ]
            foods['healthy_fats'] = [
                "✅ Nuts and seeds",
                "✅ Olive oil",
                "✅ Avocado"
            ]
            foods['beverages'] = [
                "✅ 8 glasses of water daily",
                "✅ Green tea",
                "✅ Herbal teas"
            ]
            return foods
        
        # LIVER CONCERN - NEW!
        if 'liver_concern' in conditions:
            foods['proteins'].extend([
                "Lean fish (salmon, cod)",
                "Skinless chicken breast",
                "Plant proteins (lentils, beans)",
                "Egg whites"
            ])
            foods['vegetables'].extend([
                "Leafy greens (spinach, arugula) - Support detox",
                "Cruciferous vegetables (broccoli, cauliflower) - Liver detox",
                "Beets - Support liver function",
                "Carrots, sweet potatoes"
            ])
            foods['fruits'].extend([
                "Berries (antioxidants for liver)",
                "Grapefruit - Liver cleansing",
                "Apples - Pectin helps detox",
                "Lemons - Support bile production"
            ])
            foods['grains'].extend([
                "Oats - Soluble fiber",
                "Quinoa",
                "Brown rice"
            ])
            foods['healthy_fats'].extend([
                "Walnuts - Omega-3 for liver",
                "Flaxseeds",
                "Olive oil (extra virgin)"
            ])
            foods['beverages'].extend([
                "ZERO ALCOHOL - Critical!",
                "Green tea - Antioxidants",
                "Lemon water",
                "Turmeric tea - Anti-inflammatory"
            ])
            foods['supplements'].append("Milk thistle may support liver (consult doctor)")
        
        # HYPOTHYROID - NEW!
        if 'hypothyroid' in conditions:
            foods['proteins'].extend([
                "Fish and seafood (iodine)",
                "Eggs (selenium)",
                "Chicken, turkey"
            ])
            foods['vegetables'].extend([
                "Seaweed (nori, kelp) - Natural iodine",
                "Spinach, Swiss chard",
                "Mushrooms - Selenium"
            ])
            foods['fruits'].extend([
                "Berries - Antioxidants",
                "Bananas - Selenium"
            ])
            foods['grains'].extend([
                "Quinoa",
                "Brown rice",
                "Oats"
            ])
            foods['healthy_fats'].extend([
                "Brazil nuts - High selenium (2-3 per day)",
                "Chia seeds",
                "Olive oil"
            ])
            foods['supplements'].extend([
                "Iodized salt (in moderation)",
                "Selenium supplement if needed"
            ])
            foods['beverages'].append("Avoid excessive soy milk")
        
        # HYPERTHYROID - NEW!
        if 'hyperthyroid' in conditions:
            foods['proteins'].extend([
                "Lean chicken, turkey",
                "Eggs",
                "Low-fat dairy"
            ])
            foods['vegetables'].extend([
                "Cruciferous vegetables (broccoli, cabbage) - May help slow thyroid",
                "Spinach, kale",
                "Bell peppers"
            ])
            foods['fruits'].extend([
                "Berries",
                "Peaches, pears"
            ])
            foods['grains'].extend([
                "Whole grains",
                "Oats"
            ])
            foods['beverages'].extend([
                "Avoid caffeine - Increases heart rate",
                "Herbal teas (chamomile)",
                "Plenty of water"
            ])
        
        # [ADD YOUR EXISTING CONDITIONS - Cholesterol, Diabetes, Anemia, etc.]
        # (Keep all your existing code for these)
        
        return foods
    
    def _generate_foods_to_avoid(self, conditions):
        """Generate foods to avoid - UPDATED"""
        avoid = {
            'high_risk': [],
            'moderate_risk': [],
            'limit_portions': []
        }
        
        if 'all_normal' in conditions:
            avoid['high_risk'] = [
                "❌ Trans fats and hydrogenated oils",
                "❌ Excessive processed foods",
                "❌ Too much added sugar"
            ]
            avoid['moderate_risk'] = [
                "⚠️ Excessive alcohol (limit to moderate)",
                "⚠️ High sodium foods"
            ]
            return avoid
        
        # LIVER CONCERN
        if 'liver_concern' in conditions:
            avoid['high_risk'].extend([
                "❌ ALCOHOL - Absolutely avoid!",
                "❌ Fried foods, fast food",
                "❌ Processed meats",
                "❌ High-fat dairy",
                "❌ Excessive Tylenol/acetaminophen"
            ])
            avoid['moderate_risk'].extend([
                "⚠️ Red meat (limit to once per week)",
                "⚠️ High-sugar foods"
            ])
        
        # HYPOTHYROID
        if 'hypothyroid' in conditions:
            avoid['high_risk'].extend([
                "❌ Excessive soy products (interfere with thyroid meds)",
                "❌ Raw cruciferous vegetables in large amounts"
            ])
            avoid['moderate_risk'].extend([
                "⚠️ Gluten (may interfere in some people)",
                "⚠️ Processed foods"
            ])
        
        # HYPERTHYROID
        if 'hyperthyroid' in conditions:
            avoid['high_risk'].extend([
                "❌ Iodine-rich foods (seaweed, kelp)",
                "❌ Caffeine (coffee, energy drinks)",
                "❌ Alcohol"
            ])
        
        # [KEEP YOUR EXISTING AVOIDANCE LISTS FOR OTHER CONDITIONS]
        
        return avoid
    
    def _generate_meal_suggestions(self, conditions):
        """Generate meal suggestions - UPDATED"""
        meals = {
            'breakfast': [],
            'mid_morning': [],
            'lunch': [],
            'evening_snack': [],
            'dinner': []
        }
        
        if 'all_normal' in conditions:
            meals['breakfast'] = [
                "✅ Any balanced breakfast with protein and fiber",
                "Examples: Oats with fruits, eggs with toast, yogurt parfait"
            ]
            meals['lunch'] = [
                "✅ Balanced plate: 1/2 vegetables, 1/4 protein, 1/4 whole grains"
            ]
            meals['dinner'] = [
                "✅ Similar to lunch, lighter portions",
                "Include vegetables and lean protein"
            ]
            return meals
        
        # LIVER CONCERN
        if 'liver_concern' in conditions:
            meals['breakfast'].extend([
                "Oatmeal with berries and walnuts",
                "Vegetable omelet (egg whites) with whole wheat toast",
                "Green smoothie with spinach, apple, lemon"
            ])
            meals['lunch'].extend([
                "Grilled fish with steamed broccoli",
                "Lentil soup with side salad",
                "Chicken breast with quinoa and vegetables"
            ])
            meals['dinner'].extend([
                "Baked salmon with roasted vegetables",
                "Vegetable stir-fry with brown rice",
                "Grilled chicken with beet salad"
            ])
        
        # THYROID CONDITIONS
        if 'hypothyroid' in conditions or 'hyperthyroid' in conditions:
            meals['breakfast'].extend([
                "Scrambled eggs with spinach",
                "Greek yogurt with berries and Brazil nuts (2-3)",
                "Oatmeal with banana"
            ])
            meals['lunch'].extend([
                "Grilled fish with vegetables",
                "Chicken with quinoa and salad",
                "Egg salad with mixed greens"
            ])
            meals['dinner'].extend([
                "Baked fish with steamed vegetables",
                "Turkey with brown rice",
                "Vegetable curry with small portion rice"
            ])
        
        # [KEEP YOUR EXISTING MEAL SUGGESTIONS]
        
        return meals
    
    def _generate_lifestyle_tips(self, conditions):
        """Generate lifestyle tips"""
        tips = []
        
        # Universal tips
        tips.extend([
            "💧 Drink 8-10 glasses of water daily",
            "🚶‍♂️ Walk for 30 minutes after meals",
            "😴 Get 7-8 hours of quality sleep",
            "🧘‍♀️ Practice stress management (yoga, meditation)"
        ])
        
        if 'liver_concern' in conditions:
            tips.extend([
                "🚫 ZERO ALCOHOL - Absolutely critical for liver recovery",
                "💊 Avoid unnecessary medications",
                "⚖️ Maintain healthy body weight",
                "🩺 Regular liver function tests every 3 months"
            ])
        
        if 'hypothyroid' in conditions or 'hyperthyroid' in conditions:
            tips.extend([
                "💊 Take thyroid medication consistently (if prescribed)",
                "📅 Regular thyroid function tests",
                "😴 Prioritize quality sleep",
                "🧘 Manage stress - affects thyroid"
            ])
        
        # [KEEP YOUR EXISTING LIFESTYLE TIPS]
        
        return tips
    
    def _generate_nutritional_targets(self, conditions, test_values):
        """Generate nutritional targets"""
        targets = {}
        
        if 'all_normal' in conditions:
            targets['daily_calories'] = "Maintain current intake - appears balanced"
            targets['carbohydrates'] = "45-55% of total calories"
            targets['protein'] = "15-20% of total calories"
            targets['fats'] = "25-30% of total calories (focus on unsaturated)"
            targets['fiber'] = "25-30g per day"
            targets['sodium'] = "Less than 2300mg per day"
            targets['water'] = "8-10 glasses (2-2.5 liters) per day"
            return targets
        
        # [KEEP YOUR EXISTING NUTRITIONAL TARGETS LOGIC]
        
        targets['daily_calories'] = "1800-2200 kcal (adjust based on activity and weight goals)"
        targets['fiber'] = "25-30g per day from vegetables, fruits, whole grains"
        targets['water'] = "8-10 glasses (2-2.5 liters) per day"
        
        return targets
    
    def _generate_general_notes(self):
        """Generate general notes"""
        return [
            "⚠️ These recommendations are based on your test results",
            "👨‍⚕️ Always consult your doctor before making major dietary changes",
            "📊 Individual needs vary based on age, weight, activity level, and medications",
            "🔄 Retest your health markers after 3-6 months to track progress",
            "💪 Consistency is key - small daily improvements lead to big results",
            "🤝 Consider consulting a registered dietitian for personalized planning"
        ]


# Wrapper function for routes
def generate_diet_recommendations(parsed_data):
    """
    Universal diet recommender - works for ALL report types
    
    Args:
        parsed_data: Parsed medical report data
        
    Returns:
        Complete diet plan
    """
    recommender = UniversalDietRecommender()
    return recommender.generate_diet_plan(parsed_data)