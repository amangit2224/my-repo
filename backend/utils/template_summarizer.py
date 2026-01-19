"""
Template-Based Medical Report Summarizer
Generates plain-language summaries WITHOUT AI
Pure algorithmic approach using templates
"""

import os
import sys

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
        Generate plain-language summary from parsed report
        NO AI REQUIRED - Pure template-based generation
        """
        
        summary_parts = []
        
        # Header
        summary_parts.append(self._generate_header(parsed_report))
        
        # Critical findings first (if any)
        if parsed_report['categorized']['critical']:
            summary_parts.append(self._generate_critical_section(parsed_report))
        
        # Abnormal findings
        if parsed_report['categorized']['high'] or parsed_report['categorized']['low']:
            summary_parts.append(self._generate_abnormal_section(parsed_report))
        
        # Normal findings
        if parsed_report['categorized']['normal']:
            summary_parts.append(self._generate_normal_section(parsed_report))
        
        # Recommendations
        summary_parts.append(self._generate_recommendations(parsed_report))
        
        # Footer
        summary_parts.append(self._generate_footer())
        
        return "\n\n".join(summary_parts)
    
    def _generate_header(self, parsed_report):
        """Generate opening section"""
        report_type = parsed_report['report_type']
        total_tests = parsed_report['total_tests']
        
        header = f"📋 **{report_type} Summary**\n"
        header += f"Total tests analyzed: {total_tests}\n\n"
        
        # Overall health assessment
        critical = len(parsed_report['categorized']['critical'])
        abnormal = len(parsed_report['categorized']['high']) + len(parsed_report['categorized']['low'])
        normal = len(parsed_report['categorized']['normal'])
        
        if critical > 0:
            header += "⚠️ **Immediate medical attention recommended** - Critical values detected.\n"
        elif abnormal > normal:
            header += "⚠️ **Some values need attention** - Please discuss with your doctor.\n"
        elif abnormal > 0:
            header += "✓ **Mostly good results** - A few values are outside normal range.\n"
        else:
            header += "✅ **Excellent results** - All values are within normal range!\n"
        
        return header
    
    def _generate_critical_section(self, parsed_report):
        """Generate section for critical/emergency findings"""
        section = "🚨 **CRITICAL FINDINGS - URGENT ATTENTION NEEDED:**\n\n"
        
        for result in parsed_report['categorized']['critical']:
            term = result['term']
            value = result['value']
            unit = result['unit']
            interp = result['interpretation']
            
            section += f"**{term}**: {value} {unit}\n"
            section += f"• Status: {interp['status'].upper()}\n"
            section += f"• Normal Range: {interp['normal_range']}\n"
            section += f"• **{interp.get('condition', 'Abnormal')}**\n"
            section += f"• Severity: {interp.get('severity', 'Unknown')}\n"
            section += f"• Action: **Contact your doctor immediately**\n\n"
        
        return section
    
    def _generate_abnormal_section(self, parsed_report):
        """Generate section for high/low values"""
        section = "⚠️ **VALUES OUTSIDE NORMAL RANGE:**\n\n"
        
        # High values
        for result in parsed_report['categorized']['high']:
            section += self._format_abnormal_result(result, "HIGH")
        
        # Low values
        for result in parsed_report['categorized']['low']:
            section += self._format_abnormal_result(result, "LOW")
        
        return section
    
    def _format_abnormal_result(self, result, status_label):
        """Format a single abnormal result"""
        term = result['term']
        value = result['value']
        unit = result['unit']
        interp = result['interpretation']
        
        text = f"**{term}**: {value} {unit} ({status_label})\n"
        
        # What it means
        text += f"• **What this is:** {interp['explanation']}\n"
        text += f"• **Normal Range:** {interp['normal_range']}\n"
        text += f"• **Your Status:** {interp.get('condition', 'Outside normal range')}\n"
        
        # Possible causes
        causes = interp.get('possible_causes', [])
        if causes:
            text += f"• **Common Causes:** {', '.join(causes[:3])}\n"
        
        # Symptoms to watch for
        symptoms = interp.get('symptoms', [])
        if symptoms:
            text += f"• **Watch For:** {', '.join(symptoms[:3])}\n"
        
        # Next steps
        next_steps = interp.get('next_steps', 'Consult your doctor')
        text += f"• **What to Do:** {next_steps}\n\n"
        
        return text
    
    def _generate_normal_section(self, parsed_report):
        """Generate section for normal values"""
        section = "✅ **NORMAL RESULTS:**\n\n"
        
        normal_results = parsed_report['categorized']['normal']
        
        if len(normal_results) <= 3:
            # List each individually if few
            for result in normal_results:
                term = result['term']
                value = result['value']
                unit = result['unit']
                section += f"• **{term}**: {value} {unit} ✓\n"
        else:
            # Group if many
            terms = [r['term'] for r in normal_results]
            section += f"The following {len(normal_results)} tests are within healthy range:\n"
            section += f"• {', '.join(terms)}\n"
        
        section += "\nThese results indicate good health in these areas. Keep it up!\n"
        
        return section
    
    def _generate_recommendations(self, parsed_report):
        """Generate actionable recommendations"""
        section = "💡 **RECOMMENDATIONS:**\n\n"
        
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
        
        # Generate specific recommendations
        if has_high_cholesterol or has_high_triglycerides or has_low_hdl:
            recommendations.append("**Heart Health:**")
            recommendations.append("  • Follow a heart-healthy diet (reduce saturated fats)")
            recommendations.append("  • Increase physical activity (30 min daily)")
            recommendations.append("  • Consider omega-3 rich foods (fish, nuts)")
            recommendations.append("  • Reduce alcohol consumption")
            
        if has_high_sugar:
            recommendations.append("**Blood Sugar Management:**")
            recommendations.append("  • Monitor carbohydrate intake")
            recommendations.append("  • Increase fiber-rich foods")
            recommendations.append("  • Regular exercise to improve insulin sensitivity")
            recommendations.append("  • Check blood sugar regularly")
        
        # General recommendations
        recommendations.append("**General Health:**")
        recommendations.append("  • Schedule a follow-up with your doctor to discuss these results")
        recommendations.append("  • Bring this report to your next appointment")
        
        if parsed_report['categorized']['critical']:
            recommendations.append("  • **URGENT: Contact your doctor today about critical values**")
        elif all_abnormal:
            recommendations.append("  • Ask about retesting in 3-6 months to track progress")
        
        recommendations.append("  • Maintain a healthy lifestyle (diet, exercise, sleep)")
        recommendations.append("  • Stay hydrated and manage stress")
        
        section += "\n".join(recommendations)
        
        return section
    
    def _generate_footer(self):
        """Generate disclaimer footer"""
        footer = "\n---\n\n"
        footer += "**IMPORTANT DISCLAIMER:**\n"
        footer += "This is an educational summary to help you understand your test results. "
        footer += "It is NOT a medical diagnosis or treatment recommendation. "
        footer += "Always consult your healthcare provider for medical advice and treatment. "
        footer += "Your doctor will interpret these results in the context of your overall health, "
        footer += "symptoms, medical history, and other factors.\n"
        
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
    print("FULL SUMMARY (YOUR ALGORITHM - NO AI):")
    print("=" * 70)
    full_summary = summarizer.generate_summary(parsed)
    print(full_summary)
    
    print("\n\n")
    print("=" * 70)
    print("COMPACT SUMMARY:")
    print("=" * 70)
    compact_summary = summarizer.generate_compact_summary(parsed)
    print(compact_summary)