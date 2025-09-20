from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

# SQLite config (file samassa.db will be created in the app folder)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///samassa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ---------- Models ----------
class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(64), unique=True, nullable=False)
    client = db.Column(db.String(200), nullable=False)
    total = db.Column(db.Float, nullable=False)
    items = db.Column(db.Text)  # JSON string of items
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Devis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(64), unique=True, nullable=False)
    client = db.Column(db.String(200), nullable=False)
    total = db.Column(db.Float, nullable=False)
    items = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(64), unique=True, nullable=False)
    client = db.Column(db.String(200), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    moyen = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Initialize DB ----------
with app.app_context():
    db.create_all()

# ---------- Helper ----------
def ok(data=None, message="OK"):
    payload = {"message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload)

# ---------- Factures endpoints ----------
@app.route("/api/factures", methods=["GET"])
def list_factures():
    rows = Facture.query.order_by(Facture.created_at.desc()).all()
    return jsonify([{
        "id": r.id, "numero": r.numero, "client": r.client,
        "total": r.total, "items": r.items, "created_at": r.created_at.isoformat()
    } for r in rows])

@app.route("/api/factures", methods=["POST"])
def create_facture():
    data = request.json or {}
    # minimal validation
    numero = data.get("numero")
    client = data.get("client")
    total = float(data.get("total", 0))
    items = data.get("items", "[]")
    if not numero or not client:
        return jsonify({"error": "numero and client required"}), 400
    f = Facture(numero=numero, client=client, total=total, items=str(items))
    db.session.add(f)
    db.session.commit()
    return ok({"id": f.id}, "Facture created")

@app.route("/api/factures/<int:id>", methods=["DELETE"])
def delete_facture(id):
    f = Facture.query.get(id)
    if not f:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(f)
    db.session.commit()
    return ok(message="Facture deleted")

# ---------- Devis endpoints ----------
@app.route("/api/devis", methods=["GET"])
def list_devis():
    rows = Devis.query.order_by(Devis.created_at.desc()).all()
    return jsonify([{
        "id": r.id, "numero": r.numero, "client": r.client,
        "total": r.total, "items": r.items, "created_at": r.created_at.isoformat()
    } for r in rows])

@app.route("/api/devis", methods=["POST"])
def create_devis():
    data = request.json or {}
    numero = data.get("numero")
    client = data.get("client")
    total = float(data.get("total", 0))
    items = data.get("items", "[]")
    if not numero or not client:
        return jsonify({"error": "numero and client required"}), 400
    d = Devis(numero=numero, client=client, total=total, items=str(items))
    db.session.add(d)
    db.session.commit()
    return ok({"id": d.id}, "Devis created")

@app.route("/api/devis/<int:id>", methods=["DELETE"])
def delete_devis(id):
    d = Devis.query.get(id)
    if not d:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(d)
    db.session.commit()
    return ok(message="Devis deleted")

# ---------- Recus endpoints ----------
@app.route("/api/recus", methods=["GET"])
def list_recus():
    rows = Recu.query.order_by(Recu.created_at.desc()).all()
    return jsonify([{
        "id": r.id, "numero": r.numero, "client": r.client,
        "montant": r.montant, "moyen": r.moyen, "created_at": r.created_at.isoformat()
    } for r in rows])

@app.route("/api/recus", methods=["POST"])
def create_recu():
    data = request.json or {}
    numero = data.get("numero")
    client = data.get("client")
    montant = float(data.get("montant", 0))
    moyen = data.get("moyen", "")
    if not numero or not client:
        return jsonify({"error": "numero and client required"}), 400
    r = Recu(numero=numero, client=client, montant=montant, moyen=moyen)
    db.session.add(r)
    db.session.commit()
    return ok({"id": r.id}, "Reçu created")

@app.route("/api/recus/<int:id>", methods=["DELETE"])
def delete_recu(id):
    r = Recu.query.get(id)
    if not r:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(r)
    db.session.commit()
    return ok(message="Reçu deleted")

# ---------- Health ----------
@app.route("/", methods=["GET"])
def home():
    return "SAMASSA backend (data API) is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
