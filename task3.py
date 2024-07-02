from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def create_receipt(filename, transaction_details):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Receipt Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1 * inch, height - 1 * inch, "Payment Receipt")

    # Transaction Details
    c.setFont("Helvetica", 12)
    y = height - 1.5 * inch
    for key, value in transaction_details.items():
        c.drawString(1 * inch, y, f"{key}: {value}")
        y -= 0.25 * inch

    # Footer
    c.drawString(1 * inch, y - 0.5 * inch, "Thank you for your purchase!")

    c.showPage()
    c.save()

# Sample transaction details
transaction_details = {
    "Receipt Number": "123456",
    "Date": "2024-07-02",
    "Customer Name": "John Doe",
    "Item": "Laptop",
    "Quantity": "1",
    "Price": "$1200.00",
    "Total": "$1200.00"
}

# Create the receipt
create_receipt("payment_receipt.pdf", transaction_details)
