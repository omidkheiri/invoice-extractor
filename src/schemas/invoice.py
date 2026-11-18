from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from src.validators.business_rules import validate_invoice_totals, validate_item_calculation


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class PartyInfo(BaseModel):
    name: str = Field(..., description="Name of the party.")
    address: Optional[str] = Field(default=None, description="Address of the party.")
    email: Optional[str] = Field(default=None, description="Email address of the party.")


class InvoiceItem(BaseModel):
    description: str = Field(..., description="Description of the invoice item.")
    quantity: int = Field(..., ge=1, description="Quantity of the item.")
    unit_price: Decimal = Field(..., ge=0, description="Unit price of the item.")
    total_price: Decimal = Field(..., ge=0, description="Total price for the item (quantity * unit price).")

    @model_validator(mode="after")
    def check_item_math(self) -> "InvoiceItem":
        return validate_item_calculation(self)


class Invoice(BaseModel):
    invoice_number: str = Field(..., description="Unique identifier for the invoice.")
    issue_date: date = Field(..., description="Date of the invoice in YYYY-MM-DD format.")
    due_date: Optional[date] = Field(default=None, description="Due date for payment of the invoice in YYYY-MM-DD format.")
    currency: Currency = Field(..., description="Currency in which the invoice is issued.")
    sender: PartyInfo = Field(..., description="Information about the sender of the invoice.")
    recipient: PartyInfo = Field(..., description="Information about the recipient of the invoice.")
    items: list[InvoiceItem] = Field(..., description="List of items included in the invoice.")
    total_amount: Decimal = Field(..., ge=0, description="Total amount for the invoice (sum of all item total prices).")

    @model_validator(mode="after")
    def check_invoice_math(self) -> "Invoice":
        return validate_invoice_totals(self)