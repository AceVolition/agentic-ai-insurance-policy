from __future__ import annotations

from io import BytesIO

import pdfplumber
import pytesseract
from PIL import Image
from pytesseract import TesseractError, TesseractNotFoundError


def extract_text_from_pdf(content: bytes) -> str:
    text_parts: list[str] = []
    with pdfplumber.open(BytesIO(content)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            if extracted.strip():
                text_parts.append(extracted)
                continue

            try:
                image = page.to_image(resolution=200).original
            except Exception:
                image = None
            if isinstance(image, Image.Image):
                try:
                    ocr_text = pytesseract.image_to_string(image)
                except (TesseractNotFoundError, TesseractError):
                    ocr_text = ""
                if ocr_text.strip():
                    text_parts.append(ocr_text)

    return "\n\n".join(part.strip() for part in text_parts if part.strip())
