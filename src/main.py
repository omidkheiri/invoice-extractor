import json
from pathlib import Path
from pydantic import ValidationError
from src.config import settings
from src.extractors.invoice_extractor import extract_invoice_from_document
from src.parsers.docuent_loader import load_document

def process_single_invoice(file_path:Path)->None:
    print(f"در حال پردازش فایل: {file_path.name} ...")
    try:
        loaded_document = load_document(file_path)
        print(f"نوع محتوا: {loaded_document.content_type}")
        invoice = extract_invoice_from_document(loaded_document)
        print(f"فاکتور استخراج شد: {invoice}")
        settings.processed_data_dir.mkdir(parents=True, exist_ok=True)
        output_file_path = settings.processed_data_dir / f"{file_path.stem}_invoice.json"
        json_output=invoice.model_dump_json(indent=4, ensure_ascii=False)
        output_file_path.write_text(json_output, encoding="utf-8")
        print(f"در حال ذخیره فاکتور استخراج شده در: {output_file_path} ...")

    except FileNotFoundError as e:
        print(f"خطا: {e}")
    except ValidationError as e:
        print(f"خطا در اعتبارسنجی داده‌های استخراج شده: {e}")    

def main()-> None:
    sample_invoice_path = settings.raw_data_dir / "sample_invoice.pdf"
    process_single_invoice(sample_invoice_path)

if __name__ == "__main__":
    main()