"""
Medical Knowledge Base
Contains medical terms, normal ranges, explanations
NO AI REQUIRED - Pure data structure
"""

class MedicalKnowledgeBase:
    
    # ============================================
    # BLOOD TEST PARAMETERS
    # ============================================
    
    BLOOD_TESTS = {
        # ===== COMPLETE BLOOD COUNT (CBC) =====
        "Hemoglobin": {
            "category": "Complete Blood Count",
            "full_name": "Hemoglobin",
            "abbreviation": "Hb",
            "normal_range": {
                "male": {"min": 13.5, "max": 17.5, "unit": "g/dL"},
                "female": {"min": 12.0, "max": 15.5, "unit": "g/dL"},
                "child": {"min": 11.0, "max": 16.0, "unit": "g/dL"}
            },
            "simple_explanation": "Hemoglobin is a protein in your red blood cells that carries oxygen from your lungs to all parts of your body.",
            "why_tested": "To check for anemia, blood disorders, or overall health status",
            "high_means": {
                "condition": "High hemoglobin (Polycythemia)",
                "possible_causes": [
                    "Living at high altitude",
                    "Chronic lung disease",
                    "Dehydration",
                    "Smoking",
                    "Bone marrow disorders"
                ],
                "symptoms": ["Fatigue", "Dizziness", "Headaches", "Blurred vision"],
                "severity": "Medium - Consult doctor"
            },
            "low_means": {
                "condition": "Low hemoglobin (Anemia)",
                "possible_causes": [
                    "Iron deficiency",
                    "Vitamin B12 or folate deficiency",
                    "Blood loss",
                    "Chronic disease",
                    "Bone marrow problems"
                ],
                "symptoms": ["Weakness", "Pale skin", "Shortness of breath", "Cold hands/feet"],
                "severity": "Medium to High - Medical attention needed"
            },
            "next_steps": {
                "if_high": "Consult doctor for further tests, reduce smoking, check oxygen levels",
                "if_low": "Iron supplements, vitamin B12 tests, check for internal bleeding"
            }
        },

        "RBC": {
            "category": "Complete Blood Count",
            "full_name": "Red Blood Cell Count",
            "abbreviation": "RBC",
            "normal_range": {
                "male": {"min": 4.5, "max": 5.9, "unit": "million cells/µL"},
                "female": {"min": 4.1, "max": 5.1, "unit": "million cells/µL"}
            },
            "simple_explanation": "Red blood cells carry oxygen throughout your body. This measures how many you have.",
            "why_tested": "To detect anemia, blood disorders, or hydration status",
            "high_means": {
                "condition": "High RBC count",
                "possible_causes": ["Dehydration", "Lung disease", "Heart disease", "Kidney tumor", "Smoking"],
                "symptoms": ["Fatigue", "Joint pain", "Itching after shower"],
                "severity": "Medium"
            },
            "low_means": {
                "condition": "Low RBC count (Anemia)",
                "possible_causes": ["Blood loss", "Bone marrow failure", "Nutritional deficiency", "Kidney disease"],
                "symptoms": ["Fatigue", "Weakness", "Pale skin"],
                "severity": "Medium to High"
            }
        },

        "WBC": {
            "category": "Complete Blood Count",
            "full_name": "White Blood Cell Count",
            "abbreviation": "WBC",
            "normal_range": {
                "all": {"min": 4000, "max": 11000, "unit": "cells/µL"}
            },
            "simple_explanation": "White blood cells fight infections and protect your body from disease.",
            "why_tested": "To check immune system health and detect infections or immune disorders",
            "high_means": {
                "condition": "High WBC count (Leukocytosis)",
                "possible_causes": [
                    "Bacterial or viral infection",
                    "Inflammation",
                    "Stress",
                    "Allergic reaction",
                    "Leukemia (rarely)"
                ],
                "symptoms": ["Fever", "Fatigue", "Body aches", "Night sweats"],
                "severity": "Low to High depending on count"
            },
            "low_means": {
                "condition": "Low WBC count (Leukopenia)",
                "possible_causes": [
                    "Viral infections",
                    "Bone marrow disorders",
                    "Autoimmune diseases",
                    "Certain medications",
                    "Severe infections"
                ],
                "symptoms": ["Frequent infections", "Fever", "Weakness"],
                "severity": "Medium to High"
            }
        },

        "Platelets": {
            "category": "Complete Blood Count",
            "full_name": "Platelet Count",
            "abbreviation": "PLT",
            "normal_range": {
                "all": {"min": 150000, "max": 400000, "unit": "cells/µL"}
            },
            "simple_explanation": "Platelets help your blood clot to stop bleeding when you get injured.",
            "why_tested": "To check blood clotting ability and diagnose bleeding disorders",
            "high_means": {
                "condition": "High platelet count (Thrombocytosis)",
                "possible_causes": ["Iron deficiency", "Cancer", "Infection", "Inflammation"],
                "symptoms": ["Headache", "Dizziness", "Chest pain", "Blood clots"],
                "severity": "Medium"
            },
            "low_means": {
                "condition": "Low platelet count (Thrombocytopenia)",
                "possible_causes": ["Viral infections", "Leukemia", "Immune disorders", "Medications"],
                "symptoms": ["Easy bruising", "Prolonged bleeding", "Nosebleeds"],
                "severity": "Medium to High"
            }
        },

        "Hematocrit": {
            "category": "Complete Blood Count",
            "full_name": "Hematocrit",
            "abbreviation": "HCT",
            "normal_range": {
                "male": {"min": 38.8, "max": 50.0, "unit": "%"},
                "female": {"min": 34.9, "max": 44.5, "unit": "%"}
            },
            "simple_explanation": "Hematocrit measures the percentage of your blood made up of red blood cells.",
            "why_tested": "To diagnose anemia, dehydration, or blood disorders",
            "high_means": {
                "condition": "High hematocrit",
                "possible_causes": ["Dehydration", "Lung disease", "Living at high altitude"],
                "severity": "Low to Medium"
            },
            "low_means": {
                "condition": "Low hematocrit",
                "possible_causes": ["Anemia", "Blood loss", "Nutritional deficiency"],
                "severity": "Medium"
            }
        },

        # ===== METABOLIC PANEL =====
        "Glucose": {
            "category": "Metabolic Panel",
            "full_name": "Blood Glucose (Fasting)",
            "abbreviation": "FBS",
            "normal_range": {
                "all": {"min": 70, "max": 100, "unit": "mg/dL"},  # FIXED: Added "all" key
                "fasting": {"min": 70, "max": 100, "unit": "mg/dL"},
                "random": {"min": 70, "max": 140, "unit": "mg/dL"}
            },
            "simple_explanation": "Blood sugar level - the amount of glucose (sugar) in your blood.",
            "why_tested": "To screen for diabetes, prediabetes, or monitor blood sugar control",
            "high_means": {
                "condition": "High blood sugar (Hyperglycemia)",
                "possible_causes": ["Diabetes", "Prediabetes", "Stress", "Medications", "Poor diet"],
                "symptoms": ["Increased thirst", "Frequent urination", "Blurred vision", "Fatigue"],
                "severity": "High if >126 mg/dL fasting",
                "categories": {
                    "normal": {"max": 100},
                    "prediabetes": {"min": 100, "max": 125},
                    "diabetes": {"min": 126}
                }
            },
            "low_means": {
                "condition": "Low blood sugar (Hypoglycemia)",
                "possible_causes": ["Too much insulin", "Skipped meals", "Excessive exercise", "Alcohol"],
                "symptoms": ["Shakiness", "Sweating", "Confusion", "Dizziness"],
                "severity": "High if <70 mg/dL"
            },
            "next_steps": {
                "if_high": "Consult doctor, HbA1c test, lifestyle changes, possible medication",
                "if_low": "Eat immediately, check insulin dosage, frequent monitoring"
            }
        },

        "HbA1c": {
            "category": "Metabolic Panel",
            "full_name": "Glycated Hemoglobin",
            "abbreviation": "HbA1c",
            "normal_range": {
                "all": {"min": 4.0, "max": 5.6, "unit": "%"}
            },
            "simple_explanation": "Average blood sugar level over the past 2-3 months. Better indicator than single glucose test.",
            "why_tested": "To diagnose diabetes and monitor long-term blood sugar control",
            "high_means": {
                "condition": "Poor blood sugar control",
                "categories": {
                    "normal": {"max": 5.6},
                    "prediabetes": {"min": 5.7, "max": 6.4},
                    "diabetes": {"min": 6.5}
                },
                "severity": "High"
            }
        },

        "Creatinine": {
            "category": "Kidney Function",
            "full_name": "Serum Creatinine",
            "abbreviation": "Cr",
            "normal_range": {
                "male": {"min": 0.7, "max": 1.3, "unit": "mg/dL"},
                "female": {"min": 0.6, "max": 1.1, "unit": "mg/dL"}
            },
            "simple_explanation": "Waste product filtered by kidneys. High levels indicate kidney problems.",
            "why_tested": "To check kidney function and detect kidney disease",
            "high_means": {
                "condition": "Impaired kidney function",
                "possible_causes": ["Kidney disease", "Dehydration", "High protein diet", "Medications"],
                "symptoms": ["Swelling", "Fatigue", "Changes in urination"],
                "severity": "Medium to High"
            },
            "low_means": {
                "condition": "Usually not concerning",
                "possible_causes": ["Low muscle mass", "Pregnancy"],
                "severity": "Low"
            }
        },

        "BUN": {
            "category": "Kidney Function",
            "full_name": "Blood Urea Nitrogen",
            "abbreviation": "BUN",
            "normal_range": {
                "all": {"min": 7, "max": 20, "unit": "mg/dL"}
            },
            "simple_explanation": "Measures waste product from protein breakdown. Indicates kidney function.",
            "why_tested": "To evaluate kidney function",
            "high_means": {
                "condition": "Possible kidney dysfunction",
                "possible_causes": ["Kidney disease", "Dehydration", "High protein diet", "Heart failure"],
                "severity": "Medium"
            }
        },

        # ===== LIPID PROFILE =====
        "Total Cholesterol": {
            "category": "Lipid Profile",
            "full_name": "Total Cholesterol",
            "abbreviation": "TC",
            "normal_range": {
                "all": {"min": 0, "max": 200, "unit": "mg/dL"}
            },
            "simple_explanation": "Total amount of cholesterol (fatty substance) in your blood.",
            "why_tested": "To assess heart disease risk",
            "high_means": {
                "condition": "High cholesterol",
                "possible_causes": ["Poor diet", "Lack of exercise", "Genetics", "Obesity"],
                "symptoms": ["Usually none - 'silent' condition"],
                "severity": "Medium",
                "categories": {
                    "desirable": {"max": 200},
                    "borderline_high": {"min": 200, "max": 239},
                    "high": {"min": 240}
                }
            }
        },

        "LDL": {
            "category": "Lipid Profile",
            "full_name": "Low-Density Lipoprotein",
            "abbreviation": "LDL",
            "normal_range": {
                "all": {"min": 0, "max": 100, "unit": "mg/dL"}
            },
            "simple_explanation": "'Bad' cholesterol that can clog arteries and increase heart disease risk.",
            "why_tested": "To assess cardiovascular disease risk",
            "high_means": {
                "condition": "High LDL cholesterol",
                "possible_causes": ["Unhealthy diet", "Sedentary lifestyle", "Genetics"],
                "severity": "Medium",
                "categories": {
                    "optimal": {"max": 100},
                    "near_optimal": {"min": 100, "max": 129},
                    "borderline_high": {"min": 130, "max": 159},
                    "high": {"min": 160, "max": 189},
                    "very_high": {"min": 190}
                }
            }
        },

        "HDL": {
            "category": "Lipid Profile",
            "full_name": "High-Density Lipoprotein",
            "abbreviation": "HDL",
            "normal_range": {
                "male": {"min": 40, "max": 999, "unit": "mg/dL"},
                "female": {"min": 50, "max": 999, "unit": "mg/dL"}
            },
            "simple_explanation": "'Good' cholesterol that removes bad cholesterol from arteries.",
            "why_tested": "Higher is better - protects against heart disease",
            "low_means": {
                "condition": "Low HDL cholesterol",
                "possible_causes": ["Smoking", "Obesity", "Lack of exercise"],
                "severity": "Medium",
                "note": "Below 40 mg/dL increases heart disease risk"
            },
            "high_means": {
                "condition": "High HDL (Good!)",
                "note": "Higher HDL is protective against heart disease",
                "severity": "None - this is good"
            }
        },

        "Triglycerides": {
            "category": "Lipid Profile",
            "full_name": "Triglycerides",
            "abbreviation": "TG",
            "normal_range": {
                "all": {"min": 0, "max": 150, "unit": "mg/dL"}
            },
            "simple_explanation": "Type of fat in blood. High levels increase heart disease risk.",
            "why_tested": "To assess cardiovascular disease risk",
            "high_means": {
                "condition": "High triglycerides",
                "possible_causes": ["Excess calories", "Alcohol", "Diabetes", "Obesity"],
                "severity": "Medium",
                "categories": {
                    "normal": {"max": 150},
                    "borderline_high": {"min": 150, "max": 199},
                    "high": {"min": 200, "max": 499},
                    "very_high": {"min": 500}
                }
            }
        },

        # ===== LIVER FUNCTION =====
        "ALT": {
            "category": "Liver Function",
            "full_name": "Alanine Aminotransferase",
            "abbreviation": "ALT/SGPT",
            "normal_range": {
                "male": {"min": 7, "max": 55, "unit": "U/L"},
                "female": {"min": 7, "max": 45, "unit": "U/L"}
            },
            "simple_explanation": "Enzyme found mainly in liver. High levels indicate liver damage.",
            "why_tested": "To detect liver damage or disease",
            "high_means": {
                "condition": "Liver damage or inflammation",
                "possible_causes": ["Hepatitis", "Fatty liver", "Alcohol abuse", "Medications"],
                "severity": "Medium to High"
            }
        },

        "AST": {
            "category": "Liver Function",
            "full_name": "Aspartate Aminotransferase",
            "abbreviation": "AST/SGOT",
            "normal_range": {
                "all": {"min": 8, "max": 48, "unit": "U/L"}
            },
            "simple_explanation": "Enzyme found in liver and heart. Elevated in liver or heart damage.",
            "why_tested": "To detect liver or heart problems",
            "high_means": {
                "condition": "Liver or heart damage",
                "possible_causes": ["Hepatitis", "Heart attack", "Muscle injury", "Alcohol"],
                "severity": "Medium to High"
            }
        },

        "Bilirubin": {
            "category": "Liver Function",
            "full_name": "Total Bilirubin",
            "abbreviation": "TB",
            "normal_range": {
                "all": {"min": 0.1, "max": 1.2, "unit": "mg/dL"}
            },
            "simple_explanation": "Yellow pigment from red blood cell breakdown. High levels cause jaundice.",
            "why_tested": "To check liver function and diagnose jaundice",
            "high_means": {
                "condition": "Jaundice/liver problems",
                "possible_causes": ["Liver disease", "Bile duct blockage", "Hemolytic anemia"],
                "symptoms": ["Yellow skin/eyes", "Dark urine", "Pale stools"],
                "severity": "Medium to High"
            }
        },

        # ===== THYROID FUNCTION =====
        "TSH": {
            "category": "Thyroid Function",
            "full_name": "Thyroid Stimulating Hormone",
            "abbreviation": "TSH",
            "normal_range": {
                "all": {"min": 0.4, "max": 4.0, "unit": "mIU/L"}
            },
            "simple_explanation": "Hormone that controls thyroid gland function. Indicates thyroid health.",
            "why_tested": "To diagnose thyroid disorders",
            "high_means": {
                "condition": "Hypothyroidism (underactive thyroid)",
                "possible_causes": ["Hashimoto's disease", "Iodine deficiency", "Thyroid damage"],
                "symptoms": ["Fatigue", "Weight gain", "Cold sensitivity", "Depression"],
                "severity": "Medium"
            },
            "low_means": {
                "condition": "Hyperthyroidism (overactive thyroid)",
                "possible_causes": ["Graves' disease", "Thyroid nodules", "Thyroiditis"],
                "symptoms": ["Weight loss", "Rapid heartbeat", "Anxiety", "Heat sensitivity"],
                "severity": "Medium"
            }
        },

        "T3": {
            "category": "Thyroid Function",
            "full_name": "Triiodothyronine",
            "abbreviation": "T3",
            "normal_range": {
                "all": {"min": 80, "max": 200, "unit": "ng/dL"}
            },
            "simple_explanation": "Active thyroid hormone that regulates metabolism.",
            "why_tested": "To diagnose hyperthyroidism or monitor thyroid treatment"
        },

        "T4": {
            "category": "Thyroid Function",
            "full_name": "Thyroxine",
            "abbreviation": "T4",
            "normal_range": {
                "all": {"min": 5.0, "max": 12.0, "unit": "µg/dL"}
            },
            "simple_explanation": "Main thyroid hormone that regulates metabolism and energy.",
            "why_tested": "To evaluate thyroid function"
        },

        # ===== ELECTROLYTES =====
        "Sodium": {
            "category": "Electrolytes",
            "full_name": "Serum Sodium",
            "abbreviation": "Na+",
            "normal_range": {
                "all": {"min": 135, "max": 145, "unit": "mEq/L"}
            },
            "simple_explanation": "Essential mineral for nerve and muscle function, fluid balance.",
            "why_tested": "To check fluid balance and kidney function",
            "high_means": {
                "condition": "Hypernatremia",
                "possible_causes": ["Dehydration", "Kidney disease", "Diabetes insipidus"],
                "severity": "Medium to High"
            },
            "low_means": {
                "condition": "Hyponatremia",
                "possible_causes": ["Excess fluid intake", "Kidney disease", "Heart failure"],
                "severity": "Medium to High"
            }
        },

        "Potassium": {
            "category": "Electrolytes",
            "full_name": "Serum Potassium",
            "abbreviation": "K+",
            "normal_range": {
                "all": {"min": 3.5, "max": 5.0, "unit": "mEq/L"}
            },
            "simple_explanation": "Critical for heart rhythm, muscle function, and nerve signals.",
            "why_tested": "To check heart and kidney function",
            "high_means": {
                "condition": "Hyperkalemia",
                "possible_causes": ["Kidney disease", "Medications", "Dehydration"],
                "symptoms": ["Irregular heartbeat", "Weakness"],
                "severity": "High - can be life-threatening"
            },
            "low_means": {
                "condition": "Hypokalemia",
                "possible_causes": ["Diarrhea", "Vomiting", "Diuretics", "Low dietary intake"],
                "symptoms": ["Muscle cramps", "Weakness", "Fatigue"],
                "severity": "Medium to High"
            }
        },

        # ===== VITAMINS & MINERALS =====
        "Vitamin D": {
            "category": "Vitamins",
            "full_name": "25-Hydroxyvitamin D",
            "abbreviation": "Vit D",
            "normal_range": {
                "all": {"min": 30, "max": 100, "unit": "ng/mL"}
            },
            "simple_explanation": "Vitamin essential for bone health, immune function, and mood.",
            "why_tested": "To check for deficiency, especially in limited sun exposure",
            "low_means": {
                "condition": "Vitamin D deficiency",
                "possible_causes": ["Limited sun exposure", "Poor diet", "Malabsorption"],
                "symptoms": ["Bone pain", "Muscle weakness", "Fatigue", "Depression"],
                "severity": "Medium",
                "categories": {
                    "deficient": {"max": 20},
                    "insufficient": {"min": 20, "max": 29},
                    "sufficient": {"min": 30}
                }
            }
        },

        "Vitamin B12": {
            "category": "Vitamins",
            "full_name": "Cobalamin",
            "abbreviation": "B12",
            "normal_range": {
                "all": {"min": 200, "max": 900, "unit": "pg/mL"}
            },
            "simple_explanation": "Vitamin essential for nerve function, red blood cell formation, and DNA synthesis.",
            "why_tested": "To diagnose anemia or nerve problems",
            "low_means": {
                "condition": "B12 deficiency",
                "possible_causes": ["Vegetarian diet", "Pernicious anemia", "Malabsorption"],
                "symptoms": ["Fatigue", "Numbness", "Memory problems"],
                "severity": "Medium"
            }
        },

        "Iron": {
            "category": "Minerals",
            "full_name": "Serum Iron",
            "abbreviation": "Fe",
            "normal_range": {
                "male": {"min": 65, "max": 175, "unit": "µg/dL"},
                "female": {"min": 50, "max": 170, "unit": "µg/dL"}
            },
            "simple_explanation": "Essential mineral for making hemoglobin and carrying oxygen.",
            "why_tested": "To diagnose iron deficiency anemia",
            "low_means": {
                "condition": "Iron deficiency",
                "possible_causes": ["Poor diet", "Blood loss", "Pregnancy", "Malabsorption"],
                "symptoms": ["Fatigue", "Pale skin", "Brittle nails", "Cold hands"],
                "severity": "Medium"
            }
        },

        "Calcium": {
            "category": "Minerals",
            "full_name": "Serum Calcium",
            "abbreviation": "Ca",
            "normal_range": {
                "all": {"min": 8.5, "max": 10.5, "unit": "mg/dL"}
            },
            "simple_explanation": "Essential for bones, teeth, muscle function, and nerve signals.",
            "why_tested": "To check bone health and parathyroid function",
            "high_means": {
                "condition": "Hypercalcemia",
                "possible_causes": ["Hyperparathyroidism", "Cancer", "Too much vitamin D"],
                "severity": "Medium to High"
            },
            "low_means": {
                "condition": "Hypocalcemia",
                "possible_causes": ["Vitamin D deficiency", "Hypoparathyroidism", "Kidney disease"],
                "severity": "Medium"
            }
        },

        # ===== URIC ACID =====
        "Uric Acid": {
            "category": "Metabolic",
            "full_name": "Serum Uric Acid",
            "abbreviation": "UA",
            "normal_range": {
                "male": {"min": 3.5, "max": 7.2, "unit": "mg/dL"},
                "female": {"min": 2.6, "max": 6.0, "unit": "mg/dL"}
            },
            "simple_explanation": "Waste product from purine breakdown. High levels cause gout.",
            "why_tested": "To diagnose gout or monitor kidney function",
            "high_means": {
                "condition": "Hyperuricemia (High uric acid)",
                "possible_causes": ["High purine diet", "Kidney disease", "Alcohol", "Genetics"],
                "symptoms": ["Joint pain (gout)", "Kidney stones"],
                "severity": "Medium",
                "next_steps": "Low purine diet, increase water intake, medication if needed"
            }
        },

        # ===== CARDIAC MARKERS =====
        "Troponin": {
            "category": "Cardiac Markers",
            "full_name": "Cardiac Troponin",
            "abbreviation": "cTn",
            "normal_range": {
                "all": {"min": 0, "max": 0.04, "unit": "ng/mL"}
            },
            "simple_explanation": "Protein released when heart muscle is damaged. Key heart attack indicator.",
            "why_tested": "To diagnose heart attack",
            "high_means": {
                "condition": "Heart muscle damage",
                "possible_causes": ["Heart attack", "Heart failure", "Myocarditis"],
                "severity": "EMERGENCY - Immediate medical attention"
            }
        },

        # ===== INFLAMMATION MARKERS =====
        "CRP": {
            "category": "Inflammation",
            "full_name": "C-Reactive Protein",
            "abbreviation": "CRP",
            "normal_range": {
                "all": {"min": 0, "max": 3.0, "unit": "mg/L"}
            },
            "simple_explanation": "Marker of inflammation in the body.",
            "why_tested": "To detect inflammation or infection",
            "high_means": {
                "condition": "Inflammation or infection",
                "possible_causes": ["Infection", "Autoimmune disease", "Heart disease risk"],
                "severity": "Medium",
                "categories": {
                    "low_risk": {"max": 1.0},
                    "average_risk": {"min": 1.0, "max": 3.0},
                    "high_risk": {"min": 3.0}
                }
            }
        },

        "ESR": {
            "category": "Inflammation",
            "full_name": "Erythrocyte Sedimentation Rate",
            "abbreviation": "ESR",
            "normal_range": {
                "male": {"min": 0, "max": 15, "unit": "mm/hr"},
                "female": {"min": 0, "max": 20, "unit": "mm/hr"}
            },
            "simple_explanation": "Measures inflammation level in the body.",
            "why_tested": "To detect inflammation or monitor disease activity",
            "high_means": {
                "condition": "Inflammation",
                "possible_causes": ["Infection", "Autoimmune disease", "Cancer"],
                "severity": "Medium"
            }
        }
    }

    # ============================================
    # HELPER METHODS
    # ============================================
    
    @classmethod
    def get_term_info(cls, term_name):
        """Get complete information about a medical term"""
        return cls.BLOOD_TESTS.get(term_name)
    
    @classmethod
    def get_normal_range(cls, term_name, gender="all", age_group="adult"):
        """Get normal range for a specific term"""
        term_info = cls.get_term_info(term_name)
        if not term_info:
            return None
        
        normal_range = term_info.get("normal_range", {})
        
        # Special case for Glucose - use "all" by default
        if term_name == "Glucose" and "all" in normal_range:
            return normal_range["all"]
        
        # Try gender-specific first
        if gender in normal_range:
            return normal_range[gender]
        
        # Fall back to 'all'
        if "all" in normal_range:
            return normal_range["all"]
        
        # For age-specific (like child)
        if age_group in normal_range:
            return normal_range[age_group]
        
        return None
    
    @classmethod
    def check_value_status(cls, term_name, value, gender="all"):
        """
        Check if a value is normal, high, or low
        Returns: "normal", "high", "low", or "unknown"
        """
        normal_range = cls.get_normal_range(term_name, gender)
        
        if not normal_range:
            return "unknown"
        
        min_val = normal_range.get("min", 0)
        max_val = normal_range.get("max", float('inf'))
        
        if value < min_val:
            return "low"
        elif value > max_val:
            return "high"
        else:
            return "normal"
    
    @classmethod
    def get_interpretation(cls, term_name, value, gender="all"):
        """
        Get detailed interpretation of a test result
        Returns dict with status, explanation, severity, recommendations
        """
        term_info = cls.get_term_info(term_name)
        if not term_info:
            return {"error": "Unknown medical term"}
        
        status = cls.check_value_status(term_name, value, gender)
        normal_range = cls.get_normal_range(term_name, gender)
        
        interpretation = {
            "term": term_name,
            "value": value,
            "unit": normal_range.get("unit", "") if normal_range else "",
            "status": status,
            "normal_range": f"{normal_range.get('min', 0)} - {normal_range.get('max', 0)} {normal_range.get('unit', '')}" if normal_range else "Unknown",
            "explanation": term_info.get("simple_explanation", ""),
            "category": term_info.get("category", ""),
        }
        
        if status == "high":
            high_info = term_info.get("high_means", {})
            interpretation.update({
                "condition": high_info.get("condition", "Elevated levels"),
                "possible_causes": high_info.get("possible_causes", []),
                "symptoms": high_info.get("symptoms", []),
                "severity": high_info.get("severity", "Consult doctor"),
                "next_steps": term_info.get("next_steps", {}).get("if_high", "Consult your doctor")
            })
        
        elif status == "low":
            low_info = term_info.get("low_means", {})
            interpretation.update({
                "condition": low_info.get("condition", "Low levels"),
                "possible_causes": low_info.get("possible_causes", []),
                "symptoms": low_info.get("symptoms", []),
                "severity": low_info.get("severity", "Consult doctor"),
                "next_steps": term_info.get("next_steps", {}).get("if_low", "Consult your doctor")
            })
        
        else:  # normal
            interpretation.update({
                "condition": "Within normal range",
                "message": "Your levels are healthy",
                "severity": "None"
            })
        
        return interpretation
    
    @classmethod
    def get_all_terms(cls):
        """Get list of all available medical terms"""
        return list(cls.BLOOD_TESTS.keys())
    
    @classmethod
    def get_terms_by_category(cls, category):
        """Get all terms in a specific category"""
        return [
            term for term, info in cls.BLOOD_TESTS.items()
            if info.get("category") == category
        ]
    
    @classmethod
    def get_all_categories(cls):
        """Get list of all categories"""
        categories = set()
        for info in cls.BLOOD_TESTS.values():
            categories.add(info.get("category", "Other"))
        return sorted(list(categories))


