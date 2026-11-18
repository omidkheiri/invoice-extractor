from src.config import settings
from src.extractors.llm_client import get_instructor_client
from src.parsers.docuent_loader import LoadedDocument
from src.schemas.invoice import Invoice

SYSTEM_PROMPT = """ تو یک حسابدار ارشد و متخصص استخراج دقیق داده‌های مالی از فاکتورها هستی.
وظیفه تو استخراج تمام اطلاعات فاکتور با بالاترین دقت و بدون هیچ‌گونه حدس یا توهم‌زایی (Hallucination) است.
- اگر فیلدی در فاکتور وجود ندارد، مقدار آن را null قرار بده.
- به دقت ریاضی ردیف‌ها، تخفیف‌ها، مالیات و جمع کل توجه کن.
- تاریخ‌ها را به فرمت استاندارد میلادی YYYY-MM-DD تبدیل کن. """

def _build_user_message(document: LoadedDocument) -> dict:
   if document.content_type == "txt":
       return {"role": "user", "content": f"لطفاً تمام اطلاعات فاکتور را از متن زیر استخراج کن:\n\n{document.text_content}"}
   content_blocks: list[dict] = [
        {"type": "text", "text": "لطفاً اطلاعات این فاکتور تصویری را با دقت استخراج کن:"}
    ]
   
   for base64_image in document.base64_content or []:
        content_blocks.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
   return {"role": "user", "content": content_blocks}

def extract_invoice_from_document(document: LoadedDocument) -> Invoice:
    """
    Extracts invoice data from a given document using an LLM client.

    Args:
        document (LoadedDocument): The document from which to extract invoice data.

    Returns:
        Invoice: The extracted invoice data.
    """
    llm_client = get_instructor_client()
    user_message = _build_user_message(document)
    
    invoice = llm_client.chat.completions.create(
    model=settings.llm_model,
    temperature=settings.temperature,
    max_retries=settings.max_retries,
    response_model=Invoice,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        user_message,
    ],
    )
    
    return invoice
