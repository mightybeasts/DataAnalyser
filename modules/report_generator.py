import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import tempfile
import os

def generate_pdf(df, stats, output_path):
    import matplotlib.dates as mdates

    tmp_dir = tempfile.mkdtemp()

    # Ensure Date is in datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Monthly Sales Chart
    df['Month'] = df['Date'].dt.strftime('%b')
    monthly = df.groupby("Month")["Sales"].sum()
    monthly.plot(kind='bar', title='Monthly Sales', color='skyblue')
    chart1 = os.path.join(tmp_dir, "monthly.png")
    plt.tight_layout()
    plt.savefig(chart1); plt.close()

    # Region-wise Sales Chart
    region = df.groupby("Region")["Sales"].sum()
    region.plot(kind='bar', title='Sales by Region', color='orange')
    chart2 = os.path.join(tmp_dir, "region.png")
    plt.tight_layout()
    plt.savefig(chart2); plt.close()

    # Product-wise Pie Chart
    product = df.groupby("Product")["Sales"].sum()
    product.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.ylabel("")
    plt.title("Product Share")
    chart3 = os.path.join(tmp_dir, "product.png")
    plt.tight_layout()
    plt.savefig(chart3); plt.close()

    # Sales Trend Line Chart
    df = df.sort_values("Date")
    plt.figure(figsize=(8, 4))
    plt.plot(df["Date"], df["Sales"], marker='o', linestyle='-', color='royalblue')
    plt.fill_between(df["Date"], df["Sales"], color='lightblue', alpha=0.5)
    plt.title("Sales Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
    plt.gcf().autofmt_xdate()
    chart4 = os.path.join(tmp_dir, "trend.png")
    plt.tight_layout()
    plt.savefig(chart4); plt.close()

    # Build PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Detailed Sales Report", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))

    for k, v in stats.items():
        story.append(Paragraph(f"<b>{k}:</b> {v}", styles['BodyText']))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Image(chart1, width=5*inch, height=3*inch))
    story.append(Image(chart2, width=5*inch, height=3*inch))
    story.append(Image(chart3, width=4*inch, height=4*inch))
    story.append(Image(chart4, width=5.5*inch, height=3*inch))  # Sales Trend

    doc.build(story)
