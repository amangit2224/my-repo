import pytesseract
from PIL import Image
import os

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """
    Extract text from an image file using OCR
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        raise Exception(f"OCR Error: {str(e)}")

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF file - handles both text-based and scanned PDFs
    """
    try:
        # First, try direct text extraction
        import fitz  # PyMuPDF
        
        doc = fitz.open(pdf_path)
        text = ""
        
        for page in doc:
            text += page.get_text()
        
        doc.close()
        
        # If we got meaningful text, return it
        if len(text.strip()) > 100:
            return text.strip()
        
        # Otherwise, it's a scanned PDF - use OCR
        print("Scanned PDF detected. Using OCR...")
        return extract_text_from_scanned_pdf(pdf_path)
        
    except Exception as e:
        # If PyMuPDF fails, try OCR
        return extract_text_from_scanned_pdf(pdf_path)

def extract_text_from_scanned_pdf(pdf_path):
    """
    Extract text from scanned PDF using OCR
    """
    try:
        from pdf2image import convert_from_path
        
        # Set poppler path for Windows
        poppler_path = r'C:\poppler\poppler-25.07.0\Library\bin'
        
        # Convert PDF to images
        print("Converting PDF pages to images...")
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        
        # OCR each page
        all_text = ""
        for i, image in enumerate(images):
            print(f" Processing page {i+1}/{len(images)}...")
            page_text = pytesseract.image_to_string(image)
            all_text += f"\n--- Page {i+1} ---\n{page_text}\n"
        
        return all_text.strip()
        
    except ImportError:
        return "Error: pdf2image library not installed. Run: pip install pdf2image"
    except Exception as e:
        raise Exception(f"Scanned PDF OCR Error: {str(e)}")

def process_file(filepath):
    """
    Main function to process uploaded file and extract text
    """
    file_extension = os.path.splitext(filepath)[1].lower()
    
    if file_extension in ['.png', '.jpg', '.jpeg']:
        return extract_text_from_image(filepath)
    elif file_extension == '.pdf':
        return extract_text_from_pdf(filepath)
    else:
        raise Exception("Unsupported file format")