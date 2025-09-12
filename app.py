from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///samassa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

COMPANY_INFO = {
    "name": "SAMASSA TECHNOLOGIE",
    "slogan": "Tout pour l’informatique",
    "address": "Grand Marché de Kayes, près du 1er arrondissement de la police, Rue Soundiata Keita",
    "phone": "00223 77291931",
    "email": "samassatechnologie10@gmail.com"
}

class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    client = db.Column(db.String(120), nullable=False)
    total = db.Column(db.Integer, nullable=False)

class Devis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    client = db.Column(db.String(120), nullable=False)
    total = db.Column(db.Integer, nullable=False)

class Recu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    client = db.Column(db.String(120), nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    moyen = db.Column(db.String(50), nullable=False)

def footer(elements, styles):
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        "SAMASSA TECHNOLOGIE – Tout pour l’informatique – "
        "Grand Marché de Kayes – 00223 77291931 – samassatechnologie10@gmail.com",
        styles["Italic"]
    ))

@app.route("/")
def home():
    return "Backend SAMASSA avec base SQLite est en ligne ✅"

@app.route("/api/factures", methods=["POST"])
def add_facture():
    data = request.json
    facture = Facture(numero=data["numero"], client=data["client"], total=data["total"])
    db.session.add(facture)
    db.session.commit()
    return {"message": "Facture enregistrée", "id": facture.id}

@app.route("/api/factures", methods=["GET"])
def list_factures():
    factures = Facture.query.all()
    return jsonify([{"id": f.id, "numero": f.numero, "client": f.client, "total": f.total} for f in factures])

@app.route("/api/devis", methods=["POST"])
def add_devis():
    data = request.json
    devis = Devis(numero=data["numero"], client=data["client"], total=data["total"])
    db.session.add(devis)
    db.session.commit()
    return {"message": "Devis enregistré", "id": devis.id}

@app.route("/api/devis", methods=["GET"])
def list_devis():
    devis = Devis.query.all()
    return jsonify([{"id": d.id, "numero": d.numero, "client": d.client, "total": d.total} for d in devis])

@app.route("/api/recus", methods=["POST"])
def add_recu():
    data = request.json
    recu = Recu(numero=data["numero"], client=data["client"], montant=data["montant"], moyen=data["moyen"])
    db.session.add(recu)
    db.session.commit()
    return {"message": "Reçu enregistré", "id": recu.id}

@app.route("/api/recus", methods=["GET"])
def list_recus():
    recus = Recu.query.all()
    return jsonify([{"id": r.id, "numero": r.numero, "client": r.client, "montant": r.montant, "moyen": r.moyen} for r in recus])

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
