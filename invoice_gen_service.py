from fastapi import FastAPI,  UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from jinja2 import Template

import weasyprint
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
TEMPLATES_DIR = "templates"
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)

class PDFData(BaseModel):
    json_data: str
    template_name: str

@app.post("/generate-pdf")
async def generate_pdf(data: PDFData):
    template_path = os.path.join(TEMPLATES_DIR, data.template_name)
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")

    json_data = json.loads(data.json_data)
    with open(template_path, 'r') as file:
        template = Template(file.read())

    html_content = template.render(json_data)
    output_filename = "output_invoice.pdf"
    weasyprint.HTML(string=html_content).write_pdf(output_filename)
    return FileResponse(output_filename, filename=output_filename)

@app.get("/templates")
async def get_templates(request: Request):
    templates = os.listdir(TEMPLATES_DIR)
    base_url = str(request.base_url)
    template_links = [{"name": template, "url": f"{base_url}templates/{template}"} for template in templates]
    return {"templates": template_links}

@app.get("/templates/{template_name}")
async def get_template(template_name: str):
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")
    with open(template_path, 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/upload-template")
async def upload_template(file: UploadFile = File(...)):
    if not file.filename.endswith(".html"):
        raise HTTPException(status_code=400, detail="Only HTML templates are supported")

    template_path = os.path.join(TEMPLATES_DIR, file.filename)
    with open(template_path, 'wb') as out_file:
        content = await file.read()
        out_file.write(content)

    return {"message": "Template uploaded successfully", "template_name": file.filename}
