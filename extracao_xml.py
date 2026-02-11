import pyodbc
import os
from pathlib import Path
from fpdf import FPDF  # biblioteca para gerar PDFs
import xml.etree.ElementTree as ET

# Configuração da conexão
conn_str = (
    "DRIVER={seu_driver};"
    "SERVER={seu_ser};"
    "DATABASE={Seu_banco};"
    "Trusted_Connection=yes;"
)

# Pastas de saída
xml_dir = f"{Path.cwd()}\\xml"
pdf_dir = os.path.join(xml_dir, "pdf")

os.makedirs(xml_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)

# Conectar ao banco
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Consulta que retorna os XMLs
cursor.execute("{sua_consulta}")

# Exportar cada XML para arquivo
for row in cursor.fetchall():
    xml_content = str(row.XML_Retorno)
    file_name = f"xml_{row.Id}.xml"
    file_path = os.path.join(xml_dir, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"XML exportado: {file_path}")

cursor.close()
conn.close()

# Converter XMLs para PDF
for file in os.listdir(xml_dir):
    if file.endswith(".xml"):
        xml_path = os.path.join(xml_dir, file)

        # Parsear o XML
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Buscar os campos cUF e xNome
        cUF = root.find(".//cUF")
        xNome = root.find(".//xNome")

        cUF_val = cUF.text if cUF is not None else "NA"
        xNome_val = xNome.text if xNome is not None else "SemNome"

        # Nome do PDF baseado nos campos
        pdf_name = f"{cUF_val}_{xNome_val}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_name)

        # Ler conteúdo do XML
        with open(xml_path, "r", encoding="utf-8") as f:
            xml_text = f.read()

        # Criar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, xml_text)

        pdf.output(pdf_path)
        print(f"PDF gerado: {pdf_path}")