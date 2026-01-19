"""
Template-Based Medical Report Summarizer - PROFESSIONAL VERSION
Generates GEMINI-QUALITY summaries WITHOUT AI
Clean, detailed, educational explanations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.medical_knowledge import MedicalKnowledgeBase
except ImportError:
    try:
        from medical_knowledge import MedicalKnowledgeBase
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from medical_knowledge import MedicalKnowledgeBase

class TemplateSummarizer:
    
    def __init__(self):
        self.kb = MedicalKnowledgeBase()
    
    def generate_summary(self, parsed_report):
        """
        Generate PROFESSIONAL, DETAILED summary
        Quality matches Gemini but 100% rule-based
        """
        
        summary_parts = []
        
        # Friendly introduction
        summary_parts.append(self._generate_introduction(parsed_report))
        
        # What is this report?
        summary_parts.append(self._generate_report_overview(parsed_report))
        
        # Detailed explanation of EACH test
        summary_parts.append(self._generate_detailed_test_explanations(parsed_report))
        
        # Overall summary
        summary_parts.append(self._generate_overall_summary(parsed_report))
        
        # Next steps
        summary_parts.append(self._generate_next_steps(parsed_report))
        
        return "\n\n".join(summary_parts)
    
    def _generate_introduction(self, parsed_report):
        """Friendly, welcoming introduction"""
        intro = "Looking at a medical report can feel overwhelming with all the technical terms and numbers. "
        intro += "Don't worry - I'm here to help you understand what everything means in plain, simple language.\n\n"
        intro += "Let's go through your test results together, step by step."
        return intro
    
    def _generate_report_overview(self, parsed_report):
        """Explain what this report is"""
        report_type = parsed_report['report_type']
        total_tests = parsed_report['total_tests']
        
        overview = f"## What is this report?\n\n"
        overview += f"This is a **{report_type}** from a medical laboratory. "
        
        # Explain what each report type tests
        if "Lipid" in report_type:
            overview += "These tests measure the fats (lipids) in your blood, including cholesterol and triglycerides. "
            overview += "These values help assess your risk for heart disease and stroke."
        elif "CBC" in report_type or "Blood Count" in report_type:
            overview += "These tests count different types of cells in your blood. "
            overview += "They help detect infections, anemia, and other blood disorders."
        elif "Thyroid" in report_type:
            overview += "These tests check how well your thyroid gland is working. "
            overview += "The thyroid controls your metabolism and energy levels."
        elif "Liver" in report_type:
            overview += "These tests check how well your liver is functioning. "
            overview += "The liver filters your blood and helps with digestion."
        elif "Diabetes" in report_type:
            overview += "These tests measure your blood sugar levels. "
            overview += "They help detect diabetes or prediabetes."
        else:
            overview += "These tests provide important information about your health."
        
        overview += f"\n\n**Total tests performed:** {total_tests}"
        
        return overview
    
    def _generate_detailed_test_explanations(self, parsed_report):
        """Explain EVERY test in detail (like Gemini does)"""
        
        section = "## Let's look at your results:\n\n"
        
        all_results = parsed_report['all_results']
        
        if not all_results:
            return section + "No test results were detected in the report."
        
        # Group by category for better organization
        categories = {}
        for result in all_results:
            term_info = self.kb.get_term_info(result['term'])
            if term_info:
                category = term_info.get('category', 'Other Tests')
                if category not in categories:
                    categories[category] = []
                categories[category].append(result)
        
        # Generate detailed explanation for each category
        for category, results in categories.items():
            section += f"### {category}\n\n"
            
            # Explain what this category means
            section += self._get_category_explanation(category) + "\n\n"
            
            # Explain each test in this category
            for result in results:
                section += self._explain_single_test(result) + "\n\n"
        
        return section
    
    def _get_category_explanation(self, category):
        """Educational explanation of what each category tests"""
        explanations = {
            "Lipid Profile": "**What this tests:** Your cholesterol and fat levels. These affect your heart health and risk of cardiovascular disease.",
            
            "Complete Blood Count": "**What this tests:** The number and types of cells in your blood. This helps detect infections, anemia, and blood disorders.",
            
            "Thyroid Function": "**What this tests:** How well your thyroid gland works. The thyroid controls your metabolism, energy, and body temperature.",
            
            "Liver Function": "**What this tests:** How well your liver is working. The liver filters toxins, makes proteins, and helps with digestion.",
            
            "Kidney Function": "**What this tests:** How well your kidneys filter waste from your blood. Healthy kidneys are essential for overall health.",
            
            "Metabolic Panel": "**What this tests:** Your blood sugar and kidney function. This helps detect diabetes and metabolic disorders.",
            
            "Cardiac Markers": "**What this tests:** Markers that indicate heart damage or stress. Useful for detecting heart attacks and heart disease.",
            
            "Inflammation": "**What this tests:** Levels of inflammation in your body. High inflammation can indicate infection or chronic disease.",
        }
        
        return explanations.get(category, f"**What this tests:** Important health markers in the {category} category.")
    
    def _explain_single_test(self, result):
        """Detailed explanation of a SINGLE test (Gemini-quality)"""
        term = result['term']
        value = result['value']
        unit = result['unit']
        interp = result['interpretation']
        status = interp['status']
        
        # Start with test name
        explanation = f"#### {term}\n\n"
        
        # Show the result with visual indicator
        if status == 'normal':
            explanation += f"✅ **Your result:** {value} {unit} **(Normal)**\n\n"
        elif status == 'high':
            explanation += f"⚠️ **Your result:** {value} {unit} **(Higher than normal)**\n\n"
        elif status == 'low':
            explanation += f"⚠️ **Your result:** {value} {unit} **(Lower than normal)**\n\n"
        
        # Show normal range
        explanation += f"**Normal range:** {interp['normal_range']}\n\n"
        
        # What is this test?
        explanation += f"**What is {term}?**\n\n"
        explanation += f"{interp['explanation']}\n\n"
        
        # What does YOUR result mean?
        if status == 'normal':
            explanation += f"**What this means for you:**\n\n"
            explanation += f"Your {term} level is within the healthy range. This is excellent! "
            explanation += f"It suggests this aspect of your health is functioning well.\n\n"
        else:
            explanation += f"**What this means for you:**\n\n"
            condition = interp.get('condition', f'{status} {term}')
            explanation += f"Your {term} level indicates: **{condition}**.\n\n"
            
            # Why this might happen
            causes = interp.get('possible_causes', [])
            if causes:
                explanation += f"**Common reasons for this:**\n"
                for cause in causes[:3]:  # Top 3 causes
                    explanation += f"• {cause}\n"
                explanation += "\n"
            
            # What symptoms to watch for
            symptoms = interp.get('symptoms', [])
            if symptoms:
                explanation += f"**Symptoms that might occur:**\n"
                for symptom in symptoms[:3]:  # Top 3 symptoms
                    explanation += f"• {symptom}\n"
                explanation += "\n"
            
            # What to do
            next_steps = interp.get('next_steps', 'Discuss with your doctor')
            explanation += f"**Recommended action:** {next_steps}\n\n"
        
        explanation += "---\n"
        
        return explanation
    
    def _generate_overall_summary(self, parsed_report):
        """Big picture summary of all results"""
        summary = "## Overall Summary\n\n"
        
        categorized = parsed_report['categorized']
        total = parsed_report['total_tests']
        normal_count = len(categorized['normal'])
        abnormal_count = len(categorized['high']) + len(categorized['low'])
        critical_count = len(categorized['critical'])
        
        # Overall health status
        if critical_count > 0:
            summary += "⚠️ **Important:** Some values require immediate medical attention.\n\n"
        elif abnormal_count == 0:
            summary += "✅ **Excellent news!** All your test results are within normal ranges.\n\n"
        elif normal_count > abnormal_count:
            summary += "✓ **Good news overall!** Most of your results are normal, with a few that need attention.\n\n"
        else:
            summary += "⚠️ **Attention needed:** Several values are outside normal range.\n\n"
        
        # Summary breakdown
        summary += f"**Results breakdown:**\n"
        summary += f"• Normal values: {normal_count} out of {total}\n"
        if abnormal_count > 0:
            summary += f"• Values needing attention: {abnormal_count}\n"
        if critical_count > 0:
            summary += f"• Critical values: {critical_count}\n"
        
        summary += "\n"
        
        # Specific health insights
        if any(r['term'] in ['HbA1c', 'Glucose'] for r in categorized['high']):
            summary += "**Blood sugar:** Your blood sugar levels are higher than normal. "
            summary += "This may indicate prediabetes or diabetes. Lifestyle changes and medical guidance can help.\n\n"
        
        if any(r['term'] in ['Total Cholesterol', 'LDL', 'Triglycerides'] for r in categorized['high']):
            summary += "**Heart health:** Your cholesterol levels show some elevation. "
            summary += "This increases cardiovascular risk. Diet, exercise, and potentially medication can improve these values.\n\n"
        
        if any(r['term'] == 'HDL' for r in categorized['low']):
            summary += "**HDL cholesterol:** Your 'good' cholesterol is lower than ideal. "
            summary += "Increasing HDL through exercise and healthy fats can benefit heart health.\n\n"
        
        return summary
    
    def _generate_next_steps(self, parsed_report):
        """What to do with these results"""
        steps = "## What to do next:\n\n"
        
        categorized = parsed_report['categorized']
        
        # Critical values
        if categorized['critical']:
            steps += "🚨 **URGENT:** Contact your doctor today about critical values.\n\n"
        
        # General guidance
        steps += "1. **Schedule a doctor's appointment** to discuss these results in detail.\n\n"
        steps += "2. **Bring this report** to your appointment so your doctor can review it.\n\n"
        
        # Specific recommendations
        if categorized['high'] or categorized['low']:
            steps += "3. **Ask your doctor about:**\n"
            steps += "   • What's causing these abnormal values\n"
            steps += "   • Whether you need additional tests\n"
            steps += "   • Lifestyle changes that can help\n"
            steps += "   • Whether medication is needed\n\n"
        
        steps += "4. **Maintain healthy habits:**\n"
        steps += "   • Eat a balanced diet rich in fruits and vegetables\n"
        steps += "   • Exercise regularly (at least 30 minutes daily)\n"
        steps += "   • Get adequate sleep (7-8 hours)\n"
        steps += "   • Manage stress through relaxation techniques\n"
        steps += "   • Stay hydrated\n\n"
        
        # Follow-up
        if categorized['high'] or categorized['low']:
            steps += "5. **Plan for retesting** in 3-6 months to track your progress.\n\n"
        
        # Important note
        steps += "**Remember:** This summary is for educational purposes. "
        steps += "Your doctor will interpret these results in the context of your overall health, "
        steps += "symptoms, and medical history to provide personalized care."
        
        return steps


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    from report_parser import MedicalReportParser
    
    # Sample report text
    sample_text = """
    HbA1c - (HPLC)
    H.P.L.C 5.9 %
    
    TOTAL CHOLESTEROL 195 mg/dL
    HDL CHOLESTEROL - DIRECT 46 mg/dL
    LDL CHOLESTEROL - DIRECT 118 mg/dL
    TRIGLYCERIDES 210 mg/dL
    """
    
    # Parse the report
    parser = MedicalReportParser()
    parsed = parser.parse_report(sample_text, gender="female", age=50)
    
    # Generate summary
    summarizer = TemplateSummarizer()
    
    print("=" * 70)
    print("PROFESSIONAL SUMMARY (100% RULE-BASED - GEMINI QUALITY):")
    print("=" * 70)
    print()
    
    full_summary = summarizer.generate_summary(parsed)
    print(full_summary)