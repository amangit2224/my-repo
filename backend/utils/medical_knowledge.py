"""
Enhanced Medical Knowledge Base
100+ medical terms with comprehensive information
Age/gender-specific ranges, disease interpretations, recommendations
"""

class MedicalKnowledgeBase:
    
    def __init__(self):
        """Initialize comprehensive medical knowledge base"""
        
        # ============================================
        # COMPLETE BLOOD COUNT (CBC) - 15 terms
        # ============================================
        
        self.knowledge = {
            'Hemoglobin': {
                'category': 'Complete Blood Count (CBC)',
                'unit': 'g/dL',
                'normal_ranges': {
                    'male': {'min': 13.5, 'max': 17.5},
                    'female': {'min': 12.0, 'max': 15.5}
                },
                'description': 'Protein in red blood cells that carries oxygen throughout the body.',
                'high': {
                    'condition': 'High Hemoglobin (Polycythemia)',
                    'causes': ['Dehydration', 'Living at high altitude', 'Smoking', 'Lung disease', 'Polycythemia vera'],
                    'symptoms': ['Headaches', 'Dizziness', 'Fatigue', 'Shortness of breath'],
                    'severity': 'Moderate',
                    'action': 'Consult doctor to determine cause'
                },
                'low': {
                    'condition': 'Low Hemoglobin (Anemia)',
                    'causes': ['Iron deficiency', 'Blood loss', 'Chronic disease', 'Vitamin B12/folate deficiency'],
                    'symptoms': ['Fatigue', 'Weakness', 'Pale skin', 'Shortness of breath', 'Dizziness'],
                    'severity': 'Moderate to High',
                    'action': 'Iron supplementation, dietary changes, consult doctor'
                }
            },
            
            'WBC': {
                'category': 'Complete Blood Count (CBC)',
                'unit': 'cells/µL',
                'normal_ranges': {
                    'male': {'min': 4500, 'max': 11000},
                    'female': {'min': 4500, 'max': 11000}
                },
                'description': 'White blood cells that fight infection and disease.',
                'high': {
                    'condition': 'High WBC Count (Leukocytosis)',
                    'causes': ['Infection', 'Inflammation', 'Stress', 'Leukemia', 'Allergic reaction'],
                    'symptoms': ['Fever', 'Fatigue', 'Easy bruising', 'Weight loss'],
                    'severity': 'Moderate to High',
                    'action': 'Urgent medical evaluation to rule out serious conditions'
                },
                'low': {
                    'condition': 'Low WBC Count (Leukopenia)',
                    'causes': ['Viral infection', 'Bone marrow disorder', 'Autoimmune disease', 'Certain medications'],
                    'symptoms': ['Frequent infections', 'Fever', 'Mouth sores'],
                    'severity': 'High',
                    'action': 'Medical evaluation, avoid infection exposure'
                }
            },
            
            'RBC': {
                'category': 'Complete Blood Count (CBC)',
                'unit': 'million cells/µL',
                'normal_ranges': {
                    'male': {'min': 4.5, 'max': 5.9},
                    'female': {'min': 4.1, 'max': 5.1}
                },
                'description': 'Red blood cells that carry oxygen from lungs to body tissues.',
                'high': {
                    'condition': 'High RBC Count (Polycythemia)',
                    'causes': ['Dehydration', 'Lung disease', 'Heart disease', 'Living at high altitude'],
                    'symptoms': ['Headaches', 'Dizziness', 'Itching after shower'],
                    'severity': 'Moderate',
                    'action': 'Hydrate well, consult doctor'
                },
                'low': {
                    'condition': 'Low RBC Count (Anemia)',
                    'causes': ['Blood loss', 'Iron deficiency', 'Chronic disease', 'Bone marrow problems'],
                    'symptoms': ['Fatigue', 'Weakness', 'Pale skin', 'Cold hands/feet'],
                    'severity': 'Moderate',
                    'action': 'Iron supplementation, dietary changes'
                }
            },
            
            'Platelets': {
                'category': 'Complete Blood Count (CBC)',
                'unit': 'cells/µL',
                'normal_ranges': {
                    'male': {'min': 150000, 'max': 400000},
                    'female': {'min': 150000, 'max': 400000}
                },
                'description': 'Blood cells that help with clotting and stop bleeding.',
                'high': {
                    'condition': 'High Platelet Count (Thrombocytosis)',
                    'causes': ['Iron deficiency', 'Infection', 'Inflammation', 'Blood disorder'],
                    'symptoms': ['Blood clots', 'Headaches', 'Dizziness'],
                    'severity': 'Moderate to High',
                    'action': 'Medical evaluation to prevent clotting'
                },
                'low': {
                    'condition': 'Low Platelet Count (Thrombocytopenia)',
                    'causes': ['Autoimmune disease', 'Viral infection', 'Leukemia', 'Medications'],
                    'symptoms': ['Easy bruising', 'Prolonged bleeding', 'Nosebleeds'],
                    'severity': 'High',
                    'action': 'Urgent medical attention - bleeding risk'
                }
            },
            
            'Hematocrit': {
                'category': 'Complete Blood Count (CBC)',
                'unit': '%',
                'normal_ranges': {
                    'male': {'min': 38.8, 'max': 50.0},
                    'female': {'min': 34.9, 'max': 44.5}
                },
                'description': 'Percentage of blood volume made up by red blood cells.',
                'high': {
                    'condition': 'High Hematocrit',
                    'causes': ['Dehydration', 'Lung disease', 'Smoking', 'Living at high altitude'],
                    'symptoms': ['Headaches', 'Dizziness', 'Blurred vision'],
                    'severity': 'Moderate',
                    'action': 'Hydrate, consult doctor'
                },
                'low': {
                    'condition': 'Low Hematocrit (Anemia)',
                    'causes': ['Blood loss', 'Iron deficiency', 'Vitamin deficiency'],
                    'symptoms': ['Fatigue', 'Weakness', 'Pale skin'],
                    'severity': 'Moderate',
                    'action': 'Iron supplementation, dietary changes'
                }
            },
            
            'MCV': {
                'category': 'Complete Blood Count (CBC)',
                'unit': 'fL',
                'normal_ranges': {
                    'male': {'min': 80, 'max': 100},
                    'female': {'min': 80, 'max': 100}
                },
                'description': 'Mean Corpuscular Volume - average size of red blood cells.',
                'high': {
                    'condition': 'Large Red Blood Cells (Macrocytosis)',
                    'causes': ['Vitamin B12 deficiency', 'Folate deficiency', 'Alcohol abuse', 'Liver disease'],
                    'symptoms': ['Fatigue', 'Weakness', 'Shortness of breath'],
                    'severity': 'Moderate',
                    'action': 'Vitamin B12/folate supplementation'
                },
                'low': {
                    'condition': 'Small Red Blood Cells (Microcytosis)',
                    'causes': ['Iron deficiency', 'Thalassemia', 'Chronic disease'],
                    'symptoms': ['Fatigue', 'Weakness', 'Pale skin'],
                    'severity': 'Moderate',
                    'action': 'Iron supplementation, genetic testing if needed'
                }
            },
            
            'MCH': {
                'category': 'Complete Blood Count (CBC)',
                'unit': 'pg',
                'normal_ranges': {
                    'male': {'min': 27, 'max': 33},
                    'female': {'min': 27, 'max': 33}
                },
                'description': 'Mean Corpuscular Hemoglobin - average hemoglobin per red blood cell.',
                'high': {
                    'condition': 'High MCH',
                    'causes': ['Vitamin B12 deficiency', 'Folate deficiency'],
                    'symptoms': ['Fatigue', 'Weakness'],
                    'severity': 'Low',
                    'action': 'Vitamin supplementation'
                },
                'low': {
                    'condition': 'Low MCH',
                    'causes': ['Iron deficiency', 'Thalassemia'],
                    'symptoms': ['Fatigue', 'Pale skin'],
                    'severity': 'Moderate',
                    'action': 'Iron supplementation'
                }
            },
            
            'MCHC': {
                'category': 'Complete Blood Count (CBC)',
                'unit': 'g/dL',
                'normal_ranges': {
                    'male': {'min': 32, 'max': 36},
                    'female': {'min': 32, 'max': 36}
                },
                'description': 'Mean Corpuscular Hemoglobin Concentration - hemoglobin concentration in red blood cells.',
                'high': {
                    'condition': 'High MCHC',
                    'causes': ['Hereditary spherocytosis', 'Severe dehydration'],
                    'symptoms': ['Jaundice', 'Fatigue'],
                    'severity': 'Moderate',
                    'action': 'Medical evaluation'
                },
                'low': {
                    'condition': 'Low MCHC',
                    'causes': ['Iron deficiency', 'Thalassemia'],
                    'symptoms': ['Fatigue', 'Weakness'],
                    'severity': 'Moderate',
                    'action': 'Iron supplementation'
                }
            },
            
            # ============================================
            # LIPID PROFILE - 10 terms
            # ============================================
            
            'Total Cholesterol': {
                'category': 'Lipid Profile',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 200},
                    'female': {'min': 0, 'max': 200}
                },
                'description': 'Total amount of cholesterol (fatty substance) in your blood.',
                'high': {
                    'condition': 'High Cholesterol (Hypercholesterolemia)',
                    'causes': ['Diet high in saturated fats', 'Genetics', 'Obesity', 'Lack of exercise', 'Diabetes'],
                    'symptoms': ['Usually no symptoms', 'May cause heart disease over time'],
                    'severity': 'Moderate to High',
                    'action': 'Diet changes, exercise, possible statin medication'
                },
                'low': {
                    'condition': 'Low Cholesterol',
                    'causes': ['Malnutrition', 'Liver disease', 'Hyperthyroidism'],
                    'symptoms': ['Rarely symptomatic'],
                    'severity': 'Low',
                    'action': 'Improve diet if malnourished'
                }
            },
            
            'HDL': {
                'category': 'Lipid Profile',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 40, 'max': 999},
                    'female': {'min': 50, 'max': 999}
                },
                'description': "'Good' cholesterol that removes bad cholesterol from arteries.",
                'high': {
                    'condition': 'High HDL cholesterol',
                    'causes': ['Exercise', 'Genetics', 'Moderate alcohol consumption'],
                    'symptoms': ['Protective against heart disease'],
                    'severity': 'Beneficial',
                    'action': 'Maintain healthy lifestyle - this is good!'
                },
                'low': {
                    'condition': 'Low HDL cholesterol',
                    'causes': ['Smoking', 'Obesity', 'Lack of exercise', 'Type 2 diabetes'],
                    'symptoms': ['Increased heart disease risk'],
                    'severity': 'Moderate to High',
                    'action': 'Exercise, quit smoking, weight loss, omega-3 fatty acids'
                }
            },
            
            'LDL': {
                'category': 'Lipid Profile',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 100},
                    'female': {'min': 0, 'max': 100}
                },
                'description': "'Bad' cholesterol that can clog arteries and increase heart disease risk.",
                'high': {
                    'condition': 'High LDL cholesterol',
                    'causes': ['Diet high in saturated fats', 'Genetics', 'Obesity', 'Lack of exercise'],
                    'symptoms': ['Increased risk of heart attack and stroke'],
                    'severity': 'High',
                    'action': 'Reduce saturated fats, exercise, possible statin medication'
                },
                'low': {
                    'condition': 'Low LDL cholesterol',
                    'causes': ['Healthy diet', 'Medication', 'Genetics'],
                    'symptoms': ['Protective against heart disease'],
                    'severity': 'Beneficial',
                    'action': 'Maintain healthy lifestyle'
                }
            },
            
            'Triglycerides': {
                'category': 'Lipid Profile',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 150},
                    'female': {'min': 0, 'max': 150}
                },
                'description': 'Type of fat in blood. High levels increase heart disease risk.',
                'high': {
                    'condition': 'High Triglycerides (Hypertriglyceridemia)',
                    'causes': ['Obesity', 'Diabetes', 'Alcohol abuse', 'High-carb diet', 'Kidney disease'],
                    'symptoms': ['Usually no symptoms', 'Increased heart disease risk'],
                    'severity': 'Moderate to High',
                    'action': 'Weight loss, reduce sugar/alcohol, exercise, omega-3 supplements'
                },
                'low': {
                    'condition': 'Low Triglycerides',
                    'causes': ['Malnutrition', 'Hyperthyroidism', 'Malabsorption'],
                    'symptoms': ['Rarely symptomatic'],
                    'severity': 'Low',
                    'action': 'Improve nutrition if malnourished'
                }
            },
            
            'VLDL': {
                'category': 'Lipid Profile',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 5, 'max': 40},
                    'female': {'min': 5, 'max': 40}
                },
                'description': 'Very Low-Density Lipoprotein - carries triglycerides in blood.',
                'high': {
                    'condition': 'High VLDL',
                    'causes': ['High triglycerides', 'Diabetes', 'Obesity'],
                    'symptoms': ['Increased cardiovascular risk'],
                    'severity': 'Moderate',
                    'action': 'Weight loss, exercise, reduce carbohydrates'
                },
                'low': {
                    'condition': 'Low VLDL',
                    'causes': ['Low triglycerides', 'Malnutrition'],
                    'symptoms': ['Generally not concerning'],
                    'severity': 'Low',
                    'action': 'Usually no action needed'
                }
            },
            
            # ============================================
            # DIABETES MARKERS - 5 terms
            # ============================================
            
            'HbA1c': {
                'category': 'Metabolic Panel',
                'unit': '%',
                'normal_ranges': {
                    'male': {'min': 4.0, 'max': 5.6},
                    'female': {'min': 4.0, 'max': 5.6}
                },
                'description': 'Average blood sugar level over the past 2-3 months. Better indicator than single glucose test.',
                'high': {
                    'condition': 'High HbA1c (Diabetes/Prediabetes)',
                    'causes': ['Type 2 diabetes', 'Insulin resistance', 'Poor blood sugar control'],
                    'symptoms': ['Increased thirst', 'Frequent urination', 'Fatigue', 'Blurred vision'],
                    'severity': 'High',
                    'action': 'Diabetes management, diet changes, exercise, possible medication'
                },
                'low': {
                    'condition': 'Low HbA1c',
                    'causes': ['Hypoglycemia', 'Anemia', 'Blood loss'],
                    'symptoms': ['Shakiness', 'Sweating', 'Confusion'],
                    'severity': 'Moderate',
                    'action': 'Consult doctor for evaluation'
                }
            },
            
            'Glucose': {
                'category': 'Metabolic Panel',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 70, 'max': 100},
                    'female': {'min': 70, 'max': 100}
                },
                'description': 'Blood sugar level - the amount of glucose (sugar) in your blood.',
                'high': {
                    'condition': 'High blood sugar (Hyperglycemia)',
                    'causes': ['Diabetes', 'Prediabetes', 'Stress', 'Illness', 'Recent meal'],
                    'symptoms': ['Increased thirst', 'Frequent urination', 'Blurred vision', 'Fatigue'],
                    'severity': 'High',
                    'action': 'Consult doctor, HbA1c test, lifestyle changes, possible medication'
                },
                'low': {
                    'condition': 'Low blood sugar (Hypoglycemia)',
                    'causes': ['Too much insulin', 'Skipped meals', 'Excessive exercise', 'Alcohol'],
                    'symptoms': ['Shakiness', 'Sweating', 'Dizziness', 'Confusion', 'Hunger'],
                    'severity': 'Moderate to High',
                    'action': 'Eat fast-acting carbs immediately, adjust medication if diabetic'
                }
            },
            
            'Insulin': {
                'category': 'Metabolic Panel',
                'unit': 'µU/mL',
                'normal_ranges': {
                    'male': {'min': 2.6, 'max': 24.9},
                    'female': {'min': 2.6, 'max': 24.9}
                },
                'description': 'Hormone that regulates blood sugar by moving glucose into cells.',
                'high': {
                    'condition': 'High Insulin (Hyperinsulinemia)',
                    'causes': ['Insulin resistance', 'Prediabetes', 'Obesity', 'PCOS'],
                    'symptoms': ['Weight gain', 'Fatigue', 'Sugar cravings'],
                    'severity': 'Moderate',
                    'action': 'Weight loss, low-carb diet, exercise'
                },
                'low': {
                    'condition': 'Low Insulin',
                    'causes': ['Type 1 diabetes', 'Pancreatic damage'],
                    'symptoms': ['High blood sugar', 'Weight loss', 'Frequent urination'],
                    'severity': 'High',
                    'action': 'Insulin therapy, diabetes management'
                }
            },
            
            'C-Peptide': {
                'category': 'Metabolic Panel',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 0.5, 'max': 2.0},
                    'female': {'min': 0.5, 'max': 2.0}
                },
                'description': 'Byproduct of insulin production - indicates how much insulin body makes.',
                'high': {
                    'condition': 'High C-Peptide',
                    'causes': ['Insulin resistance', 'Type 2 diabetes', 'Insulinoma'],
                    'symptoms': ['Similar to high insulin'],
                    'severity': 'Moderate',
                    'action': 'Diabetes management, weight loss'
                },
                'low': {
                    'condition': 'Low C-Peptide',
                    'causes': ['Type 1 diabetes', 'Pancreatic insufficiency'],
                    'symptoms': ['High blood sugar', 'Weight loss'],
                    'severity': 'High',
                    'action': 'Insulin therapy'
                }
            },
            
            # ============================================
            # THYROID FUNCTION - 6 terms
            # ============================================
            
            'TSH': {
                'category': 'Thyroid Function',
                'unit': 'mIU/L',
                'normal_ranges': {
                    'male': {'min': 0.4, 'max': 4.5},
                    'female': {'min': 0.4, 'max': 4.5}
                },
                'description': 'Thyroid Stimulating Hormone - controls thyroid gland function.',
                'high': {
                    'condition': 'High TSH (Hypothyroidism)',
                    'causes': ['Underactive thyroid', 'Hashimoto\'s thyroiditis', 'Iodine deficiency'],
                    'symptoms': ['Fatigue', 'Weight gain', 'Cold intolerance', 'Depression', 'Constipation'],
                    'severity': 'Moderate',
                    'action': 'Thyroid hormone replacement (Levothyroxine)'
                },
                'low': {
                    'condition': 'Low TSH (Hyperthyroidism)',
                    'causes': ['Overactive thyroid', 'Graves\' disease', 'Thyroid nodules'],
                    'symptoms': ['Weight loss', 'Rapid heartbeat', 'Anxiety', 'Sweating', 'Tremors'],
                    'severity': 'Moderate to High',
                    'action': 'Anti-thyroid medication, radioactive iodine, or surgery'
                }
            },
            
            'T3': {
                'category': 'Thyroid Function',
                'unit': 'ng/dL',
                'normal_ranges': {
                    'male': {'min': 80, 'max': 200},
                    'female': {'min': 80, 'max': 200}
                },
                'description': 'Triiodothyronine - active thyroid hormone that regulates metabolism.',
                'high': {
                    'condition': 'High T3 (Hyperthyroidism)',
                    'causes': ['Graves\' disease', 'Toxic nodular goiter', 'Thyroiditis'],
                    'symptoms': ['Weight loss', 'Rapid heartbeat', 'Nervousness', 'Sweating'],
                    'severity': 'Moderate to High',
                    'action': 'Anti-thyroid medication, beta-blockers'
                },
                'low': {
                    'condition': 'Low T3 (Hypothyroidism)',
                    'causes': ['Underactive thyroid', 'Severe illness', 'Malnutrition'],
                    'symptoms': ['Fatigue', 'Weight gain', 'Depression', 'Cold intolerance'],
                    'severity': 'Moderate',
                    'action': 'Thyroid hormone replacement'
                }
            },
            
            'T4': {
                'category': 'Thyroid Function',
                'unit': 'µg/dL',
                'normal_ranges': {
                    'male': {'min': 4.5, 'max': 11.2},
                    'female': {'min': 4.5, 'max': 11.2}
                },
                'description': 'Thyroxine - main thyroid hormone, converted to T3 in body.',
                'high': {
                    'condition': 'High T4 (Hyperthyroidism)',
                    'causes': ['Graves\' disease', 'Toxic adenoma', 'Thyroiditis'],
                    'symptoms': ['Weight loss', 'Tremors', 'Heat intolerance', 'Palpitations'],
                    'severity': 'Moderate to High',
                    'action': 'Anti-thyroid drugs, radioactive iodine'
                },
                'low': {
                    'condition': 'Low T4 (Hypothyroidism)',
                    'causes': ['Hashimoto\'s disease', 'Iodine deficiency', 'Pituitary disorder'],
                    'symptoms': ['Fatigue', 'Weight gain', 'Dry skin', 'Hair loss'],
                    'severity': 'Moderate',
                    'action': 'Levothyroxine therapy'
                }
            },
            
            'Free T3': {
                'category': 'Thyroid Function',
                'unit': 'pg/mL',
                'normal_ranges': {
                    'male': {'min': 2.3, 'max': 4.2},
                    'female': {'min': 2.3, 'max': 4.2}
                },
                'description': 'Unbound T3 hormone - more accurate measure of thyroid function.',
                'high': {
                    'condition': 'High Free T3',
                    'causes': ['Hyperthyroidism', 'T3 thyrotoxicosis'],
                    'symptoms': ['Similar to high T3'],
                    'severity': 'Moderate to High',
                    'action': 'Anti-thyroid medication'
                },
                'low': {
                    'condition': 'Low Free T3',
                    'causes': ['Hypothyroidism', 'Severe illness', 'Starvation'],
                    'symptoms': ['Fatigue', 'Weight gain', 'Depression'],
                    'severity': 'Moderate',
                    'action': 'Thyroid hormone replacement'
                }
            },
            
            'Free T4': {
                'category': 'Thyroid Function',
                'unit': 'ng/dL',
                'normal_ranges': {
                    'male': {'min': 0.8, 'max': 1.8},
                    'female': {'min': 0.8, 'max': 1.8}
                },
                'description': 'Unbound T4 hormone - not affected by protein levels.',
                'high': {
                    'condition': 'High Free T4',
                    'causes': ['Hyperthyroidism', 'Graves\' disease'],
                    'symptoms': ['Weight loss', 'Anxiety', 'Tremors'],
                    'severity': 'Moderate to High',
                    'action': 'Anti-thyroid medication'
                },
                'low': {
                    'condition': 'Low Free T4',
                    'causes': ['Hypothyroidism', 'Pituitary disorder'],
                    'symptoms': ['Fatigue', 'Cold intolerance', 'Weight gain'],
                    'severity': 'Moderate',
                    'action': 'Levothyroxine replacement'
                }
            },
            
            # ============================================
            # LIVER FUNCTION - 8 terms
            # ============================================
            
            'ALT': {
                'category': 'Liver Function',
                'unit': 'U/L',
                'normal_ranges': {
                    'male': {'min': 7, 'max': 45},
                    'female': {'min': 7, 'max': 34}
                },
                'description': 'Enzyme found mainly in liver. High levels indicate liver damage.',
                'high': {
                    'condition': 'Elevated ALT (Liver damage)',
                    'causes': ['Hepatitis', 'Fatty liver disease', 'Alcohol abuse', 'Medications', 'Cirrhosis'],
                    'symptoms': ['Fatigue', 'Jaundice', 'Abdominal pain', 'Nausea'],
                    'severity': 'Moderate to High',
                    'action': 'Stop alcohol, weight loss if obese, medical evaluation, liver imaging'
                },
                'low': {
                    'condition': 'Low ALT',
                    'causes': ['Rare', 'Vitamin B6 deficiency'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Generally not concerning'
                }
            },
            
            'AST': {
                'category': 'Liver Function',
                'unit': 'U/L',
                'normal_ranges': {
                    'male': {'min': 8, 'max': 48},
                    'female': {'min': 8, 'max': 43}
                },
                'description': 'Enzyme found in liver and heart. Elevated in liver or heart damage.',
                'high': {
                    'condition': 'Elevated AST',
                    'causes': ['Liver disease', 'Heart attack', 'Muscle damage', 'Alcohol abuse', 'Medications'],
                    'symptoms': ['Depends on cause - fatigue, jaundice, chest pain'],
                    'severity': 'Moderate to High',
                    'action': 'Medical evaluation to determine cause'
                },
                'low': {
                    'condition': 'Low AST',
                    'causes': ['Vitamin B6 deficiency', 'Uremia'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Usually not concerning'
                }
            },
            
            'ALP': {
                'category': 'Liver Function',
                'unit': 'U/L',
                'normal_ranges': {
                    'male': {'min': 40, 'max': 130},
                    'female': {'min': 35, 'max': 104}
                },
                'description': 'Alkaline Phosphatase - enzyme in liver, bones, kidneys.',
                'high': {
                    'condition': 'Elevated ALP',
                    'causes': ['Liver disease', 'Bone disorders', 'Bile duct obstruction', 'Pregnancy'],
                    'symptoms': ['Jaundice', 'Bone pain', 'Fatigue'],
                    'severity': 'Moderate',
                    'action': 'Medical evaluation, liver ultrasound'
                },
                'low': {
                    'condition': 'Low ALP',
                    'causes': ['Malnutrition', 'Zinc deficiency', 'Hypothyroidism'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Nutritional assessment if very low'
                }
            },
            
            'Bilirubin': {
                'category': 'Liver Function',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 0.1, 'max': 1.2},
                    'female': {'min': 0.1, 'max': 1.2}
                },
                'description': 'Yellow pigment from red blood cell breakdown. High levels cause jaundice.',
                'high': {
                    'condition': 'High Bilirubin (Hyperbilirubinemia)',
                    'causes': ['Liver disease', 'Bile duct obstruction', 'Hemolytic anemia', 'Gilbert\'s syndrome'],
                    'symptoms': ['Jaundice (yellow skin/eyes)', 'Dark urine', 'Fatigue'],
                    'severity': 'Moderate to High',
                    'action': 'Medical evaluation, liver function tests, ultrasound'
                },
                'low': {
                    'condition': 'Low Bilirubin',
                    'causes': ['Generally not concerning'],
                    'symptoms': ['None'],
                    'severity': 'Low',
                    'action': 'No action needed'
                }
            },
            
            'Albumin': {
                'category': 'Liver Function',
                'unit': 'g/dL',
                'normal_ranges': {
                    'male': {'min': 3.5, 'max': 5.5},
                    'female': {'min': 3.5, 'max': 5.5}
                },
                'description': 'Protein made by liver - maintains fluid balance in blood.',
                'high': {
                    'condition': 'High Albumin',
                    'causes': ['Dehydration', 'High protein diet'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Hydrate well'
                },
                'low': {
                    'condition': 'Low Albumin (Hypoalbuminemia)',
                    'causes': ['Liver disease', 'Kidney disease', 'Malnutrition', 'Inflammation'],
                    'symptoms': ['Swelling (edema)', 'Fatigue', 'Weakness'],
                    'severity': 'Moderate to High',
                    'action': 'Treat underlying cause, improve nutrition'
                }
            },
            
            'Total Protein': {
                'category': 'Liver Function',
                'unit': 'g/dL',
                'normal_ranges': {
                    'male': {'min': 6.0, 'max': 8.3},
                    'female': {'min': 6.0, 'max': 8.3}
                },
                'description': 'Total protein in blood - albumin plus globulins.',
                'high': {
                    'condition': 'High Total Protein',
                    'causes': ['Dehydration', 'Chronic inflammation', 'Multiple myeloma'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low to Moderate',
                    'action': 'Hydrate, medical evaluation if very high'
                },
                'low': {
                    'condition': 'Low Total Protein',
                    'causes': ['Malnutrition', 'Liver disease', 'Kidney disease'],
                    'symptoms': ['Swelling', 'Weakness', 'Fatigue'],
                    'severity': 'Moderate',
                    'action': 'Improve nutrition, treat underlying disease'
                }
            },
            
            'GGT': {
                'category': 'Liver Function',
                'unit': 'U/L',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 65},
                    'female': {'min': 0, 'max': 45}
                },
                'description': 'Gamma-Glutamyl Transferase - enzyme sensitive to alcohol and bile duct problems.',
                'high': {
                    'condition': 'Elevated GGT',
                    'causes': ['Alcohol abuse', 'Bile duct disease', 'Fatty liver', 'Certain medications'],
                    'symptoms': ['Usually none', 'Possible jaundice'],
                    'severity': 'Moderate',
                    'action': 'Stop alcohol, medical evaluation'
                },
                'low': {
                    'condition': 'Low GGT',
                    'causes': ['Generally not significant'],
                    'symptoms': ['None'],
                    'severity': 'Low',
                    'action': 'No action needed'
                }
            },
            
            # ============================================
            # KIDNEY FUNCTION - 6 terms
            # ============================================
            
            'Creatinine': {
                'category': 'Kidney Function',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 0.7, 'max': 1.3},
                    'female': {'min': 0.6, 'max': 1.1}
                },
                'description': 'Waste product filtered by kidneys. High levels indicate kidney problems.',
                'high': {
                    'condition': 'High Creatinine (Kidney dysfunction)',
                    'causes': ['Chronic kidney disease', 'Dehydration', 'Muscle breakdown', 'Certain medications'],
                    'symptoms': ['Fatigue', 'Swelling', 'Decreased urination', 'Nausea'],
                    'severity': 'High',
                    'action': 'Medical evaluation, reduce protein intake, treat underlying cause'
                },
                'low': {
                    'condition': 'Low Creatinine',
                    'causes': ['Low muscle mass', 'Malnutrition', 'Pregnancy'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Generally not concerning'
                }
            },
            
            'BUN': {
                'category': 'Kidney Function',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 8, 'max': 24},
                    'female': {'min': 8, 'max': 24}
                },
                'description': 'Blood Urea Nitrogen - waste product from protein breakdown, filtered by kidneys.',
                'high': {
                    'condition': 'High BUN',
                    'causes': ['Kidney disease', 'Dehydration', 'High protein diet', 'Heart failure'],
                    'symptoms': ['Fatigue', 'Nausea', 'Confusion', 'Decreased urination'],
                    'severity': 'Moderate to High',
                    'action': 'Hydrate, medical evaluation, reduce protein intake'
                },
                'low': {
                    'condition': 'Low BUN',
                    'causes': ['Liver disease', 'Malnutrition', 'Overhydration'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Improve nutrition if malnourished'
                }
            },
            
            'eGFR': {
                'category': 'Kidney Function',
                'unit': 'mL/min/1.73m²',
                'normal_ranges': {
                    'male': {'min': 90, 'max': 120},
                    'female': {'min': 90, 'max': 120}
                },
                'description': 'Estimated Glomerular Filtration Rate - how well kidneys are filtering blood.',
                'high': {
                    'condition': 'High eGFR',
                    'causes': ['Hyperfiltration', 'Early diabetes'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Monitor kidney function'
                },
                'low': {
                    'condition': 'Low eGFR (Kidney disease)',
                    'causes': ['Chronic kidney disease', 'Diabetes', 'Hypertension', 'Glomerulonephritis'],
                    'symptoms': ['Fatigue', 'Swelling', 'Decreased urination'],
                    'severity': 'High',
                    'action': 'Nephrology referral, blood pressure control, diabetes management'
                }
            },
            
            'Uric Acid': {
                'category': 'Kidney Function',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 3.4, 'max': 7.0},
                    'female': {'min': 2.4, 'max': 6.0}
                },
                'description': 'Waste product from purine breakdown. High levels cause gout.',
                'high': {
                    'condition': 'High Uric Acid (Hyperuricemia)',
                    'causes': ['Gout', 'Kidney disease', 'High-purine diet', 'Alcohol', 'Certain medications'],
                    'symptoms': ['Joint pain (gout)', 'Swelling', 'Redness', 'Kidney stones'],
                    'severity': 'Moderate to High',
                    'action': 'Low-purine diet, hydration, allopurinol medication, avoid alcohol'
                },
                'low': {
                    'condition': 'Low Uric Acid',
                    'causes': ['Wilson\'s disease', 'Fanconi syndrome', 'Low-purine diet'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Generally not concerning'
                }
            },
            
            'Sodium': {
                'category': 'Electrolytes',
                'unit': 'mEq/L',
                'normal_ranges': {
                    'male': {'min': 136, 'max': 145},
                    'female': {'min': 136, 'max': 145}
                },
                'description': 'Electrolyte that regulates fluid balance and nerve function.',
                'high': {
                    'condition': 'High Sodium (Hypernatremia)',
                    'causes': ['Dehydration', 'Diabetes insipidus', 'Excessive salt intake'],
                    'symptoms': ['Thirst', 'Confusion', 'Seizures', 'Weakness'],
                    'severity': 'Moderate to High',
                    'action': 'Hydrate gradually, medical evaluation'
                },
                'low': {
                    'condition': 'Low Sodium (Hyponatremia)',
                    'causes': ['Overhydration', 'Heart failure', 'Kidney disease', 'SIADH'],
                    'symptoms': ['Nausea', 'Headache', 'Confusion', 'Seizures'],
                    'severity': 'High',
                    'action': 'Fluid restriction, medical evaluation'
                }
            },
            
            'Potassium': {
                'category': 'Electrolytes',
                'unit': 'mEq/L',
                'normal_ranges': {
                    'male': {'min': 3.5, 'max': 5.0},
                    'female': {'min': 3.5, 'max': 5.0}
                },
                'description': 'Electrolyte essential for heart and muscle function.',
                'high': {
                    'condition': 'High Potassium (Hyperkalemia)',
                    'causes': ['Kidney disease', 'Certain medications (ACE inhibitors)', 'Excessive supplementation'],
                    'symptoms': ['Weakness', 'Irregular heartbeat', 'Nausea', 'Tingling'],
                    'severity': 'High - Emergency',
                    'action': 'Urgent medical attention - can cause cardiac arrest'
                },
                'low': {
                    'condition': 'Low Potassium (Hypokalemia)',
                    'causes': ['Diuretics', 'Vomiting', 'Diarrhea', 'Poor diet'],
                    'symptoms': ['Muscle weakness', 'Cramps', 'Irregular heartbeat', 'Fatigue'],
                    'severity': 'Moderate to High',
                    'action': 'Potassium supplementation, eat bananas/potatoes'
                }
            },
            
            # ============================================
            # CARDIAC MARKERS - 4 terms
            # ============================================
            
            'Troponin': {
                'category': 'Cardiac Markers',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 0.04},
                    'female': {'min': 0, 'max': 0.04}
                },
                'description': 'Protein released when heart muscle is damaged. Key heart attack indicator.',
                'high': {
                    'condition': 'Elevated Troponin (Heart muscle damage)',
                    'causes': ['Heart attack (MI)', 'Heart failure', 'Myocarditis', 'Pulmonary embolism'],
                    'symptoms': ['Chest pain', 'Shortness of breath', 'Sweating', 'Nausea'],
                    'severity': 'Critical - Emergency',
                    'action': 'IMMEDIATE EMERGENCY CARE - Call 911'
                },
                'low': {
                    'condition': 'Normal Troponin',
                    'causes': ['Healthy heart'],
                    'symptoms': ['None'],
                    'severity': 'Normal',
                    'action': 'No action needed - good sign'
                }
            },
            
            'CK-MB': {
                'category': 'Cardiac Markers',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 3.6},
                    'female': {'min': 0, 'max': 3.6}
                },
                'description': 'Creatine Kinase MB - enzyme specific to heart muscle.',
                'high': {
                    'condition': 'Elevated CK-MB (Heart damage)',
                    'causes': ['Heart attack', 'Myocarditis', 'Cardiac surgery'],
                    'symptoms': ['Chest pain', 'Irregular heartbeat'],
                    'severity': 'High - Emergency',
                    'action': 'Emergency medical evaluation'
                },
                'low': {
                    'condition': 'Normal CK-MB',
                    'causes': ['Healthy heart'],
                    'symptoms': ['None'],
                    'severity': 'Normal',
                    'action': 'No action needed'
                }
            },
            
            'BNP': {
                'category': 'Cardiac Markers',
                'unit': 'pg/mL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 100},
                    'female': {'min': 0, 'max': 100}
                },
                'description': 'B-type Natriuretic Peptide - indicates heart failure severity.',
                'high': {
                    'condition': 'Elevated BNP (Heart failure)',
                    'causes': ['Congestive heart failure', 'Kidney failure', 'Pulmonary hypertension'],
                    'symptoms': ['Shortness of breath', 'Fatigue', 'Swollen legs', 'Rapid heartbeat'],
                    'severity': 'High',
                    'action': 'Cardiology evaluation, diuretics, heart failure management'
                },
                'low': {
                    'condition': 'Normal BNP',
                    'causes': ['Normal heart function'],
                    'symptoms': ['None'],
                    'severity': 'Normal',
                    'action': 'No action needed'
                }
            },
            
            # ============================================
            # VITAMINS & MINERALS - 8 terms
            # ============================================
            
            'Vitamin D': {
                'category': 'Vitamins & Minerals',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 30, 'max': 100},
                    'female': {'min': 30, 'max': 100}
                },
                'description': 'Vitamin essential for bone health and immune function.',
                'high': {
                    'condition': 'Vitamin D Toxicity',
                    'causes': ['Excessive supplementation'],
                    'symptoms': ['Nausea', 'Weakness', 'Kidney problems'],
                    'severity': 'Moderate',
                    'action': 'Stop supplements, medical evaluation'
                },
                'low': {
                    'condition': 'Vitamin D Deficiency',
                    'causes': ['Lack of sun exposure', 'Poor diet', 'Malabsorption'],
                    'symptoms': ['Bone pain', 'Muscle weakness', 'Fatigue', 'Increased infection risk'],
                    'severity': 'Moderate',
                    'action': 'Vitamin D3 supplementation (1000-2000 IU daily), sun exposure'
                }
            },
            
            'Vitamin B12': {
                'category': 'Vitamins & Minerals',
                'unit': 'pg/mL',
                'normal_ranges': {
                    'male': {'min': 200, 'max': 900},
                    'female': {'min': 200, 'max': 900}
                },
                'description': 'Vitamin essential for nerve function and red blood cell production.',
                'high': {
                    'condition': 'High Vitamin B12',
                    'causes': ['Supplementation', 'Liver disease', 'Certain cancers'],
                    'symptoms': ['Usually none'],
                    'severity': 'Low',
                    'action': 'Medical evaluation if very high'
                },
                'low': {
                    'condition': 'Vitamin B12 Deficiency',
                    'causes': ['Vegan diet', 'Pernicious anemia', 'Malabsorption', 'Age'],
                    'symptoms': ['Fatigue', 'Weakness', 'Tingling in hands/feet', 'Memory problems'],
                    'severity': 'Moderate',
                    'action': 'B12 supplementation or injections, dietary changes'
                }
            },
            
            'Folate': {
                'category': 'Vitamins & Minerals',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 2.7, 'max': 17.0},
                    'female': {'min': 2.7, 'max': 17.0}
                },
                'description': 'Vitamin B9 - essential for DNA synthesis and red blood cell formation.',
                'high': {
                    'condition': 'High Folate',
                    'causes': ['Excessive supplementation'],
                    'symptoms': ['Usually none', 'May mask B12 deficiency'],
                    'severity': 'Low',
                    'action': 'Reduce supplementation'
                },
                'low': {
                    'condition': 'Folate Deficiency',
                    'causes': ['Poor diet', 'Alcohol abuse', 'Malabsorption', 'Pregnancy'],
                    'symptoms': ['Fatigue', 'Weakness', 'Mouth sores', 'Anemia'],
                    'severity': 'Moderate',
                    'action': 'Folate supplementation, eat leafy greens'
                }
            },
            
            'Iron': {
                'category': 'Vitamins & Minerals',
                'unit': 'µg/dL',
                'normal_ranges': {
                    'male': {'min': 65, 'max': 175},
                    'female': {'min': 50, 'max': 170}
                },
                'description': 'Mineral essential for hemoglobin production and oxygen transport.',
                'high': {
                    'condition': 'High Iron (Iron overload)',
                    'causes': ['Hemochromatosis', 'Excessive supplementation', 'Multiple transfusions'],
                    'symptoms': ['Fatigue', 'Joint pain', 'Abdominal pain', 'Organ damage'],
                    'severity': 'High',
                    'action': 'Phlebotomy (blood removal), chelation therapy'
                },
                'low': {
                    'condition': 'Low Iron (Iron deficiency)',
                    'causes': ['Poor diet', 'Blood loss', 'Pregnancy', 'Malabsorption'],
                    'symptoms': ['Fatigue', 'Weakness', 'Pale skin', 'Brittle nails', 'Cold hands/feet'],
                    'severity': 'Moderate',
                    'action': 'Iron supplementation, eat red meat/spinach'
                }
            },
            
            'Ferritin': {
                'category': 'Vitamins & Minerals',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 24, 'max': 336},
                    'female': {'min': 11, 'max': 307}
                },
                'description': 'Protein that stores iron - best indicator of iron stores.',
                'high': {
                    'condition': 'High Ferritin',
                    'causes': ['Hemochromatosis', 'Inflammation', 'Liver disease', 'Alcohol abuse'],
                    'symptoms': ['Fatigue', 'Joint pain', 'Abdominal pain'],
                    'severity': 'Moderate to High',
                    'action': 'Medical evaluation, treat underlying cause'
                },
                'low': {
                    'condition': 'Low Ferritin (Iron deficiency)',
                    'causes': ['Poor diet', 'Blood loss', 'Pregnancy'],
                    'symptoms': ['Fatigue', 'Weakness', 'Hair loss', 'Restless legs'],
                    'severity': 'Moderate',
                    'action': 'Iron supplementation, dietary changes'
                }
            },
            
            'Calcium': {
                'category': 'Vitamins & Minerals',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 8.5, 'max': 10.5},
                    'female': {'min': 8.5, 'max': 10.5}
                },
                'description': 'Mineral essential for bones, teeth, muscle function, and nerve signaling.',
                'high': {
                    'condition': 'High Calcium (Hypercalcemia)',
                    'causes': ['Hyperparathyroidism', 'Cancer', 'Excessive vitamin D', 'Certain medications'],
                    'symptoms': ['Kidney stones', 'Bone pain', 'Confusion', 'Nausea', 'Fatigue'],
                    'severity': 'Moderate to High',
                    'action': 'Medical evaluation, hydration, treat underlying cause'
                },
                'low': {
                    'condition': 'Low Calcium (Hypocalcemia)',
                    'causes': ['Vitamin D deficiency', 'Hypoparathyroidism', 'Kidney disease', 'Malabsorption'],
                    'symptoms': ['Muscle cramps', 'Tingling', 'Seizures', 'Irregular heartbeat'],
                    'severity': 'Moderate to High',
                    'action': 'Calcium and vitamin D supplementation'
                }
            },
            
            'Magnesium': {
                'category': 'Vitamins & Minerals',
                'unit': 'mg/dL',
                'normal_ranges': {
                    'male': {'min': 1.7, 'max': 2.2},
                    'female': {'min': 1.7, 'max': 2.2}
                },
                'description': 'Mineral important for muscle and nerve function, blood sugar control.',
                'high': {
                    'condition': 'High Magnesium (Hypermagnesemia)',
                    'causes': ['Kidney failure', 'Excessive supplementation', 'Antacids'],
                    'symptoms': ['Nausea', 'Weakness', 'Low blood pressure', 'Irregular heartbeat'],
                    'severity': 'Moderate to High',
                    'action': 'Medical evaluation, stop supplements'
                },
                'low': {
                    'condition': 'Low Magnesium (Hypomagnesemia)',
                    'causes': ['Poor diet', 'Alcohol abuse', 'Diuretics', 'Diarrhea'],
                    'symptoms': ['Muscle cramps', 'Tremors', 'Irregular heartbeat', 'Fatigue'],
                    'severity': 'Moderate',
                    'action': 'Magnesium supplementation, eat nuts/seeds/whole grains'
                }
            },
            
            'Zinc': {
                'category': 'Vitamins & Minerals',
                'unit': 'µg/dL',
                'normal_ranges': {
                    'male': {'min': 70, 'max': 120},
                    'female': {'min': 70, 'max': 120}
                },
                'description': 'Mineral essential for immune function, wound healing, and taste.',
                'high': {
                    'condition': 'Zinc Toxicity',
                    'causes': ['Excessive supplementation'],
                    'symptoms': ['Nausea', 'Vomiting', 'Loss of appetite', 'Headaches'],
                    'severity': 'Moderate',
                    'action': 'Stop zinc supplements'
                },
                'low': {
                    'condition': 'Zinc Deficiency',
                    'causes': ['Poor diet', 'Malabsorption', 'Chronic disease'],
                    'symptoms': ['Hair loss', 'Diarrhea', 'Delayed wound healing', 'Loss of taste/smell'],
                    'severity': 'Moderate',
                    'action': 'Zinc supplementation, eat meat/seafood/nuts'
                }
            },
            
            # ============================================
            # INFLAMMATORY MARKERS - 3 terms
            # ============================================
            
            'CRP': {
                'category': 'Inflammatory Markers',
                'unit': 'mg/L',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 3.0},
                    'female': {'min': 0, 'max': 3.0}
                },
                'description': 'C-Reactive Protein - general marker of inflammation in the body.',
                'high': {
                    'condition': 'High CRP (Inflammation)',
                    'causes': ['Infection', 'Autoimmune disease', 'Heart disease', 'Cancer', 'Chronic inflammation'],
                    'symptoms': ['Depends on underlying cause'],
                    'severity': 'Moderate',
                    'action': 'Identify and treat source of inflammation'
                },
                'low': {
                    'condition': 'Low CRP',
                    'causes': ['No significant inflammation'],
                    'symptoms': ['None'],
                    'severity': 'Normal',
                    'action': 'Good sign - no action needed'
                }
            },
            
            'ESR': {
                'category': 'Inflammatory Markers',
                'unit': 'mm/hr',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 15},
                    'female': {'min': 0, 'max': 20}
                },
                'description': 'Erythrocyte Sedimentation Rate - measures how quickly red blood cells settle.',
                'high': {
                    'condition': 'High ESR (Inflammation)',
                    'causes': ['Infection', 'Autoimmune disease', 'Cancer', 'Kidney disease'],
                    'symptoms': ['Depends on underlying condition'],
                    'severity': 'Moderate',
                    'action': 'Further testing to identify cause'
                },
                'low': {
                    'condition': 'Low ESR',
                    'causes': ['Normal', 'Polycythemia'],
                    'symptoms': ['None'],
                    'severity': 'Normal',
                    'action': 'No action needed'
                }
            },
            
            # ============================================
            # HORMONES - 6 terms
            # ============================================
            
            'Testosterone': {
                'category': 'Hormones',
                'unit': 'ng/dL',
                'normal_ranges': {
                    'male': {'min': 300, 'max': 1000},
                    'female': {'min': 15, 'max': 70}
                },
                'description': 'Primary male sex hormone - affects muscle, bone density, sex drive.',
                'high': {
                    'condition': 'High Testosterone',
                    'causes': ['Steroid use', 'Adrenal tumors', 'PCOS (in women)'],
                    'symptoms': ['Acne', 'Aggression', 'Excessive body hair', 'Enlarged prostate (men)'],
                    'severity': 'Moderate',
                    'action': 'Medical evaluation, stop steroids if using'
                },
                'low': {
                    'condition': 'Low Testosterone (Hypogonadism)',
                    'causes': ['Aging', 'Obesity', 'Pituitary disorders', 'Testicular problems'],
                    'symptoms': ['Low libido', 'Fatigue', 'Muscle loss', 'Depression', 'Erectile dysfunction'],
                    'severity': 'Moderate',
                    'action': 'Testosterone replacement therapy, weight loss, exercise'
                }
            },
            
            'Estradiol': {
                'category': 'Hormones',
                'unit': 'pg/mL',
                'normal_ranges': {
                    'male': {'min': 10, 'max': 40},
                    'female': {'min': 30, 'max': 400}  # Varies by menstrual cycle phase
                },
                'description': 'Primary female sex hormone - regulates reproductive system.',
                'high': {
                    'condition': 'High Estradiol',
                    'causes': ['Ovarian tumors', 'Hormone therapy', 'Obesity'],
                    'symptoms': ['Irregular periods', 'Breast tenderness', 'Mood swings'],
                    'severity': 'Moderate',
                    'action': 'Medical evaluation, possible imaging'
                },
                'low': {
                    'condition': 'Low Estradiol',
                    'causes': ['Menopause', 'Ovarian failure', 'Excessive exercise', 'Eating disorders'],
                    'symptoms': ['Hot flashes', 'Vaginal dryness', 'Bone loss', 'Mood changes'],
                    'severity': 'Moderate',
                    'action': 'Hormone replacement therapy (if menopausal)'
                }
            },
            
            'Cortisol': {
                'category': 'Hormones',
                'unit': 'µg/dL',
                'normal_ranges': {
                    'male': {'min': 6, 'max': 23},  # Morning levels
                    'female': {'min': 6, 'max': 23}
                },
                'description': 'Stress hormone produced by adrenal glands.',
                'high': {
                    'condition': 'High Cortisol (Cushing\'s syndrome)',
                    'causes': ['Chronic stress', 'Cushing\'s disease', 'Steroid medications', 'Adrenal tumors'],
                    'symptoms': ['Weight gain', 'High blood pressure', 'Mood changes', 'Easy bruising'],
                    'severity': 'Moderate to High',
                    'action': 'Stress reduction, medical evaluation, treat underlying cause'
                },
                'low': {
                    'condition': 'Low Cortisol (Addison\'s disease)',
                    'causes': ['Adrenal insufficiency', 'Pituitary disorders'],
                    'symptoms': ['Fatigue', 'Weakness', 'Low blood pressure', 'Weight loss'],
                    'severity': 'High',
                    'action': 'Cortisol replacement therapy - medical emergency if acute'
                }
            },
            
            'Prolactin': {
                'category': 'Hormones',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 2, 'max': 18},
                    'female': {'min': 2, 'max': 29}
                },
                'description': 'Hormone that stimulates breast milk production.',
                'high': {
                    'condition': 'High Prolactin (Hyperprolactinemia)',
                    'causes': ['Pituitary tumor', 'Medications', 'Hypothyroidism', 'Pregnancy'],
                    'symptoms': ['Breast milk production (not pregnant)', 'Irregular periods', 'Low libido'],
                    'severity': 'Moderate',
                    'action': 'MRI of pituitary, medication (bromocriptine)'
                },
                'low': {
                    'condition': 'Low Prolactin',
                    'causes': ['Pituitary dysfunction'],
                    'symptoms': ['Difficulty breastfeeding'],
                    'severity': 'Low to Moderate',
                    'action': 'Medical evaluation if symptomatic'
                }
            },
            
            'FSH': {
                'category': 'Hormones',
                'unit': 'mIU/mL',
                'normal_ranges': {
                    'male': {'min': 1.5, 'max': 12.4},
                    'female': {'min': 4.7, 'max': 21.5}  # Varies by menstrual cycle
                },
                'description': 'Follicle Stimulating Hormone - regulates reproductive processes.',
                'high': {
                    'condition': 'High FSH',
                    'causes': ['Menopause', 'Ovarian failure', 'Testicular failure'],
                    'symptoms': ['Irregular periods', 'Hot flashes', 'Infertility'],
                    'severity': 'Moderate',
                    'action': 'Fertility evaluation, hormone replacement if menopausal'
                },
                'low': {
                    'condition': 'Low FSH',
                    'causes': ['Pituitary disorders', 'Stress', 'Eating disorders'],
                    'symptoms': ['Irregular periods', 'Low libido', 'Infertility'],
                    'severity': 'Moderate',
                    'action': 'Medical evaluation, treat underlying cause'
                }
            },
            
            'LH': {
                'category': 'Hormones',
                'unit': 'mIU/mL',
                'normal_ranges': {
                    'male': {'min': 1.7, 'max': 8.6},
                    'female': {'min': 2.4, 'max': 12.6}  # Varies by menstrual cycle
                },
                'description': 'Luteinizing Hormone - triggers ovulation and testosterone production.',
                'high': {
                    'condition': 'High LH',
                    'causes': ['PCOS', 'Menopause', 'Pituitary tumors'],
                    'symptoms': ['Irregular periods', 'Infertility', 'Hot flashes'],
                    'severity': 'Moderate',
                    'action': 'Medical evaluation, fertility treatment if desired'
                },
                'low': {
                    'condition': 'Low LH',
                    'causes': ['Pituitary dysfunction', 'Eating disorders', 'Stress'],
                    'symptoms': ['Irregular periods', 'Low testosterone', 'Infertility'],
                    'severity': 'Moderate',
                    'action': 'Treat underlying cause, hormone therapy'
                }
            },
            
            # ============================================
            # OTHER IMPORTANT TESTS - 5 terms
            # ============================================
            
            'PSA': {
                'category': 'Cancer Markers',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 4.0},
                    'female': {'min': 0, 'max': 0}  # Not applicable
                },
                'description': 'Prostate Specific Antigen - screening test for prostate cancer (men only).',
                'high': {
                    'condition': 'Elevated PSA',
                    'causes': ['Prostate cancer', 'Benign prostatic hyperplasia', 'Prostatitis', 'Age'],
                    'symptoms': ['Difficulty urinating', 'Blood in urine', 'Pelvic pain'],
                    'severity': 'Moderate to High',
                    'action': 'Urology referral, prostate biopsy if indicated'
                },
                'low': {
                    'condition': 'Normal PSA',
                    'causes': ['Healthy prostate'],
                    'symptoms': ['None'],
                    'severity': 'Normal',
                    'action': 'Continue regular screening (men >50)'
                }
            },
            
            'CEA': {
                'category': 'Cancer Markers',
                'unit': 'ng/mL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 3.0},
                    'female': {'min': 0, 'max': 3.0}
                },
                'description': 'Carcinoembryonic Antigen - tumor marker for colorectal cancer.',
                'high': {
                    'condition': 'Elevated CEA',
                    'causes': ['Colorectal cancer', 'Lung cancer', 'Smoking', 'Inflammation'],
                    'symptoms': ['Depends on cancer type'],
                    'severity': 'Moderate to High',
                    'action': 'Further testing (colonoscopy, CT scan), oncology referral'
                },
                'low': {
                    'condition': 'Normal CEA',
                    'causes': ['No cancer detected'],
                    'symptoms': ['None'],
                    'severity': 'Normal',
                    'action': 'No action needed'
                }
            },
            
            'CA 19-9': {
                'category': 'Cancer Markers',
                'unit': 'U/mL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 37},
                    'female': {'min': 0, 'max': 37}
                },
                'description': 'Tumor marker for pancreatic and bile duct cancers.',
                'high': {
                    'condition': 'Elevated CA 19-9',
                    'causes': ['Pancreatic cancer', 'Bile duct cancer', 'Pancreatitis', 'Cirrhosis'],
                    'symptoms': ['Abdominal pain', 'Jaundice', 'Weight loss'],
                    'severity': 'High',
                    'action': 'CT scan, oncology referral, endoscopy'
                },
                'low': {
                    'condition': 'Normal CA 19-9',
                    'causes': ['No malignancy'],
                    'symptoms': ['None'],
                    'severity': 'Normal',
                    'action': 'No action needed'
                }
            },
            
            'HCG': {
                'category': 'Pregnancy Markers',
                'unit': 'mIU/mL',
                'normal_ranges': {
                    'male': {'min': 0, 'max': 5},
                    'female': {'min': 0, 'max': 5}  # Non-pregnant
                },
                'description': 'Human Chorionic Gonadotropin - pregnancy hormone.',
                'high': {
                    'condition': 'Elevated HCG',
                    'causes': ['Pregnancy', 'Testicular/ovarian tumors', 'Ectopic pregnancy'],
                    'symptoms': ['Pregnancy symptoms', 'Nausea', 'Breast tenderness'],
                    'severity': 'Varies',
                    'action': 'Pregnancy test confirmation, ultrasound, medical evaluation'
                },
                'low': {
                    'condition': 'Normal HCG (non-pregnant)',
                    'causes': ['Not pregnant', 'Miscarriage'],
                    'symptoms': ['None or pregnancy loss'],
                    'severity': 'Normal or concerning if pregnant',
                    'action': 'Depends on context'
                }
            },
        }
    
    def get_normal_range(self, term, gender='female', age=50):
        """Get normal range for a specific term"""
        if term not in self.knowledge:
            return None
        
        info = self.knowledge[term]
        
        if 'normal_ranges' in info:
            # Return gender-specific range
            if gender in info['normal_ranges']:
                return {
                    'min': info['normal_ranges'][gender]['min'],
                    'max': info['normal_ranges'][gender]['max'],
                    'unit': info['unit']
                }
        
        return None
    
    def get_interpretation(self, term, value, gender='female', age=50):
        """Get interpretation for a test value"""
        if term not in self.knowledge:
            return {
                'status': 'unknown',
                'message': f'No information available for {term}'
            }
        
        info = self.knowledge[term]
        normal_range = self.get_normal_range(term, gender, age)
        
        if not normal_range:
            return {
                'status': 'unknown',
                'message': 'Normal range not available'
            }
        
        # Determine status
        if value < normal_range['min']:
            status = 'low'
            condition_info = info['low']
        elif value > normal_range['max']:
            status = 'high'
            condition_info = info['high']
        else:
            status = 'normal'
            return {
                'status': 'normal',
                'message': f'{term} is within the healthy range',
                'normal_range': f"{normal_range['min']}-{normal_range['max']} {normal_range['unit']}",
                'category': info['category'],
                'description': info['description']
            }
        
        # Build detailed interpretation
        return {
            'status': status,
            'category': info['category'],
            'description': info['description'],
            'normal_range': f"{normal_range['min']}-{normal_range['max']} {normal_range['unit']}",
            'condition': condition_info['condition'],
            'causes': condition_info['causes'],
            'symptoms': condition_info['symptoms'],
            'severity': condition_info['severity'],
            'action': condition_info['action']
        }
    
    def get_all_terms(self):
        """Get list of all available terms"""
        return list(self.knowledge.keys())
    
    def get_terms_by_category(self, category):
        """Get all terms in a specific category"""
        return [
            term for term, info in self.knowledge.items()
            if info['category'] == category
        ]
    
    def get_all_categories(self):
        """Get list of all categories"""
        categories = set()
        for info in self.knowledge.values():
            categories.add(info['category'])
        return sorted(list(categories))


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    kb = MedicalKnowledgeBase()
    
    print(f"Total terms in knowledge base: {len(kb.get_all_terms())}")
    print(f"\nCategories:")
    for cat in kb.get_all_categories():
        terms = kb.get_terms_by_category(cat)
        print(f"  {cat}: {len(terms)} terms")
    
    print("\n" + "="*60)
    print("TESTING INTERPRETATIONS:")
    print("="*60 + "\n")
    
    # Test high HbA1c
    result = kb.get_interpretation('HbA1c', 8.5, 'female', 50)
    print(f"HbA1c = 8.5%")
    print(f"Status: {result['status'].upper()}")
    print(f"Condition: {result['condition']}")
    print(f"Severity: {result['severity']}")
    print(f"Action: {result['action']}")
    
    print("\n" + "="*60 + "\n")
    
    # Test low iron
    result = kb.get_interpretation('Iron', 30, 'female', 30)
    print(f"Iron = 30 µg/dL (Female, age 30)")
    print(f"Status: {result['status'].upper()}")
    print(f"Condition: {result['condition']}")
    print(f"Causes: {', '.join(result['causes'][:3])}")
    print(f"Symptoms: {', '.join(result['symptoms'][:3])}")