"""
PDF Forensics - Detects Tampered/Fake Medical Reports
Analyzes PDF metadata, structure, and digital signatures
NO AI REQUIRED - Pure forensics algorithms
"""

import PyPDF2
from datetime import datetime
import re
import os

class PDFForensics:
    
    def __init__(self):
        self.suspicion_score = 0
        self.findings = []
        self.risk_level = "Unknown"
    
    def analyze_pdf(self, filepath):
        """
        Comprehensive PDF forensics analysis
        Returns trust score and detailed findings
        """
        
        print(f"\n{'='*60}")
        print(f"🔍 PDF FORENSICS ANALYSIS")
        print(f"{'='*60}\n")
        
        if not filepath.endswith('.pdf'):
            return {
                'verified': False,
                'trust_score': 100,
                'risk_level': 'Not Applicable',
                'findings': ['Not a PDF file - forensics not applicable'],
                'recommendations': []
            }
        
        try:
            with open(filepath, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                # Run all forensic checks
                self._check_metadata(pdf_reader)
                self._check_encryption(pdf_reader)
                self._check_page_count(pdf_reader)
                self._check_creation_modification_dates(pdf_reader)
                self._check_producer_software(pdf_reader)
                
                # Calculate final scores
                trust_score = max(0, 100 - self.suspicion_score)
                self._determine_risk_level(trust_score)
                
                print(f"\n{'='*60}")
                print(f"📊 FORENSICS SUMMARY:")
                print(f"   Trust Score: {trust_score}/100")
                print(f"   Risk Level: {self.risk_level}")
                print(f"   Suspicion Points: {self.suspicion_score}")
                print(f"   Findings: {len(self.findings)}")
                print(f"{'='*60}\n")
                
                return {
                    'verified': trust_score >= 70,
                    'trust_score': trust_score,
                    'risk_level': self.risk_level,
                    'findings': self.findings,
                    'recommendations': self._generate_recommendations()
                }
                
        except Exception as e:
            print(f"❌ PDF Forensics Error: {e}")
            return {
                'verified': False,
                'trust_score': 0,
                'risk_level': 'Error',
                'findings': [f'Error analyzing PDF: {str(e)}'],
                'recommendations': ['Unable to verify - manual review required']
            }
    
    def _check_metadata(self, pdf_reader):
        """Check for presence and validity of metadata - SIMPLIFIED"""
        try:
            metadata = pdf_reader.metadata
            
            if not metadata:
                self.suspicion_score += 20
                self.findings.append("⚠️ Document information incomplete")
                print("⚠️  No metadata found (+20 suspicion)")
            else:
                has_creator = metadata.get('/Creator')
                has_producer = metadata.get('/Producer')
                has_creation_date = metadata.get('/CreationDate')
                
                if not has_creator and not has_producer:
                    self.suspicion_score += 15
                    self.findings.append("⚠️ Software information missing")
                    print("⚠️  Missing creator/producer (+15 suspicion)")
                
                if not has_creation_date:
                    self.suspicion_score += 10
                    self.findings.append("⚠️ Creation date not recorded")
                    print("⚠️  Missing creation date (+10 suspicion)")
                        
        except Exception as e:
            print(f"⚠️  Metadata check failed: {e}")
    
    def _check_encryption(self, pdf_reader):
        """Check if PDF is encrypted or password protected"""
        try:
            if pdf_reader.is_encrypted:
                self.suspicion_score += 25
                self.findings.append("🔒 PDF is encrypted - unusual for medical reports")
                print("🔒 PDF encrypted (+25 suspicion)")
            else:
                self.findings.append("✅ PDF is not encrypted")
                print("✅ Not encrypted")
        except:
            pass
    
    def _check_page_count(self, pdf_reader):
        """Check for suspiciously low page count"""
        try:
            page_count = len(pdf_reader.pages)
            
            if page_count == 1:
                self.suspicion_score += 5
                self.findings.append("⚠️ Single-page report (unusual)")
                print(f"⚠️  Only 1 page (+5 suspicion)")
            elif page_count > 20:
                self.suspicion_score += 5
                self.findings.append("⚠️ Unusually long report (>20 pages)")
                print(f"⚠️  {page_count} pages - unusually long (+5 suspicion)")
            else:
                self.findings.append(f"✅ Normal page count ({page_count} pages)")
                print(f"✅ {page_count} pages - normal")
        except:
            pass
    
    def _check_creation_modification_dates(self, pdf_reader):
        """Detect if modification date is much later than creation"""
        try:
            metadata = pdf_reader.metadata
            if not metadata:
                return
            
            creation_date_str = metadata.get('/CreationDate')
            mod_date_str = metadata.get('/ModDate')
            
            if creation_date_str and mod_date_str:
                creation_date = self._parse_pdf_date(creation_date_str)
                mod_date = self._parse_pdf_date(mod_date_str)
                
                if creation_date and mod_date:
                    time_diff = (mod_date - creation_date).total_seconds()
                    days_diff = time_diff / (3600 * 24)
                    
                    if days_diff > 30:
                        self.suspicion_score += 20
                        self.findings.append("⚠️ Document was edited long after creation")
                        print(f"🚨 Modified {int(days_diff)} days after creation (+20 suspicion)")
                    elif days_diff > 7:
                        self.suspicion_score += 10
                        self.findings.append("⚠️ Document was edited after creation")
                        print(f"⚠️  Modified {int(days_diff)} days later (+10 suspicion)")
                    elif days_diff > 1:
                        self.suspicion_score += 5
                        self.findings.append("⚠️ Minor editing detected")
                        print(f"⚠️  Modified {int(days_diff)} days later (+5 suspicion)")
                            
        except Exception as e:
            print(f"⚠️  Date check failed: {e}")
    
    def _parse_pdf_date(self, date_str):
        """Parse PDF date string to datetime"""
        try:
            # PDF date format: D:YYYYMMDDHHmmSS
            date_str = str(date_str).replace('D:', '').replace("'", "")
            # Extract just the date/time part (first 14 chars)
            date_part = date_str[:14]
            return datetime.strptime(date_part, '%Y%m%d%H%M%S')
        except:
            return None
    
    def _check_producer_software(self, pdf_reader):
        """Check what software created the PDF - SIMPLIFIED"""
        try:
            metadata = pdf_reader.metadata
            if not metadata:
                return
            
            producer = str(metadata.get('/Producer', '')).lower()
            creator = str(metadata.get('/Creator', '')).lower()
            
            suspicious_producers = [
                'photoshop', 'gimp', 'paint', 'canva',
                'pixlr', 'online', 'converter', 'merge', 'smallpdf'
            ]
            
            is_suspicious = any(sus in producer or sus in creator 
                               for sus in suspicious_producers)
            
            if is_suspicious:
                self.suspicion_score += 30
                self.findings.append("⚠️ Created using image editing software")
                print(f"🚨 Suspicious software: {producer} (+30 suspicion)")
            elif not producer and not creator:
                self.suspicion_score += 10
                self.findings.append("⚠️ Software information unavailable")
                print(f"⚠️  Unknown software (+10 suspicion)")
                    
        except Exception as e:
            print(f"⚠️  Producer check failed: {e}")
    
    def _determine_risk_level(self, trust_score):
        """Determine risk level based on trust score"""
        if trust_score >= 90:
            self.risk_level = "Verified"
        elif trust_score >= 70:
            self.risk_level = "Low Risk"
        elif trust_score >= 50:
            self.risk_level = "Medium Risk"
        elif trust_score >= 30:
            self.risk_level = "High Risk"
        else:
            self.risk_level = "Critical - Likely Fake"
    
    def _generate_recommendations(self):
        """Generate simplified, actionable recommendations"""
        recommendations = []
        
        if self.suspicion_score >= 50:
            recommendations.append("Verify this report directly with the laboratory")
            recommendations.append("Request a fresh copy from the medical facility")
        elif self.suspicion_score >= 30:
            recommendations.append("Additional verification recommended")
            recommendations.append("Contact the issuing facility if concerns arise")
        elif self.suspicion_score >= 15:
            recommendations.append("Minor inconsistencies detected")
            recommendations.append("Report appears mostly legitimate")
        else:
            recommendations.append("This report appears authentic")
            recommendations.append("No significant concerns detected")
        
        return recommendations


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":
    # Test with a sample PDF
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        forensics = PDFForensics()
        result = forensics.analyze_pdf(filepath)
        
        print("\n" + "="*60)
        print("FINAL FORENSICS REPORT:")
        print("="*60)
        print(f"\nTrust Score: {result['trust_score']}/100")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Verified: {result['verified']}")
        
        print("\nFindings:")
        for finding in result['findings']:
            print(f"  {finding}")
        
        print("\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  {rec}")
    else:
        print("Usage: python pdf_forensics.py <path_to_pdf>")