from jinja2 import Template
import json
import weasyprint

def create_pdf_from_template(json_data, template_file, output_filename):
    # Открываем данные JSON
    data = json.loads(json_data)

    # Загружаем HTML-шаблон
    with open(template_file, 'r') as file:
        template = Template(file.read())

    # Генерируем HTML на основе шаблона и данных
    html_content = template.render(data)

    # Преобразуем HTML в PDF
    weasyprint.HTML(string=html_content).write_pdf(output_filename)

# Пример использования
json_input = '''{
    "logo_url": "https://donondo.com/img/fav.png",
    "invoice_title": "Invoice #12345",
    "company_info": "Your Company Name\\nAddress Line 1\\nAddress Line 2",
    "client_info": "Client Name\\nClient Address\\nClient City",
    "items": [
        {"description": "Product 1", "quantity": 2, "price": 15.50},
        {"description": "Product 2", "quantity": 1, "price": 42.00}
    ],
    "total": 73.00
}'''

create_pdf_from_template(json_input, 'template.html', 'invoice.pdf')
