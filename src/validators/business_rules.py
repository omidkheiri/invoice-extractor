from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.schemas.invoice import Invoice, InvoiceItem

TOLERANCE = Decimal("0.05")


def validate_item_calculation(item: "InvoiceItem") -> "InvoiceItem":
    """Validates that quantity * unit_price equals total_price for each item."""
    expected_total = item.quantity * item.unit_price
    if abs(expected_total - item.total_price) > TOLERANCE:
        raise ValueError(
            f"Calculation error in item '{item.description}': "
            f"{item.quantity} * {item.unit_price} = {expected_total}, "
            f"but extracted total_price is {item.total_price}."
        )
    return item


def validate_invoice_totals(invoice: "Invoice") -> "Invoice":
    """Validates date logic and that the sum of item prices matches total_amount."""
    if invoice.due_date and invoice.due_date < invoice.issue_date:
        raise ValueError(
            f"Invoice due date ({invoice.due_date}) cannot be earlier than issue date ({invoice.issue_date})."
        )

    calculated_total = sum((item.total_price for item in invoice.items), Decimal("0"))
    if abs(calculated_total - invoice.total_amount) > TOLERANCE:
        raise ValueError(
            f"Invoice total amount ({invoice.total_amount}) does not match "
            f"the sum of item total prices ({calculated_total})."
        )

    return invoice