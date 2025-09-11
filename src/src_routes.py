from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src.models import db, Client

def register_routes(app):
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route("/clients", methods=["GET"])
    def get_clients():
        clients = Client.query.all()
        return jsonify([{
            "id": c.id,
            "nom": c.nom,
            "email": c.email,
            "telephone": c.telephone,
            "adresse": c.adresse
        } for c in clients])

    @app.route("/clients", methods=["POST"])
    def add_client():
        data = request.json
        client = Client(
            nom=data.get("nom"),
            email=data.get("email"),
            telephone=data.get("telephone"),
            adresse=data.get("adresse")
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({"message": "Client ajouté", "id": client.id}), 201

    @app.route("/clients/<int:client_id>", methods=["PUT"])
    def update_client(client_id):
        client = Client.query.get_or_404(client_id)
        data = request.json
        client.nom = data.get("nom", client.nom)
        client.email = data.get("email", client.email)
        client.telephone = data.get("telephone", client.telephone)
        client.adresse = data.get("adresse", client.adresse)
        db.session.commit()
        return jsonify({"message": "Client mis à jour"})

    @app.route("/clients/<int:client_id>", methods=["DELETE"])
    def delete_client(client_id):
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Client supprimé"})