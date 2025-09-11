from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
CORS(app)

COMPANY_INFO = {
    "name": "SAMASSA TECHNOLOGIE",
    "slogan": "Tout pour l’informatique",
    "address": "Grand Marché de Kayes, près du 1er arrondissement de la police, Rue Soundiata Keita",
    "phone": "00223 77291931",
    "email": "samassatechnologie10@gmail.com"
}

@app.route("/")
def home():
    return "Backend SAMASSA est en ligne ✅"

@app.route("/api/generate_invoice", methods=["POST"])
def generate_invoice():
    data = request.json or {}
    invoice_number = data.get("invoice_number", "SAM-001")
    client_name = data.get("client_name", "Client Test")
    items = data.get("items", [{"description":"Service informatique","qty":1,"price":10000}])

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # --- En-tête avec logo + infos société
    try:
        logo = Image("logo.png", width=80, height=80)
        elements.append(logo)
    except:
        elements.append(Paragraph("<b>[Logo manquant]</b>", styles["Normal"]))
    elements.append(Paragraph(f"<b>{COMPANY_INFO['name']}</b>", styles["Title"]))
    elements.append(Paragraph(COMPANY_INFO["slogan"], styles["Normal"]))
    elements.append(Paragraph(COMPANY_INFO["address"], styles["Normal"]))
    elements.append(Paragraph(f"Tél: {COMPANY_INFO['phone']} — {COMPANY_INFO['email']}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # --- Infos facture
    elements.append(Paragraph(f"<b>FACTURE N° {invoice_number}</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Client : {client_name}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # --- Tableau des articles
    data_table = [["Description", "Quantité", "Prix Unitaire (F)", "Total (F)"]]
    total_general = 0
    for it in items:
        desc = it.get("description", "")
        qty = float(it.get("qty", 1))
        price = float(it.get("price", 0))
        total = qty * price
        total_general += total
        data_table.append([desc, f"{int(qty)}", f"{int(price):,}", f"{int(total):,}"])

    data_table.append(["", "", "TOTAL", f"{int(total_general):,}"])

    table = Table(data_table, colWidths=[200, 80, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 30))

    # --- Pied de page
    elements.append(Paragraph("<b>Merci pour votre confiance !</b>", styles["Normal"]))
    elements.append(Paragraph("SAMASSA TECHNOLOGIE — Tout pour l’informatique", styles["Italic"]))

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf",
                     as_attachment=True, download_name=f"facture_{invoice_number}.pdf")
@app.route("/api/generate_devis", methods=["POST"])
def generate_devis():
    data = request.json or {}
    devis_number = data.get("devis_number", "DEV-001")
    client_name = data.get("client_name", "Client Test")
    items = data.get("items", [{"description":"Service proposé","qty":1,"price":10000}])

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # --- En-tête
    try:
        logo = Image("logo.png", width=80, height=80)
        elements.append(logo)
    except:
        elements.append(Paragraph("<b>[Logo manquant]</b>", styles["Normal"]))
    elements.append(Paragraph(f"<b>{COMPANY_INFO['name']}</b>", styles["Title"]))
    elements.append(Paragraph(COMPANY_INFO["slogan"], styles["Normal"]))
    elements.append(Spacer(1, 20))

    # --- Infos devis
    elements.append(Paragraph(f"<b>DEVIS N° {devis_number}</b>", styles["Heading2"]))
    elements.append(Paragraph(f"Client : {client_name}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # --- Tableau des articles
    data_table = [["Description", "Quantité", "Prix Unitaire (F)", "Total (F)"]]
    total_general = 0
    for it in items:
        desc = it.get("description", "")
        qty = float(it.get("qty", 1))
        price = float(it.get("price", 0))
        total = qty * price
        total_general += total
        data_table.append([desc, f"{int(qty)}", f"{int(price):,}", f"{int(total):,}"])

    data_table.append(["", "", "TOTAL", f"{int(total_general):,}"])

    table = Table(data_table, colWidths=[200, 80, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#059669")),  # vert
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 30))

    # --- Pied de page
    elements.append(Paragraph("<b>Valable 30 jours à compter de la date d’émission.</b>", styles["Normal"]))
    elements.append(Paragraph("SAMASSA TECHNOLOGIE — Tout pour l’informatique", styles["Italic"]))

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf",
                     as_attachment=True, download_name=f"devis_{devis_number}.pdf")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
