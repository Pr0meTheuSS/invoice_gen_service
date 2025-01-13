from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import json
import requests
from io import BytesIO

def create_pdf_invoice(json_data, output_filename):
    # Открываем JSON данные
    data = json.loads(json_data)
    
    c = canvas.Canvas(output_filename, pagesize=A4)
    width, height = A4

    # Добавление логотипа
    if 'logo_url' in data:
        response = requests.get(data['logo_url'])
        if response.status_code == 200:
            logo_img = BytesIO(response.content)
            logo_reader = ImageReader(logo_img)
            logo_width, logo_height = 1*inch, 0.5*inch  # Размер логотипа
            c.drawImage(logo_reader, 50, height - 100, logo_width, logo_height)

    # Заголовок
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 150, data.get('invoice_title', 'Invoice'))

    # Информация о компании
    c.setFont("Helvetica", 12)
    company_info = data.get('company_info', 'Company Information')
    for i, line in enumerate(company_info.split('\\n')):
        c.drawString(50, height - 180 - i * 15, line)

    # Информация о клиенте
    client_info = data.get('client_info', 'Client Information')
    for i, line in enumerate(client_info.split('\\n')):
        c.drawString(50, height - 210 - i * 15, line)

    # Дата счета и срок оплаты
    c.drawString(50, height - 250, f"Invoice Date: {data.get('invoice_date', 'N/A')}")
    c.drawString(50, height - 270, f"Due Date: {data.get('due_date', 'N/A')}")

    # Таблица с элементами счета
    c.drawString(50, height - 300, "Itemized Details:")
    items = data.get('items', [])

    y_position = height - 320
    for item in items:
        item_description = item.get('description', 'No description')
        item_quantity = item.get('quantity', 1)
        item_price = item.get('price', 0.0)
        line_text = f"{item_description}: {item_quantity} x ${item_price:.2f}"
        c.drawString(60, y_position, line_text)
        y_position -= 20

    # Итоговая сумма
    total = data.get('total', '0.0')
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position - 20, f"Total: ${total:.2f}")

    # Закрытие PDF файла
    c.save()

# Пример использования с дополнительными полями
json_input = '''{
    "logo_url": "https://donondo.com/img/fav.png",
    "invoice_title": "Invoice #12345",
    "invoice_date": "2025-01-12",
    "due_date": "2025-02-12",
    "company_info": "Your Company Name\\nAddress Line 1\\nAddress Line 2",
    "client_info": "Client Name\\nClient Address\\nClient City",
    "items": [
        {"description": "Product 1", "quantity": 2, "price": 15.50},
        {"description": "Product 2", "quantity": 1, "price": 42.00}
    ],
    "total": 73.00
}'''

create_pdf_invoice(json_input, "invoice_with_dates.pdf")