# ============================================
# USAGE EXAMPLES (for testing)
# ============================================

if __name__ == "__main__":
    kb = MedicalKnowledgeBase()
    
    # Example 1: Get term info
    print("=" * 50)
    print("EXAMPLE 1: Get Hemoglobin Info")
    print("=" * 50)
    hb_info = kb.get_term_info("Hemoglobin")
    print(f"Full Name: {hb_info['full_name']}")
    print(f"Explanation: {hb_info['simple_explanation']}")
    print()
    
    # Example 2: Check value status
    print("=" * 50)
    print("EXAMPLE 2: Check Blood Sugar Value")
    print("=" * 50)
    glucose_value = 120
    status = kb.check_value_status("Glucose", glucose_value)
    print(f"Blood Sugar: {glucose_value} mg/dL")
    print(f"Status: {status}")
    print()
    
    # Example 3: Get full interpretation
    print("=" * 50)
    print("EXAMPLE 3: Full Interpretation")
    print("=" * 50)
    interpretation = kb.get_interpretation("Hemoglobin", 10.5, gender="female")
    print(f"Term: {interpretation['term']}")
    print(f"Value: {interpretation['value']} {interpretation['unit']}")
    print(f"Status: {interpretation['status']}")
    print(f"Normal Range: {interpretation['normal_range']}")
    print(f"Condition: {interpretation.get('condition', 'N/A')}")
    print(f"Possible Causes: {', '.join(interpretation.get('possible_causes', []))}")
    print()
    
    # Example 4: Get all categories
    print("=" * 50)
    print("EXAMPLE 4: All Categories")
    print("=" * 50)
    categories = kb.get_all_categories()
    print(f"Available categories: {', '.join(categories)}")
    print()
    
    # Example 5: Get terms by category
    print("=" * 50)
    print("EXAMPLE 5: Lipid Profile Tests")
    print("=" * 50)
    lipid_tests = kb.get_terms_by_category("Lipid Profile")
    print(f"Lipid tests: {', '.join(lipid_tests)}")