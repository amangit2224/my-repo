import PyPDF2
import os

def process_file(filepath):
    """
    Fast PDF text extraction using PyPDF2
    Works for digital PDFs (not scanned images)
    Returns extracted text or None
    """
    try:
        if filepath.lower().endswith('.pdf'):
            print(f" Extracting text from PDF: {filepath}")
            
            with open(filepath, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                extracted_text = ""
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
                
                extracted_text = extracted_text.strip()
                
                if extracted_text:
                    print(f" PyPDF2 extracted {len(extracted_text)} characters")
                    return extracted_text
                else:
                    print(" PyPDF2 extracted no text (might be scanned image)")
                    return None
        
        else:
            # For images, return None (let AI handle it)
            print(f"Not a PDF file: {filepath}")
            return None
            
    except Exception as e:
        print(f"PyPDF2 extraction failed: {e}")
        return None