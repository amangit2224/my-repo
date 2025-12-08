# backend/utils/ocr.py
import os
import io
import requests

def _try_pymupdf_text(pdf_path):
    try:
        import fitz  # PyMuPDF
    except Exception:
        return None

    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        if text and len(text.strip()) > 50:
            return text.strip()
        return None
    except Exception:
        return None


def _ocr_space_api_file(filepath, api_key=None):
    """
    Use OCR.space API fallback. api_key can be 'helloworld' for demo (low rate limit).
    """
    if api_key is None:
        api_key = os.getenv("OCR_SPACE_API_KEY", "helloworld")

    url = "https://api.ocr.space/parse/image"
    with open(filepath, "rb") as f:
        files = {"file": (os.path.basename(filepath), f)}
        data = {
            "apikey": api_key,
            "language": "eng",
            "isOverlayRequired": False,
            "OCREngine": 2
        }
        try:
            r = requests.post(url, data=data, files=files, timeout=60)
            r.raise_for_status()
            result = r.json()
            if result.get("IsErroredOnProcessing"):
                return None
            parsed = []
            for parsed_result in result.get("ParsedResults") or []:
                parsed.append(parsed_result.get("ParsedText", ""))
            text = "\n".join(parsed).strip()
            return text if text else None
        except Exception:
            return None


def extract_text_from_image(image_path):
    # try local pytesseract if available
    try:
        from PIL import Image
        import pytesseract
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        if text and len(text.strip()) > 0:
            return text.strip()
    except Exception:
        pass

    # fallback to OCR.space
    text = _ocr_space_api_file(image_path)
    if text:
        return text
    raise Exception("Unable to extract text from image (no local OCR and OCR API failed).")


def extract_text_from_pdf(pdf_path):
    # 1) try fast text extraction via PyMuPDF
    text = _try_pymupdf_text(pdf_path)
    if text:
        return text

    # 2) try local OCR for scanned pages (pytesseract+pdf2image) if available
    try:
        from pdf2image import convert_from_path
        from PIL import Image
        import pytesseract

        poppler_path = os.getenv("POPPLER_PATH")  # optional env pointing to poppler bin
        images = convert_from_path(pdf_path, poppler_path=poppler_path) if poppler_path else convert_from_path(pdf_path)
        out = []
        for img in images:
            t = pytesseract.image_to_string(img)
            if t:
                out.append(t)
        if out:
            return "\n\n".join(out).strip()
    except Exception:
        pass

    # 3) fallback to OCR.space (upload PDF file directly)
    text = _ocr_space_api_file(pdf_path)
    if text:
        return text

    raise Exception("Unable to extract text from PDF with local OCR. AI fallback not available.")


def process_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(filepath)
    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    raise Exception("Unsupported file format")
