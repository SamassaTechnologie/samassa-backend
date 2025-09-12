from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import io
from reportlab.pdfgen import canvas

app = Flask(__name__)
CORS(app)

# Config SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///samassa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# -------------------------------
# MODELES
# -------------------------------
class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True)
    client = db.Column(db.String(100))
    total = db.Column(db.Float)

class Devis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True)
    client = db.Column(db.String(100))
    total = db.Column(db.Float)

class Recu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True)
    client = db.Column(db.String(100))
    montant = db.Column(db.Float)
    moyen = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# -------------------------------
# ROUTES FACTURES
# -------------------------------
@app.route("/api/factures", methods=["GET"])
def get_factures():
    factures = Facture.query.all()
    return jsonify([{"id": f.id, "numero": f.numero, "client": f.client, "total": f.total} for f in factures])

@app.route("/api/factures", methods=["POST"])
def add_facture():
    data = request.json
    new_facture = Facture(numero=data["numero"], client=data["client"], total=data["total"])
    db.session.add(new_facture)
    db.session.commit()
    return {"message": "Facture ajoutée"}

@app.route("/api/factures/<int:id>", methods=["DELETE"])
def delete_facture(id):
    facture = Facture.query.get(id)
    if facture:
        db.session.delete(facture)
        db.session.commit()
        return {"message": "Facture supprimée"}
    return {"error": "Facture introuvable"}, 404

@app.route("/api/generate_invoice", methods=["POST"])
def generate_invoice():
    data = request.json
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, f"FACTURE N° {data['numero']}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Client : {data['client']}")
    p.drawString(100, 750, f"Total : {data['total']} F CFA")
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"facture_{data['numero']}.pdf", mimetype="application/pdf")

# -------------------------------
# ROUTES DEVIS
# -------------------------------
@app.route("/api/devis", methods=["GET"])
def get_devis():
    devis = Devis.query.all()
    return jsonify([{"id": d.id, "numero": d.numero, "client": d.client, "total": d.total} for d in devis])

@app.route("/api/devis", methods=["POST"])
def add_devis():
    data = request.json
    new_devis = Devis(numero=data["numero"], client=data["client"], total=data["total"])
    db.session.add(new_devis)
    db.session.commit()
    return {"message": "Devis ajouté"}

@app.route("/api/devis/<int:id>", methods=["DELETE"])
def delete_devis(id):
    devis = Devis.query.get(id)
    if devis:
        db.session.delete(devis)
        db.session.commit()
        return {"message": "Devis supprimé"}
    return {"error": "Devis introuvable"}, 404

@app.route("/api/generate_devis", methods=["POST"])
def generate_devis():
    data = request.json
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, f"DEVIS N° {data['numero']}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Client : {data['client']}")
    p.drawString(100, 750, f"Total : {data['total']} F CFA")
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"devis_{data['numero']}.pdf", mimetype="application/pdf")

# -------------------------------
# ROUTES RECUS
# -------------------------------
@app.route("/api/recus", methods=["GET"])
def get_recus():
    recus = Recu.query.all()
    return jsonify([{"id": r.id, "numero": r.numero, "client": r.client, "montant": r.montant, "moyen": r.moyen} for r in recus])

@app.route("/api/recus", methods=["POST"])
def add_recu():
    data = request.json
    new_recu = Recu(numero=data["numero"], client=data["client"], montant=data["montant"], moyen=data["moyen"])
    db.session.add(new_recu)
    db.session.commit()
    return {"message": "Reçu ajouté"}

@app.route("/api/recus/<int:id>", methods=["DELETE"])
def delete_recu(id):
    recu = Recu.query.get(id)
    if recu:
        db.session.delete(recu)
        db.session.commit()
        return {"message": "Reçu supprimé"}
    return {"error": "Reçu introuvable"}, 404

@app.route("/api/generate_recu", methods=["POST"])
def generate_recu():
    data = request.json
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, f"REÇU N° {data['numero']}")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Client : {data['client']}")
    p.drawString(100, 750, f"Montant : {data['montant']} F CFA")
    p.drawString(100, 730, f"Moyen : {data['moyen']}")
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"recu_{data['numero']}.pdf", mimetype="application/pdf")

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
