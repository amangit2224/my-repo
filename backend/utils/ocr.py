# backend/utils/ocr.py
"""
Defensive OCR helper.
If local OCR libs (pytesseract / Pillow / pdf2image) are not installed,
this module will still import fine and process_file() will return None.
Caller must handle None and optionally use AI fallback.
"""

import os

# Default flags / placeholders
OCR_AVAILABLE = False
pytesseract = None
Image = None
convert_from_path = None

# Try to import optional heavy OCR libs only if they exist
try:
    import pytesseract as _pytesseract
    from PIL import Image as _Image
    pytesseract = _pytesseract
    Image = _Image
    OCR_AVAILABLE = True
except Exception:
    # Local OCR not available — fine for lightweight deploy
    pytesseract = None
    Image = None
    OCR_AVAILABLE = False

# pdf2image is optional (only needed for scanned PDFs)
try:
    from pdf2image import convert_from_path as _convert_from_path
    convert_from_path = _convert_from_path
except Exception:
    convert_from_path = None


def extract_text_from_image(image_path):
    """Extract text from an image using pytesseract (if available)."""
    if not OCR_AVAILABLE or Image is None or pytesseract is None:
        return None

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip() if text else None
    except Exception:
        return None


def extract_text_from_pdf(pdf_path):
    """
    Try to extract text from PDF using PyMuPDF (if installed) first.
    If textual extraction is poor or PyMuPDF isn't available, fall back to scanned-PDF OCR (pdf2image + pytesseract).
    If local OCR tools are not available, return None.
    """
    # Try fast text extraction with PyMuPDF (fitz) if available
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        text_chunks = []
        for page in doc:
            text_chunks.append(page.get_text())
        doc.close()
        text = "\n".join(text_chunks).strip()
        # If the extracted text seems meaningful, return it
        if text and len(text) > 50:
            return text
    except Exception:
        text = ""

    # If we got little/no text, and local OCR is available, use pdf2image -> pytesseract
    if convert_from_path is None or pytesseract is None:
        # Local OCR not available
        return None

    try:
        # Convert PDF pages to images (poppler must be available on host if used locally)
        images = convert_from_path(pdf_path)
        all_text = []
        for i, page_image in enumerate(images):
            page_text = pytesseract.image_to_string(page_image)
            if page_text:
                all_text.append(f"--- Page {i+1} ---\n{page_text}")
        final = "\n".join(all_text).strip()
        return final if final else None
    except Exception:
        return None


def process_file(filepath):
    """
    Unified entrypoint. Returns extracted text (string) or None if no local extractor is available or extraction fails.
    """
    if not filepath or not os.path.exists(filepath):
        return None

    ext = os.path.splitext(filepath)[1].lower()
    if ext in (".png", ".jpg", ".jpeg"):
        return extract_text_from_image(filepath)
    if ext == ".pdf":
        return extract_text_from_pdf(filepath)

    # Unsupported file type for local OCR
    return None
