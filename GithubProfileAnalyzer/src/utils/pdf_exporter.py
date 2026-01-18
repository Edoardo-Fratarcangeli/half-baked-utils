from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os
from datetime import datetime

def generate_pdf(data, chart_image_path, output_path):
    """
    Generates a PDF report with the profile analysis.
    
    data: dict containing 'name', 'site', 'username', 'target', 'commit_total', 'df'
    chart_image_path: path to the temporary chart image
    output_path: destination path for the PDF
    """
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    # Title
    elements.append(Paragraph("<b>Developer Profile</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Metadata
    meta = [
        f"Nome: {data.get('name', '')}",
        f"Sito: {data.get('site', '')}",
        f"GitHub: {data.get('username', '')}",
        f"Target: {data.get('target', '')}",
        f"Commit totali: {data.get('commit_total', 0)}",
        f"Data report: {datetime.now().strftime('%d/%m/%Y')}",
    ]

    for m in meta:
        elements.append(Paragraph(m, styles["Normal"]))

    elements.append(Spacer(1, 12))

    # Chart
    if os.path.exists(chart_image_path):
        elements.append(Image(chart_image_path, width=350, height=280))
        elements.append(Spacer(1, 12))

    # Table
    table_data = [["Linguaggio", "Bytes", "%"]]
    df = data.get('df')
    
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            table_data.append(
                [r["language"], int(r["bytes"]), f"{r['percentage']:.2f}%"]
            )

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))

    elements.append(table)
    doc.build(elements)
