import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import tempfile
import os

def generate_pdf(df, stats, output_path):
    tmp_dir = tempfile.mkdtemp()

    # Ensure Date is in datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Generate charts
    df['Month'] = df['Date'].dt.strftime('%b')
    monthly = df.groupby("Month")["Sales"].sum()
    monthly.plot(kind='bar', title='Monthly Sales')
    chart1 = os.path.join(tmp_dir, "monthly.png")
    plt.savefig(chart1); plt.close()

    region = df.groupby("Region")["Sales"].sum()
    region.plot(kind='bar', title='Sales by Region')
    chart2 = os.path.join(tmp_dir, "region.png")
    plt.savefig(chart2); plt.close()

    product = df.groupby("Product")["Sales"].sum()
    product.plot(kind='pie', autopct='%1.1f%%')
    plt.ylabel("")
    plt.title("Product Share")
    chart3 = os.path.join(tmp_dir, "product.png")
    plt.savefig(chart3); plt.close()

    # Build PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("📊 Detailed Sales Report", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    
    for k, v in stats.items():
        story.append(Paragraph(f"<b>{k}:</b> {v}", styles['BodyText']))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Image(chart1, width=5*inch, height=3*inch))
    story.append(Image(chart2, width=5*inch, height=3*inch))
    story.append(Image(chart3, width=4*inch, height=4*inch))

    doc.build(story)
