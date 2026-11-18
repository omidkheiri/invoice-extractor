import base64
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Literal
import fitz  # PyMuPDF
from PIL import Image

@dataclass
class LoadedDocument:
    source_path: Path
    content_type: Literal["pdf", "image"]
    text_content: str |None=None
    base64_content: list[str] |None=None 

def _encode_pil_image_to_base64(image: Image.Image, format: str = "jpg") -> str:
    """
    Encodes a PIL Image to a base64 string.
    
    Args:
        image (Image.Image): The PIL Image to encode.
        
    Returns:
        str: The base64 encoded string of the image.
    """
    buffered = BytesIO()
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(buffered, format="PNG",quality=85)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def _load_pdf(source_path: Path, min_text_length: int=50) -> LoadedDocument:
    doc=fitz.open(source_path)
    extracted_pages_text=[]
    for page in doc:
        extracted_pages_text.append(page.get_text("text").strip())
    full_text="\n\n--- Page Break ---\n\n".join(extracted_pages_text).strip()

    if len(full_text) >= min_text_length:
        doc.close()
        return LoadedDocument(
            source_path=source_path,
            content_type="txt",
            text_content=full_text)
    base64_pages=[]
    for page in doc:
        pix=page.get_pixmap()
        img=Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        base64_pages.append(_encode_pil_image_to_base64(img))
    doc.close()
    return LoadedDocument(
        source_path=source_path,
        content_type="image",
        base64_content=base64_pages)

def _load_image(source_path: Path) -> LoadedDocument:
    with Image.open(source_path) as img:
        base64_content=[_encode_pil_image_to_base64(img)]
    return LoadedDocument(
        source_path=source_path,
        content_type="image",
        base64_content=base64_content)
def load_document(source_path: str|Path) -> LoadedDocument:
    path=Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"The specified file does not exist: {source_path}")
    suffix=path.suffix.lower()
    if suffix==".pdf":
        return _load_pdf(path)
    elif suffix in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
        return _load_image(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Supported types are PDF and common image formats (jpg, jpeg, png, bmp, gif).")
    