"""
Template-based Summary Generator
Generates patient-friendly summaries using rule-based templates
NO AI REQUIRED - Pure template logic
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from medical_knowledge import MedicalKnowledgeBase
except ImportError:
    from utils.medical_knowledge import MedicalKnowledgeBase


class TemplateSummarizer:
    
    def __init__(self):
        self.kb = MedicalKnowledgeBase()
    
    def generate_summary(self, parsed_report):
        """
        Generate a comprehensive summary from parsed report data
        """
        summary_parts = []
        
        # Introduction
        summary_parts.append(self._generate_introduction())
        
        # Report overview
        summary_parts.append(self._generate_overview(parsed_report))
        
        # Detailed test explanations
        summary_parts.append(self._generate_detailed_test_explanations(parsed_report))
        
        # Overall summary
        summary_parts.append(self._generate_overall_summary(parsed_report))
        
        # Next steps
        summary_parts.append(self._generate_next_steps(parsed_report))
        
        # Combine all parts
        return "\n\n".join(summary_parts)
    
    def _generate_introduction(self):
        """Generate friendly introduction"""
        return """Looking at a medical report can feel overwhelming with all the technical terms and numbers. Don't worry - I'm here to help you understand what everything means in plain, simple language.

Let's go through your test results together, step by step."""
    
    def _generate_overview(self, parsed_report):
        """Generate report overview"""
        report_type = parsed_report.get('report_type', 'Medical Report')
        total_tests = parsed_report.get('total_tests', 0)
        
        # Get category description
        category_descriptions = {
            'Lipid Profile': 'These tests measure the fats (lipids) in your blood, including cholesterol and triglycerides. These values help assess your risk for heart disease and stroke.',
            'Complete Blood Count (CBC)': 'These tests measure different components of your blood, including red blood cells, white blood cells, and platelets. They help detect anemia, infections, and blood disorders.',
            'Thyroid Function Test': 'These tests measure thyroid hormone levels to assess how well your thyroid gland is working. The thyroid controls your metabolism.',
            'Liver Function Test': 'These tests check how well your liver is working. The liver filters toxins, makes proteins, and helps with digestion.',
            'Kidney Function Test': 'These tests evaluate how well your kidneys are filtering waste from your blood.',
            'Diabetes Screening / Lipid Profile': 'These tests check your blood sugar levels and cholesterol to assess diabetes risk and heart health.',
            'Metabolic Panel': 'These tests measure various substances in your blood to evaluate overall metabolism and organ function.',
        }
        
        description = category_descriptions.get(report_type, 'This medical report contains various laboratory tests to assess your health.')
        
        return f"""## What is this report?

This is a **{report_type}** from a medical laboratory. {description}

**Total tests performed:** {total_tests}"""
    
    def _generate_detailed_test_explanations(self, parsed_report):
        """Generate detailed explanation for each test result"""
        categorized = parsed_report.get('categorized', {})
        all_results = parsed_report.get('all_results', [])
        gender = parsed_report.get('patient_info', {}).get('gender', 'female')
        age = parsed_report.get('patient_info', {}).get('age', 50)
        
        # Group tests by category
        tests_by_category = {}
        for result in all_results:
            term = result['term']
            
            # ✅ FIX: Use get_interpretation instead of get_term_info
            interpretation = self.kb.get_interpretation(term, result['value'], gender, age)
            
            if interpretation and 'category' in interpretation:
                category = interpretation['category']
                if category not in tests_by_category:
                    tests_by_category[category] = []
                tests_by_category[category].append((result, interpretation))
        
        # Generate output
        output = ["## Let's look at your results:"]
        
        # Category descriptions
        category_intros = {
            'Metabolic Panel': "**What this tests:** Your blood sugar and kidney function. This helps detect diabetes and metabolic disorders.",
            'Complete Blood Count (CBC)': "**What this tests:** Your blood cell counts. This helps detect anemia, infections, and blood disorders.",
            'Lipid Profile': "**What this tests:** Your cholesterol and fat levels. These affect your heart health and risk of cardiovascular disease.",
            'Liver Function': "**What this tests:** How well your liver is working. The liver filters toxins, makes proteins, and helps with digestion.",
            'Kidney Function': "**What this tests:** How well your kidneys are filtering waste from your blood.",
            'Thyroid Function': "**What this tests:** Thyroid hormone levels that control your metabolism.",
            'Cardiac Markers': "**What this tests:** Markers that indicate heart damage or stress. Useful for detecting heart attacks and heart disease.",
            'Vitamins & Minerals': "**What this tests:** Essential nutrients needed for various body functions.",
            'Electrolytes': "**What this tests:** Minerals that regulate fluid balance and nerve/muscle function.",
            'Hormones': "**What this tests:** Hormone levels that regulate various body processes.",
        }
        
        for category, tests in sorted(tests_by_category.items()):
            output.append(f"\n### {category}")
            
            # Add category intro if available
            if category in category_intros:
                output.append(f"\n{category_intros[category]}")
            
            for result, interpretation in tests:
                output.append(self._format_test_result(result, interpretation, gender, age))
        
        return "\n".join(output)
    
    def _format_test_result(self, result, interpretation, gender, age):
        """Format a single test result with interpretation"""
        term = result['term']
        value = result['value']
        unit = result.get('unit', '')
        status = interpretation.get('status', 'unknown')
        
        # Status emoji
        if status == 'normal':
            emoji = "✅"
            status_text = "**(Normal)**"
        elif status == 'high':
            emoji = "⚠️"
            status_text = "**(Higher than normal)**"
        elif status == 'low':
            emoji = "⚠️"
            status_text = "**(Lower than normal)**"
        else:
            emoji = "❓"
            status_text = ""
        
        # Build output
        lines = [
            f"\n#### {term}",
            f"\n{emoji} **Your result:** {value} {unit} {status_text}",
        ]
        
        # Add normal range
        if 'normal_range' in interpretation:
            lines.append(f"\n**Normal range:** {interpretation['normal_range']}")
        
        # Add description
        if 'description' in interpretation:
            lines.append(f"\n**What is {term}?**\n\n{interpretation['description']}")
        
        # Add interpretation for abnormal values
        if status != 'normal':
            lines.append(f"\n**What this means for you:**\n")
            
            if 'condition' in interpretation:
                lines.append(f"\nYour {term} level indicates: **{interpretation['condition']}**.")
            
            if 'causes' in interpretation and interpretation['causes']:
                causes_text = "\n".join([f"• {cause}" for cause in interpretation['causes'][:3]])
                lines.append(f"\n**Common reasons for this:**\n{causes_text}")
            
            if 'symptoms' in interpretation and interpretation['symptoms']:
                symptoms_text = "\n".join([f"• {symptom}" for symptom in interpretation['symptoms'][:3]])
                lines.append(f"\n**Symptoms that might occur:**\n{symptoms_text}")
            
            if 'action' in interpretation:
                lines.append(f"\n**Recommended action:** {interpretation['action']}")
        else:
            # Normal value
            lines.append(f"\n**What this means for you:**\n")
            lines.append(f"\nYour {term} level is within the healthy range. This is excellent! It suggests this aspect of your health is functioning well.")
        
        lines.append("\n---\n")
        
        return "\n".join(lines)
    
    def _generate_overall_summary(self, parsed_report):
        """Generate overall health summary"""
        categorized = parsed_report.get('categorized', {})
        
        normal_count = len(categorized.get('normal', []))
        high_count = len(categorized.get('high', []))
        low_count = len(categorized.get('low', []))
        critical_count = len(categorized.get('critical', []))
        total = normal_count + high_count + low_count + critical_count
        
        abnormal_count = high_count + low_count + critical_count
        
        output = ["## Overall Summary"]
        
        if critical_count > 0:
            output.append("\n⚠️ **Important:** Some values require immediate medical attention.")
        elif abnormal_count > 0:
            output.append("\n⚠️ **Note:** Some values are outside the normal range and need attention.")
        else:
            output.append("\n✅ **Great news:** All your test results are within normal ranges!")
        
        output.append(f"\n**Results breakdown:**")
        output.append(f"• Normal values: {normal_count} out of {total}")
        if abnormal_count > 0:
            output.append(f"• Values needing attention: {high_count + low_count}")
        if critical_count > 0:
            output.append(f"• Critical values: {critical_count}")
        
        # Add specific insights
        insights = self._generate_insights(categorized)
        if insights:
            output.append(f"\n{insights}")
        
        return "\n".join(output)
    
    def _generate_insights(self, categorized):
        """Generate specific health insights"""
        insights = []
        
        # Check for common patterns
        high_tests = categorized.get('high', [])
        low_tests = categorized.get('low', [])
        
        # Cholesterol insights
        high_ldl = any(r['term'] == 'LDL' for r in high_tests)
        low_hdl = any(r['term'] == 'HDL' for r in low_tests)
        
        if high_ldl and low_hdl:
            insights.append("**Cholesterol pattern:** You have high 'bad' cholesterol (LDL) and low 'good' cholesterol (HDL). This combination increases heart disease risk. Focus on exercise, healthy fats, and reducing saturated fats.")
        elif high_ldl:
            insights.append("**LDL cholesterol:** Your 'bad' cholesterol is elevated. Reducing saturated fats and increasing exercise can help.")
        elif low_hdl:
            insights.append("**HDL cholesterol:** Your 'good' cholesterol is lower than ideal. Increasing HDL through exercise and healthy fats can benefit heart health.")
        
        # Diabetes risk
        high_hba1c = any(r['term'] == 'HbA1c' for r in high_tests)
        high_glucose = any(r['term'] == 'Glucose' for r in high_tests)
        
        if high_hba1c or high_glucose:
            insights.append("**Blood sugar:** Your blood sugar levels suggest prediabetes or diabetes risk. Lifestyle changes (diet, exercise, weight loss) are crucial.")
        
        # Liver function
        high_alt = any(r['term'] == 'ALT' for r in high_tests)
        high_ast = any(r['term'] == 'AST' for r in high_tests)
        
        if high_alt or high_ast:
            insights.append("**Liver enzymes:** Elevated liver enzymes may indicate liver stress. Avoid alcohol, maintain healthy weight, and follow up with your doctor.")
        
        return "\n\n".join(insights) if insights else ""
    
    def _generate_next_steps(self, parsed_report):
        """Generate recommended next steps"""
        categorized = parsed_report.get('categorized', {})
        critical_count = len(categorized.get('critical', []))
        abnormal_count = len(categorized.get('high', [])) + len(categorized.get('low', []))
        
        output = ["## What to do next:"]
        
        if critical_count > 0:
            output.append("\n🚨 **URGENT:** Contact your doctor today about critical values.")
        
        output.append("\n1. **Schedule a doctor's appointment** to discuss these results in detail.")
        output.append("\n2. **Bring this report** to your appointment so your doctor can review it.")
        
        output.append("\n3. **Ask your doctor about:**")
        output.append("   • What's causing these abnormal values")
        output.append("   • Whether you need additional tests")
        output.append("   • Lifestyle changes that can help")
        output.append("   • Whether medication is needed")
        
        output.append("\n4. **Maintain healthy habits:**")
        output.append("   • Eat a balanced diet rich in fruits and vegetables")
        output.append("   • Exercise regularly (at least 30 minutes daily)")
        output.append("   • Get adequate sleep (7-8 hours)")
        output.append("   • Manage stress through relaxation techniques")
        output.append("   • Stay hydrated")
        
        if abnormal_count > 0:
            output.append("\n5. **Plan for retesting** in 3-6 months to track your progress.")
        
        output.append("\n**Remember:** This summary is for educational purposes. Your doctor will interpret these results in the context of your overall health, symptoms, and medical history to provide personalized care.")
        
        return "\n".join(output)


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    # Test data
    test_data = {
        'report_type': 'Lipid Profile',
        'total_tests': 5,
        'all_results': [
            {'term': 'Total Cholesterol', 'value': 220, 'unit': 'mg/dL'},
            {'term': 'HDL', 'value': 35, 'unit': 'mg/dL'},
            {'term': 'LDL', 'value': 150, 'unit': 'mg/dL'},
            {'term': 'Triglycerides', 'value': 200, 'unit': 'mg/dL'},
            {'term': 'HbA1c', 'value': 6.2, 'unit': '%'},
        ],
        'categorized': {
            'normal': [],
            'high': [
                {'term': 'Total Cholesterol', 'value': 220},
                {'term': 'LDL', 'value': 150},
                {'term': 'Triglycerides', 'value': 200},
                {'term': 'HbA1c', 'value': 6.2},
            ],
            'low': [
                {'term': 'HDL', 'value': 35},
            ],
            'critical': []
        },
        'patient_info': {
            'gender': 'female',
            'age': 50
        }
    }
    
    summarizer = TemplateSummarizer()
    summary = summarizer.generate_summary(test_data)
    
    print("="*60)
    print("GENERATED SUMMARY:")
    print("="*60)
    print(summary)
    print("="*60)
    print(f"\nSummary length: {len(summary)} characters")