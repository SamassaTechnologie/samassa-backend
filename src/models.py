from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.String(200))

class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    montant = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20))
    statut = db.Column(db.String(20))

class Intervention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    description = db.Column(db.Text)
    date = db.Column(db.String(20))
