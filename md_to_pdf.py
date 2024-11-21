import markdown2
import pdfkit

# Convertir Markdown a HTML
with open("Primer_tetra/Base_De_Datos_Relacionales/TareaII_Modelo_Relacional.md", "r") as md_file:
    html_content = markdown2.markdown(md_file.read())

# Guardar como PDF
pdfkit.from_string(html_content, "prueba1.pdf")