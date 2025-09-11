from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)
CORS(app)

COMPANY_INFO = {
    "name": "SAMASSA TECHNOLOGIE",
    "address": "Grand Marché de Kayes, Rue Soundiata Keita",
    "phone": "00223 77291931",
    "email": "samassatechnologie10@gmail.com",
    "slogan": "Tout pour l'informatique"
}

@app.route("/")
def home():
    return "SAMASSA Backend est en ligne ✅"

@app.route("/api/clients", methods=["GET"])
def clients():
    sample = [
        {"id":1,"name":"Client A","phone":"+223 70000001"},
        {"id":2,"name":"Client B","phone":"+223 70000002"}
    ]
    return jsonify(sample)

@app.route("/api/generate_invoice", methods=["POST"])
def generate_invoice():
    data = request.json or {}
    invoice_number = data.get("invoice_number", "SAM-001")
    client_name = data.get("client_name", "Client Test")
    items = data.get("items", [{"description":"Service","qty":1,"price":10000}])
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, COMPANY_INFO["name"])
    c.setFont("Helvetica", 10)
    y -= 20
    c.drawString(50, y, COMPANY_INFO["address"])
    y -= 15
    c.drawString(50, y, f"Tél: {COMPANY_INFO['phone']} - {COMPANY_INFO['email']}")
    y -= 25
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Facture: {invoice_number}")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Client: {client_name}")
    y -= 25
    c.drawString(50, y, "Description")
    c.drawString(350, y, "Qte")
    c.drawString(420, y, "Prix U")
    c.drawString(500, y, "Total")
    y -= 15
    total = 0
    for it in items:
        desc = it.get("description", "")
        qty = float(it.get("qty", 1))
        price = float(it.get("price", 0))
        line_total = qty * price
        total += line_total
        c.drawString(50, y, desc)
        c.drawString(350, y, str(int(qty)))
        c.drawString(420, y, f"{int(price)}")
        c.drawString(500, y, f"{int(line_total)}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y, "TOTAL:")
    c.drawString(500, y, f"{int(total)}")
    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name=f"invoice_{invoice_number}.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)