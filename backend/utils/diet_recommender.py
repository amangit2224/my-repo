"""
Diet Recommender System
Provides personalized dietary recommendations based on medical test results
Evidence-based and medically sound guidelines
"""

class DietRecommender:
    """
    Generates personalized diet plans based on health markers
    """
    
    def __init__(self):
        """Initialize the diet recommender"""
        pass
    
    def generate_diet_plan(self, parsed_data):
        """
        Generate a comprehensive diet plan based on parsed medical data
        
        Args:
            parsed_data: Dictionary containing test results and health markers
            
        Returns:
            Dictionary with complete diet recommendations
        """
        
        # Extract test values
        test_values = self._extract_test_values(parsed_data)
        
        # Identify health conditions
        conditions = self._identify_conditions(test_values)
        
        # Generate dietary goals
        goals = self._generate_dietary_goals(conditions)
        
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
            'general_notes': self._generate_general_notes()
        }
    
    def _extract_test_values(self, parsed_data):
        """Extract relevant test values from parsed data"""
        test_values = {}
        
        if not parsed_data or 'all_results' not in parsed_data:
            return test_values
        
        tests = parsed_data.get('all_results', [])
        
        for test in tests:
            test_name = str(test.get('term', '')).lower()
            test_value = test.get('value')
            
            if test_value is None:
                continue
            
            # Convert to float
            try:
                if isinstance(test_value, str):
                    test_value = float(test_value.strip().replace(',', ''))
                else:
                    test_value = float(test_value)
            except:
                continue
            
            # Map test names
            if 'total' in test_name and 'cholesterol' in test_name:
                test_values['total_cholesterol'] = test_value
            elif 'hdl' in test_name:
                test_values['hdl'] = test_value
            elif 'ldl' in test_name:
                test_values['ldl'] = test_value
            elif 'triglyceride' in test_name:
                test_values['triglycerides'] = test_value
            elif 'hba1c' in test_name or 'a1c' in test_name:
                test_values['hba1c'] = test_value
            elif 'glucose' in test_name and 'fasting' not in test_name:
                test_values['glucose'] = test_value
            elif 'fasting' in test_name and 'glucose' in test_name:
                test_values['fasting_glucose'] = test_value
            elif 'hemoglobin' in test_name and 'a1c' not in test_name:
                test_values['hemoglobin'] = test_value
            elif 'creatinine' in test_name:
                test_values['creatinine'] = test_value
            elif 'urea' in test_name or 'bun' in test_name:
                test_values['urea'] = test_value
            elif 'iron' in test_name:
                test_values['iron'] = test_value
            elif 'ferritin' in test_name:
                test_values['ferritin'] = test_value
            elif 'vitamin' in test_name and ('d' in test_name or 'd3' in test_name):
                test_values['vitamin_d'] = test_value
            elif 'vitamin' in test_name and 'b12' in test_name:
                test_values['vitamin_b12'] = test_value
            elif 'calcium' in test_name:
                test_values['calcium'] = test_value
            elif 'sodium' in test_name:
                test_values['sodium'] = test_value
            elif 'potassium' in test_name:
                test_values['potassium'] = test_value
            elif 'uric' in test_name and 'acid' in test_name:
                test_values['uric_acid'] = test_value
        
        return test_values
    
    def _identify_conditions(self, test_values):
        """Identify health conditions based on test values"""
        conditions = []
        
        # High Cholesterol
        if test_values.get('total_cholesterol', 0) >= 200:
            conditions.append('high_cholesterol')
        
        # High LDL
        if test_values.get('ldl', 0) >= 130:
            conditions.append('high_ldl')
        
        # Low HDL
        if test_values.get('hdl', 0) < 40:
            conditions.append('low_hdl')
        
        # High Triglycerides
        if test_values.get('triglycerides', 0) >= 150:
            conditions.append('high_triglycerides')
        
        # Diabetes/Prediabetes
        hba1c = test_values.get('hba1c', 0)
        fasting_glucose = test_values.get('fasting_glucose', 0) or test_values.get('glucose', 0)
        
        if hba1c >= 6.5 or fasting_glucose >= 126:
            conditions.append('diabetes')
        elif hba1c >= 5.7 or fasting_glucose >= 100:
            conditions.append('prediabetes')
        
        # Anemia (Low Hemoglobin)
        hemoglobin = test_values.get('hemoglobin', 0)
        if hemoglobin > 0 and hemoglobin < 12:  # Low for women
            conditions.append('anemia')
        
        # Low Iron
        if test_values.get('iron', 0) < 50:
            conditions.append('low_iron')
        
        # Kidney Issues
        if test_values.get('creatinine', 0) > 1.3 or test_values.get('urea', 0) > 45:
            conditions.append('kidney_concern')
        
        # High Uric Acid (Gout risk)
        if test_values.get('uric_acid', 0) > 7:
            conditions.append('high_uric_acid')
        
        # Vitamin D Deficiency
        if test_values.get('vitamin_d', 0) < 20:
            conditions.append('vitamin_d_deficiency')
        
        # Vitamin B12 Deficiency
        if test_values.get('vitamin_b12', 0) < 200:
            conditions.append('vitamin_b12_deficiency')
        
        # If no specific conditions, mark as healthy
        if not conditions:
            conditions.append('healthy')
        
        return conditions
    
    def _generate_dietary_goals(self, conditions):
        """Generate dietary goals based on conditions"""
        goals = []
        
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
        
        if 'healthy' in conditions:
            goals.append("Maintain current healthy status")
            goals.append("Prevent future health issues through balanced diet")
            goals.append("Support overall wellness and energy levels")
        
        return goals
    
    def _generate_foods_to_eat(self, conditions):
        """Generate foods to eat based on conditions"""
        foods = {
            'proteins': [],
            'vegetables': [],
            'fruits': [],
            'grains': [],
            'healthy_fats': [],
            'beverages': [],
            'supplements': []
        }
        
        # Cholesterol Management
        if 'high_cholesterol' in conditions or 'high_ldl' in conditions or 'high_triglycerides' in conditions:
            foods['proteins'].extend([
                "Fatty fish (salmon, mackerel, sardines) - Rich in Omega-3",
                "Legumes (lentils, chickpeas, beans) - High in soluble fiber",
                "Skinless chicken breast",
                "Egg whites (limit whole eggs to 3-4 per week)"
            ])
            foods['vegetables'].extend([
                "Oats and oat bran - Soluble fiber to lower LDL",
                "Leafy greens (spinach, kale, collards)",
                "Broccoli, Brussels sprouts",
                "Bell peppers, tomatoes"
            ])
            foods['fruits'].extend([
                "Apples - Pectin helps lower cholesterol",
                "Berries (blueberries, strawberries)",
                "Citrus fruits (oranges, grapefruit)",
                "Avocado - Monounsaturated fats"
            ])
            foods['grains'].extend([
                "Steel-cut oats or oatmeal",
                "Barley",
                "Quinoa",
                "Whole wheat bread (limited)"
            ])
            foods['healthy_fats'].extend([
                "Almonds, walnuts (handful daily)",
                "Flaxseeds, chia seeds",
                "Olive oil (extra virgin)",
                "Avocado"
            ])
            foods['beverages'].append("Green tea - Antioxidants help lower cholesterol")
        
        # Low HDL
        if 'low_hdl' in conditions:
            foods['healthy_fats'].extend([
                "Nuts - especially almonds and walnuts",
                "Fatty fish - 2-3 times per week",
                "Olive oil - use liberally"
            ])
            foods['supplements'].append("Consider Omega-3 supplements (consult doctor)")
        
        # Diabetes/Prediabetes
        if 'diabetes' in conditions or 'prediabetes' in conditions:
            foods['proteins'].extend([
                "Lean fish and poultry",
                "Greek yogurt (unsweetened)",
                "Tofu and tempeh",
                "Eggs (moderate)"
            ])
            foods['vegetables'].extend([
                "Non-starchy vegetables (all leafy greens)",
                "Cauliflower, cabbage, zucchini",
                "Green beans, asparagus",
                "Bitter gourd (karela) - Helps blood sugar"
            ])
            foods['fruits'].extend([
                "Berries (low glycemic)",
                "Cherries",
                "Apples with skin",
                "Pears (limit portions to 1 small fruit)"
            ])
            foods['grains'].extend([
                "Quinoa",
                "Brown rice (small portions)",
                "Whole grain bread (1-2 slices max)",
                "Steel-cut oats"
            ])
            foods['beverages'].extend([
                "Water with cinnamon - May help blood sugar",
                "Herbal teas (unsweetened)",
                "Buttermilk (unsweetened)"
            ])
        
        # Anemia / Low Iron
        if 'anemia' in conditions or 'low_iron' in conditions:
            foods['proteins'].extend([
                "Lean red meat (2-3 times per week)",
                "Chicken liver (occasional)",
                "Fish and shellfish",
                "Eggs"
            ])
            foods['vegetables'].extend([
                "Spinach, kale (cooked)",
                "Beets",
                "Broccoli",
                "Sweet potatoes"
            ])
            foods['fruits'].extend([
                "Pomegranate - Natural iron source",
                "Dried apricots, raisins",
                "Citrus fruits (Vitamin C aids iron absorption)",
                "Strawberries"
            ])
            foods['grains'].extend([
                "Iron-fortified cereals",
                "Whole wheat bread",
                "Quinoa"
            ])
            foods['supplements'].append("Vitamin C-rich foods with iron sources")
            foods['beverages'].append("Avoid tea/coffee with meals (inhibits iron absorption)")
        
        # Kidney Concern
        if 'kidney_concern' in conditions:
            foods['proteins'].extend([
                "Small portions of lean fish",
                "Egg whites",
                "Limited chicken (3-4 oz per meal)"
            ])
            foods['vegetables'].extend([
                "Cabbage, cauliflower",
                "Bell peppers",
                "Onions, garlic",
                "Radishes"
            ])
            foods['fruits'].extend([
                "Apples, berries",
                "Grapes",
                "Pineapple",
                "Cranberries"
            ])
            foods['grains'].extend([
                "White rice (easier on kidneys than brown)",
                "White bread",
                "Pasta (moderate)"
            ])
            foods['beverages'].extend([
                "Adequate water (as per doctor's advice)",
                "Limit to 6-8 glasses if advised"
            ])
        
        # High Uric Acid
        if 'high_uric_acid' in conditions:
            foods['proteins'].extend([
                "Eggs",
                "Low-fat dairy",
                "Tofu (moderate)"
            ])
            foods['vegetables'].extend([
                "Most vegetables are safe",
                "Cherries - Help lower uric acid"
            ])
            foods['beverages'].extend([
                "Plenty of water (8-10 glasses)",
                "Coffee (may help lower uric acid)",
                "Low-fat milk"
            ])
        
        # Vitamin D Deficiency
        if 'vitamin_d_deficiency' in conditions:
            foods['proteins'].extend([
                "Fatty fish (salmon, tuna, mackerel)",
                "Egg yolks",
                "Fortified milk"
            ])
            foods['supplements'].append("Vitamin D3 supplement (1000-2000 IU daily)")
            foods['beverages'].append("Fortified plant-based milk")
        
        # Vitamin B12 Deficiency
        if 'vitamin_b12_deficiency' in conditions:
            foods['proteins'].extend([
                "Salmon, trout, tuna",
                "Lean beef",
                "Eggs",
                "Fortified nutritional yeast"
            ])
            foods['beverages'].append("Fortified plant-based milk")
            foods['supplements'].append("B12 supplement if vegetarian/vegan")
        
        # Healthy baseline
        if 'healthy' in conditions:
            foods['proteins'] = [
                "Variety of lean proteins (fish, chicken, eggs)",
                "Plant proteins (beans, lentils, tofu)",
                "Greek yogurt"
            ]
            foods['vegetables'] = [
                "Rainbow of vegetables daily",
                "Leafy greens",
                "Cruciferous vegetables"
            ]
            foods['fruits'] = [
                "2-3 servings of fresh fruits daily",
                "Berries, citrus fruits",
                "Seasonal fruits"
            ]
            foods['grains'] = [
                "Whole grains (quinoa, brown rice)",
                "Oats",
                "Whole wheat products"
            ]
            foods['healthy_fats'] = [
                "Nuts and seeds",
                "Olive oil",
                "Avocado"
            ]
            foods['beverages'] = [
                "8 glasses of water daily",
                "Green tea",
                "Herbal teas"
            ]
        
        return foods
    
    def _generate_foods_to_avoid(self, conditions):
        """Generate foods to avoid based on conditions"""
        avoid = {
            'high_risk': [],
            'moderate_risk': [],
            'limit_portions': []
        }
        
        # Cholesterol Issues
        if 'high_cholesterol' in conditions or 'high_ldl' in conditions:
            avoid['high_risk'].extend([
                "Red meat (beef, pork, lamb) - High saturated fat",
                "Full-fat dairy (butter, cheese, cream)",
                "Fried foods and fast food",
                "Coconut oil, palm oil",
                "Processed meats (bacon, sausages, salami)"
            ])
            avoid['moderate_risk'].extend([
                "Egg yolks (limit to 3-4 per week)",
                "Shrimp and shellfish (occasional only)"
            ])
            avoid['limit_portions'].extend([
                "Baked goods with trans fats",
                "Pastries, cakes, cookies"
            ])
        
        # High Triglycerides
        if 'high_triglycerides' in conditions:
            avoid['high_risk'].extend([
                "Sugary drinks (soda, fruit juices)",
                "White bread, white rice",
                "Sweets and candies",
                "Alcohol (especially beer)",
                "High-fructose corn syrup products"
            ])
            avoid['moderate_risk'].extend([
                "Dried fruits (high in sugar)",
                "Honey, maple syrup"
            ])
        
        # Diabetes/Prediabetes
        if 'diabetes' in conditions or 'prediabetes' in conditions:
            avoid['high_risk'].extend([
                "Sugary beverages and juices",
                "White bread, white rice, refined flour",
                "Pastries, cakes, cookies",
                "Sweetened breakfast cereals",
                "Candy and sweets"
            ])
            avoid['moderate_risk'].extend([
                "Potatoes (high glycemic index)",
                "Bananas (limit to half)",
                "Mangoes (small portions only)",
                "Pasta (limit portions)"
            ])
            avoid['limit_portions'].extend([
                "Whole grains (still measure portions)",
                "Fruits (max 2-3 small portions daily)"
            ])
        
        # Kidney Concern
        if 'kidney_concern' in conditions:
            avoid['high_risk'].extend([
                "High-sodium foods (chips, pickles)",
                "Processed foods",
                "Dark colas (high phosphorus)",
                "Excessive protein (>0.8g per kg body weight)"
            ])
            avoid['moderate_risk'].extend([
                "Bananas, oranges (high potassium)",
                "Tomatoes, potatoes (high potassium)",
                "Whole grains (high phosphorus)",
                "Dairy (high potassium and phosphorus)"
            ])
            avoid['limit_portions'].append("Limit salt to 1 teaspoon per day")
        
        # High Uric Acid
        if 'high_uric_acid' in conditions:
            avoid['high_risk'].extend([
                "Red meat (beef, pork, lamb)",
                "Organ meats (liver, kidney)",
                "Anchovies, sardines, mackerel",
                "Shellfish (shrimp, crab, lobster)",
                "Beer and alcohol",
                "High-fructose corn syrup"
            ])
            avoid['moderate_risk'].extend([
                "Asparagus, spinach, mushrooms (moderate purines)",
                "Cauliflower, peas"
            ])
        
        # General for most conditions
        if len(conditions) > 1 and 'healthy' not in conditions:
            avoid['high_risk'].extend([
                "Trans fats and hydrogenated oils",
                "Processed and packaged foods",
                "Excessive salt (>1 tsp daily)"
            ])
        
        # Healthy baseline
        if 'healthy' in conditions:
            avoid['high_risk'] = [
                "Trans fats and hydrogenated oils",
                "Excessive processed foods",
                "Too much added sugar"
            ]
            avoid['limit_portions'] = [
                "Moderation in everything",
                "Occasional treats are fine"
            ]
        
        return avoid
    
    def _generate_meal_suggestions(self, conditions):
        """Generate meal suggestions based on conditions"""
        meals = {
            'breakfast': [],
            'mid_morning': [],
            'lunch': [],
            'evening_snack': [],
            'dinner': []
        }
        
        # Cholesterol/Heart Health
        if 'high_cholesterol' in conditions or 'high_ldl' in conditions or 'high_triglycerides' in conditions:
            meals['breakfast'].extend([
                "Steel-cut oatmeal with berries and walnuts",
                "Greek yogurt with flaxseeds and apple slices",
                "Whole wheat toast with avocado and tomato"
            ])
            meals['lunch'].extend([
                "Grilled salmon with quinoa and steamed broccoli",
                "Chickpea salad with olive oil dressing",
                "Vegetable soup with whole grain bread"
            ])
            meals['dinner'].extend([
                "Baked fish with roasted vegetables",
                "Lentil curry with brown rice (small portion)",
                "Grilled chicken breast with mixed green salad"
            ])
        
        # Diabetes/Prediabetes
        if 'diabetes' in conditions or 'prediabetes' in conditions:
            meals['breakfast'].extend([
                "Vegetable omelet (egg whites) with whole wheat toast",
                "Greek yogurt with nuts and seeds (no sugar)",
                "Steel-cut oats with cinnamon"
            ])
            meals['mid_morning'].append("Handful of almonds or one small apple")
            meals['lunch'].extend([
                "Grilled chicken with large salad and vinaigrette",
                "Fish with non-starchy vegetables",
                "Lentil soup with side of vegetables"
            ])
            meals['evening_snack'].append("Cucumber slices with hummus")
            meals['dinner'].extend([
                "Stir-fried tofu with vegetables",
                "Grilled fish with cauliflower rice",
                "Vegetable curry with small portion quinoa"
            ])
        
        # Anemia
        if 'anemia' in conditions or 'low_iron' in conditions:
            meals['breakfast'].extend([
                "Scrambled eggs with spinach",
                "Iron-fortified cereal with milk",
                "Whole wheat toast with egg"
            ])
            meals['lunch'].extend([
                "Lean beef with dark leafy greens",
                "Chicken with beet salad",
                "Lentils with tomato (Vitamin C)"
            ])
            meals['dinner'].extend([
                "Fish with spinach and sweet potato",
                "Chicken liver curry (occasional)",
                "Egg curry with vegetables"
            ])
        
        # Kidney Concern
        if 'kidney_concern' in conditions:
            meals['breakfast'].extend([
                "Egg white omelet with peppers",
                "White toast with cucumber",
                "Small portion oatmeal"
            ])
            meals['lunch'].extend([
                "Small portion fish with cabbage",
                "Egg whites with cauliflower rice",
                "Limited chicken with low-potassium vegetables"
            ])
            meals['dinner'].extend([
                "Small portion protein with low-potassium vegetables",
                "White rice with limited vegetable curry"
            ])
        
        # Healthy
        if 'healthy' in conditions:
            meals['breakfast'] = [
                "Any balanced breakfast with protein and fiber",
                "Examples: Oats, eggs, yogurt with fruits"
            ]
            meals['lunch'] = [
                "Balanced plate: 1/2 vegetables, 1/4 protein, 1/4 whole grains",
                "Variety of cuisines are fine"
            ]
            meals['dinner'] = [
                "Similar to lunch, lighter portions",
                "Include vegetables and lean protein"
            ]
        
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
        
        if 'diabetes' in conditions or 'prediabetes' in conditions:
            tips.extend([
                "📊 Monitor blood sugar levels regularly",
                "🍽️ Eat at regular times, don't skip meals",
                "🥗 Fill half your plate with non-starchy vegetables"
            ])
        
        if 'high_cholesterol' in conditions or 'high_ldl' in conditions:
            tips.extend([
                "🏃‍♂️ Aerobic exercise 150 minutes per week",
                "🚭 Quit smoking if applicable",
                "⚖️ Maintain healthy body weight"
            ])
        
        if 'kidney_concern' in conditions:
            tips.extend([
                "🩺 Monitor blood pressure regularly",
                "💊 Take medications as prescribed",
                "📉 Track protein and sodium intake"
            ])
        
        if 'anemia' in conditions:
            tips.extend([
                "☕ Avoid tea/coffee with meals",
                "🍊 Pair iron-rich foods with Vitamin C",
                "💊 Take iron supplements as prescribed"
            ])
        
        return tips
    
    def _generate_nutritional_targets(self, conditions, test_values):
        """Generate nutritional targets"""
        targets = {}
        
        # Calories (general recommendation)
        targets['daily_calories'] = "1800-2200 kcal (adjust based on activity level and weight goals)"
        
        # Macronutrients
        if 'diabetes' in conditions or 'prediabetes' in conditions:
            targets['carbohydrates'] = "45-50% of total calories (focus on complex carbs)"
            targets['protein'] = "20-25% of total calories"
            targets['fats'] = "25-30% of total calories (mostly unsaturated)"
        elif 'kidney_concern' in conditions:
            targets['protein'] = "0.8g per kg body weight (limited)"
            targets['sodium'] = "Less than 2000mg per day"
            targets['potassium'] = "Monitor and limit high-potassium foods"
        else:
            targets['carbohydrates'] = "45-55% of total calories"
            targets['protein'] = "15-20% of total calories"
            targets['fats'] = "25-30% of total calories"
        
        # Cholesterol
        if 'high_cholesterol' in conditions or 'high_ldl' in conditions:
            targets['cholesterol'] = "Less than 200mg per day"
            targets['saturated_fat'] = "Less than 7% of total calories"
            targets['fiber'] = "25-30g per day (soluble fiber important)"
        
        # Sodium
        if 'high_cholesterol' in conditions or 'kidney_concern' in conditions:
            targets['sodium'] = "Less than 2000mg per day (about 1 tsp salt)"
        else:
            targets['sodium'] = "Less than 2300mg per day"
        
        # Sugar
        if 'diabetes' in conditions or 'prediabetes' in conditions or 'high_triglycerides' in conditions:
            targets['added_sugar'] = "Less than 25g per day (avoid completely if possible)"
        
        # Fiber
        targets['fiber'] = "25-30g per day from vegetables, fruits, whole grains"
        
        # Water
        targets['water'] = "8-10 glasses (2-2.5 liters) per day"
        
        return targets
    
    def _generate_general_notes(self):
        """Generate general notes"""
        return [
            "⚠️ These recommendations are general guidelines based on your test results",
            "👨‍⚕️ Always consult your doctor before making major dietary changes",
            "📊 Individual needs vary based on age, weight, activity level, and medications",
            "🔄 Retest your health markers after 3-6 months to track progress",
            "💪 Consistency is key - small daily improvements lead to big results",
            "🤝 Consider consulting a registered dietitian for personalized meal planning"
        ]


# Function to use in routes
def generate_diet_recommendations(parsed_data):
    """
    Wrapper function to generate diet recommendations
    
    Args:
        parsed_data: Parsed medical report data
        
    Returns:
        Diet plan dictionary
    """
    recommender = DietRecommender()
    return recommender.generate_diet_plan(parsed_data)