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
    title_style = styles["Title"]
    title_style.textColor = colors.navy
    elements.append(Paragraph("<b>GitHub Profile Analysis</b>", title_style))
    elements.append(Spacer(1, 20))

    # Metadata
    meta_style = styles["Normal"]
    meta_style.fontSize = 12
    meta_style.leading = 16
    
    meta_data = [
        ("Author", data.get('name', 'N/A')),
        ("Website", data.get('site', 'N/A')),
        ("Target Role", data.get('target', 'N/A')),
        ("Analyzed Profile", data.get('username', 'N/A')),
        ("Total Commits", str(data.get('commit_total', 0))),
        ("Date", datetime.now().strftime('%d/%m/%Y'))
    ]

    # Create a small table for metadata to look cleaner
    meta_table_data = [[Paragraph(f"<b>{k}:</b>", meta_style), Paragraph(v, meta_style)] for k, v in meta_data]
    meta_table = Table(meta_table_data, colWidths=[120, 300])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.darkblue),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 20))

    # Chart
    if os.path.exists(chart_image_path):
        # Center the image
        img = Image(chart_image_path, width=400, height=320)
        elements.append(img)
        elements.append(Spacer(1, 20))

    # Data Processing for Table
    df = data.get('df')
    threshold = data.get('threshold', 5)
    others_list = []
    
    table_data = [["Language", "Bytes", "Percentage"]]
    
    if df is not None and not df.empty:
        # Filter logic
        main_mask = df["percentage"] >= threshold
        main_rows = df[main_mask]
        others_rows = df[~main_mask]

        # Add main rows
        for _, r in main_rows.iterrows():
            table_data.append(
                [r["language"], f"{int(r['bytes']):,}", f"{r['percentage']:.2f}%"]
            )
        
        # Add "Others" row if needed
        if not others_rows.empty:
            others_bytes = others_rows["bytes"].sum()
            others_pct = others_rows["percentage"].sum()
            table_data.append(
                ["Others", f"{int(others_bytes):,}", f"{others_pct:.2f}%"]
            )
            others_list = others_rows["language"].tolist()

    # Table Style
    table = Table(table_data, colWidths=[200, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'), # Align numbers to right
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Others Footnote
    if others_list:
        small_style = styles["Normal"]
        small_style.fontSize = 8
        small_style.textColor = colors.grey
        others_text = "<b>* Others includes:</b> " + ", ".join(others_list)
        elements.append(Paragraph(others_text, small_style))

    doc.build(elements)
