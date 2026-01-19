"""
Template-Based Medical Report Summarizer - ENHANCED VERSION
Generates DETAILED plain-language summaries WITHOUT AI
Pure algorithmic approach using templates
"""

import sys
import os

# Try different import paths for flexibility
try:
    from utils.medical_knowledge import MedicalKnowledgeBase
    print("✅ MedicalKnowledgeBase imported from utils.medical_knowledge (template)")
except ImportError:
    try:
        from medical_knowledge import MedicalKnowledgeBase
        print("✅ MedicalKnowledgeBase imported from medical_knowledge (template)")
    except ImportError:
        try:
            # Add current directory to Python path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            sys.path.append(current_dir)
            sys.path.append(parent_dir)
            from medical_knowledge import MedicalKnowledgeBase
            print("✅ MedicalKnowledgeBase imported with sys.path adjustment (template)")
        except ImportError as e:
            print(f"❌ Failed to import MedicalKnowledgeBase in template_summarizer: {e}")
            # Create a dummy class to prevent crashes
            class MedicalKnowledgeBase:
                @staticmethod
                def get_term_info(term):
                    return None
            print("⚠️ Using dummy MedicalKnowledgeBase in template_summarizer")

class TemplateSummarizer:
    
    def __init__(self):
        self.kb = MedicalKnowledgeBase()
    
    def generate_summary(self, parsed_report):
        """
        Generate DETAILED plain-language summary from parsed report
        NO AI REQUIRED - Pure template-based generation
        """
        
        summary_parts = []
        
        # Header with patient-friendly greeting
        summary_parts.append(self._generate_detailed_header(parsed_report))
        
        # Critical findings first (if any)
        if parsed_report['categorized']['critical']:
            summary_parts.append(self._generate_critical_section(parsed_report))
        
        # Detailed explanation of each abnormal value
        if parsed_report['categorized']['high'] or parsed_report['categorized']['low']:
            summary_parts.append(self._generate_detailed_abnormal_section(parsed_report))
        
        # Normal findings with encouragement
        if parsed_report['categorized']['normal']:
            summary_parts.append(self._generate_detailed_normal_section(parsed_report))
        
        # Comprehensive recommendations
        summary_parts.append(self._generate_detailed_recommendations(parsed_report))
        
        # What to discuss with doctor
        summary_parts.append(self._generate_doctor_discussion_points(parsed_report))
        
        # Footer
        summary_parts.append(self._generate_footer())
        
        return "\n\n".join(summary_parts)
    
    def _generate_detailed_header(self, parsed_report):
        """Generate friendly, detailed opening"""
        report_type = parsed_report['report_type']
        total_tests = parsed_report['total_tests']
        
        header = f"# 📋 Your {report_type} Results Explained\n\n"
        header += f"Hello! Let's go through your test results together. I'll explain what each number means in plain language.\n\n"
        header += f"**Tests Analyzed:** {total_tests}\n\n"
        
        # Overall health assessment
        critical = len(parsed_report['categorized']['critical'])
        abnormal = len(parsed_report['categorized']['high']) + len(parsed_report['categorized']['low'])
        normal = len(parsed_report['categorized']['normal'])
        
        if critical > 0:
            header += "## ⚠️ Immediate Attention Needed\n\n"
            header += "Some of your results require urgent medical attention. Please contact your doctor today.\n"
        elif abnormal > normal:
            header += "## 📊 Results Need Discussion\n\n"
            header += "Several values are outside the normal range. Don't worry - we'll explain what this means and what you can do about it.\n"
        elif abnormal > 0:
            header += "## ✓ Mostly Good News!\n\n"
            header += "Most of your results look good! A few values need attention, but nothing alarming.\n"
        else:
            header += "## ✅ Excellent Results!\n\n"
            header += "Great news! All your values are within healthy ranges. Keep up the good work!\n"
        
        return header
    
    def _generate_critical_section(self, parsed_report):
        """Generate detailed critical findings section"""
        section = "## 🚨 URGENT: Critical Values Detected\n\n"
        
        for result in parsed_report['categorized']['critical']:
            term = result['term']
            value = result['value']
            unit = result['unit']
            interp = result['interpretation']
            
            section += f"### ❗ {term}\n\n"
            section += f"**Your Value:** {value} {unit}\n\n"
            section += f"**Normal Range:** {interp['normal_range']}\n\n"
            section += f"**What This Means:**\n{interp['explanation']}\n\n"
            section += f"**Why This is Critical:**\n{interp.get('condition', 'This value is significantly outside normal range')}\n\n"
            section += f"**What You Should Do:**\n"
            section += f"🚨 **Contact your doctor TODAY** - This requires immediate medical evaluation.\n\n"
            section += "---\n\n"
        
        return section
    
    def _generate_detailed_abnormal_section(self, parsed_report):
        """Generate detailed section for abnormal values"""
        section = "## 📊 Values That Need Attention\n\n"
        section += "Let me explain each value that's outside the normal range:\n\n"
        
        # High values
        for result in parsed_report['categorized']['high']:
            section += self._format_detailed_abnormal_result(result, "Higher Than Normal")
        
        # Low values
        for result in parsed_report['categorized']['low']:
            section += self._format_detailed_abnormal_result(result, "Lower Than Normal")
        
        return section
    
    def _format_detailed_abnormal_result(self, result, status_label):
        """Format a single abnormal result with FULL explanation"""
        term = result['term']
        value = result['value']
        unit = result['unit']
        interp = result['interpretation']
        
        text = f"### 📍 {term} - {status_label}\n\n"
        
        # The result
        text += f"**Your Result:** {value} {unit}\n\n"
        text += f"**Normal Range:** {interp['normal_range']}\n\n"
        
        # What it is (detailed explanation)
        text += f"**What is {term}?**\n\n"
        text += f"{interp['explanation']}\n\n"
        
        # What your result means
        text += f"**What Your Result Means:**\n\n"
        text += f"Your {term} level is {status_label.lower()}. "
        text += f"This condition is called **{interp.get('condition', 'abnormal ' + term)}**.\n\n"
        
        # Why this might happen
        causes = interp.get('possible_causes', [])
        if causes:
            text += f"**Common Reasons for {status_label}:**\n\n"
            for i, cause in enumerate(causes, 1):
                text += f"{i}. {cause}\n"
            text += "\n"
        
        # Symptoms to watch for
        symptoms = interp.get('symptoms', [])
        if symptoms:
            text += f"**Symptoms You Might Notice:**\n\n"
            for i, symptom in enumerate(symptoms, 1):
                text += f"• {symptom}\n"
            text += "\n"
        
        # What to do about it
        text += f"**What You Can Do:**\n\n"
        next_steps = interp.get('next_steps', 'Discuss with your doctor')
        text += f"{next_steps}\n\n"
        
        text += "---\n\n"
        
        return text
    
    def _generate_detailed_normal_section(self, parsed_report):
        """Generate encouraging section for normal values"""
        section = "## ✅ Great News: Normal Results\n\n"
        
        normal_results = parsed_report['categorized']['normal']
        
        section += "These values are all within healthy range - excellent work!\n\n"
        
        for result in normal_results:
            term = result['term']
            value = result['value']
            unit = result['unit']
            interp = result['interpretation']
            
            section += f"### ✓ {term}\n\n"
            section += f"**Your Result:** {value} {unit} (Normal ✓)\n\n"
            section += f"**Normal Range:** {interp['normal_range']}\n\n"
            section += f"**What This Means:**\n{interp['explanation']}\n\n"
            section += f"Your {term} level is healthy! This is great for your overall health.\n\n"
        
        section += "**Keep It Up!** These normal results show you're taking good care of your health in these areas.\n\n"
        
        return section
    
    def _generate_detailed_recommendations(self, parsed_report):
        """Generate comprehensive, actionable recommendations"""
        section = "## 💡 Personalized Recommendations\n\n"
        section += "Based on your results, here's what you can do:\n\n"
        
        recommendations = []
        
        # Analyze abnormal results for specific recommendations
        all_abnormal = (parsed_report['categorized']['high'] + 
                       parsed_report['categorized']['low'] +
                       parsed_report['categorized']['critical'])
        
        # Check for specific conditions
        has_high_cholesterol = any(r['term'] in ['Total Cholesterol', 'LDL'] and r['interpretation']['status'] == 'high' 
                                   for r in all_abnormal)
        has_high_triglycerides = any(r['term'] == 'Triglycerides' and r['interpretation']['status'] == 'high' 
                                      for r in all_abnormal)
        has_low_hdl = any(r['term'] == 'HDL' and r['interpretation']['status'] == 'low' 
                         for r in all_abnormal)
        has_high_sugar = any(r['term'] in ['Glucose', 'HbA1c'] and r['interpretation']['status'] == 'high' 
                            for r in all_abnormal)
        
        # Heart Health Recommendations
        if has_high_cholesterol or has_high_triglycerides or has_low_hdl:
            recommendations.append({
                "category": "❤️ Heart Health",
                "tips": [
                    "**Diet Changes:**\n  - Reduce saturated fats (fried foods, red meat, full-fat dairy)\n  - Increase foods with omega-3 (salmon, walnuts, flaxseed)\n  - Eat more fiber (oats, beans, vegetables, fruits)\n  - Choose olive oil over butter",
                    "**Physical Activity:**\n  - Aim for 150 minutes of moderate exercise per week\n  - Walking, swimming, or cycling are excellent choices\n  - Even 10-minute walks after meals help!",
                    "**Lifestyle:**\n  - Limit alcohol to 1 drink per day (if any)\n  - If you smoke, consider a quit plan (talk to your doctor)\n  - Manage stress through meditation, yoga, or hobbies"
                ]
            })
        
        # Blood Sugar Recommendations
        if has_high_sugar:
            recommendations.append({
                "category": "🍎 Blood Sugar Management",
                "tips": [
                    "**Food Choices:**\n  - Choose whole grains over white bread/rice\n  - Include protein with each meal (eggs, fish, beans)\n  - Eat vegetables first at meals to slow sugar absorption\n  - Limit sugary drinks and desserts",
                    "**Meal Timing:**\n  - Don't skip meals (causes blood sugar spikes)\n  - Eat smaller portions more frequently\n  - Avoid eating late at night",
                    "**Activity:**\n  - Walk for 10-15 minutes after meals\n  - Regular exercise improves insulin sensitivity\n  - Aim for 30 minutes daily"
                ]
            })
        
        # General Health Recommendations
        recommendations.append({
            "category": "🏃 General Health",
            "tips": [
                "**Doctor Follow-Up:**\n  - Schedule an appointment to discuss these results\n  - Bring this summary with you\n  - Ask about retesting in 3-6 months to track progress",
                "**Healthy Habits:**\n  - Drink 8 glasses of water daily\n  - Get 7-8 hours of quality sleep\n  - Manage stress (it affects all health markers!)\n  - Consider keeping a food and activity journal",
                "**Medications:**\n  - If your doctor prescribes medication, take it as directed\n  - Don't stop medication without consulting your doctor\n  - Report any side effects promptly"
            ]
        })
        
        # Format all recommendations
        for rec in recommendations:
            section += f"### {rec['category']}\n\n"
            for tip in rec['tips']:
                section += f"{tip}\n\n"
        
        return section
    
    def _generate_doctor_discussion_points(self, parsed_report):
        """Generate specific questions to ask doctor"""
        section = "## 🗨️ Questions to Ask Your Doctor\n\n"
        section += "Bring these questions to your next appointment:\n\n"
        
        all_abnormal = (parsed_report['categorized']['high'] + 
                       parsed_report['categorized']['low'] +
                       parsed_report['categorized']['critical'])
        
        if all_abnormal:
            section += "**About Your Results:**\n\n"
            for result in all_abnormal[:3]:  # Top 3 abnormal
                term = result['term']
                section += f"1. \"My {term} is {result['interpretation']['status']}. What could be causing this?\"\n"
                section += f"2. \"What steps should I take to bring my {term} to a healthy range?\"\n"
                section += f"3. \"How soon should I retest my {term}?\"\n\n"
        
        section += "**General Questions:**\n\n"
        section += "1. \"Do I need any additional tests based on these results?\"\n"
        section += "2. \"Are there any medications or supplements I should consider?\"\n"
        section += "3. \"What lifestyle changes would help me the most?\"\n"
        section += "4. \"When should I schedule my next checkup?\"\n\n"
        
        return section
    
    def _generate_footer(self):
        """Generate comprehensive disclaimer"""
        footer = "\n---\n\n"
        footer += "## ⚖️ Important Medical Disclaimer\n\n"
        footer += "**Please Read Carefully:**\n\n"
        footer += "This summary is an **educational tool** designed to help you understand your test results in simple language. "
        footer += "It is **NOT**:\n\n"
        footer += "❌ A medical diagnosis\n\n"
        footer += "❌ A treatment plan\n\n"
        footer += "❌ A substitute for professional medical advice\n\n"
        footer += "✅ **Always consult your healthcare provider** for:\n\n"
        footer += "• Medical interpretation of your results\n\n"
        footer += "• Personalized treatment recommendations\n\n"
        footer += "• Questions about your health\n\n"
        footer += "• Before making any changes to medications or treatment\n\n"
        footer += "Your doctor will consider these results alongside your symptoms, medical history, medications, and overall health to provide proper care.\n\n"
        footer += "**In case of emergency:** If you experience severe symptoms, call emergency services immediately.\n"
        
        return footer
    
    def generate_compact_summary(self, parsed_report):
        """
        Generate a shorter, more compact summary
        Good for quick overview
        """
        
        critical = len(parsed_report['categorized']['critical'])
        abnormal = len(parsed_report['categorized']['high']) + len(parsed_report['categorized']['low'])
        normal = len(parsed_report['categorized']['normal'])
        
        summary = f"**{parsed_report['report_type']}**\n\n"
        
        if critical > 0:
            summary += f"🚨 {critical} critical value(s) - **Seek immediate medical attention**\n\n"
        
        if abnormal > 0:
            summary += f"⚠️ {abnormal} value(s) outside normal range:\n"
            for r in (parsed_report['categorized']['high'] + parsed_report['categorized']['low']):
                summary += f"  • {r['term']}: {r['value']} {r['unit']} ({r['interpretation']['status']})\n"
            summary += "\n"
        
        if normal > 0:
            summary += f"✅ {normal} value(s) normal\n\n"
        
        summary += "Consult your doctor to discuss these results."
        
        return summary


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    try:
        from report_parser import MedicalReportParser
        print("✅ ReportParser imported for testing")
    except ImportError:
        print("❌ Could not import ReportParser for testing")
        exit(1)
    
    # Sample report text (from your actual report)
    sample_text = """
    HbA1c - (HPLC)
    H.P.L.C 5.9 %
    
    TOTAL CHOLESTEROL 195 mg/dL
    HDL CHOLESTEROL - DIRECT 46 mg/dL
    LDL CHOLESTEROL - DIRECT 118 mg/dL
    TRIGLYCERIDES 210 mg/dL
    
    TROPONIN I HEART ATTACK RISK 1.4 pg/mL
    """
    
    # Parse the report
    parser = MedicalReportParser()
    parsed = parser.parse_report(sample_text, gender="female", age=50)
    
    # Generate summary
    summarizer = TemplateSummarizer()
    
    print("=" * 70)
    print("DETAILED SUMMARY (YOUR ALGORITHM - NO AI):")
    print("=" * 70)
    full_summary = summarizer.generate_summary(parsed)
    print(full_summary)
    
    print("\n\n")
    print("=" * 70)
    print("COMPACT SUMMARY:")
    print("=" * 70)
    compact_summary = summarizer.generate_compact_summary(parsed)
    print(compact_summary)