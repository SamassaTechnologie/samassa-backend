# SAMASSA BACKEND

Backend Flask pour la suite de gestion SAMASSA TECHNOLOGIE.

## Installation locale

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=src/app.py
flask run
```

## Structure

- `src/app.py` : point d’entrée Flask
- `src/models.py` : modèles de données
- `src/routes.py` : routes API REST
- `src/pdf_utils.py` : utilitaires PDF

## Déploiement sur Render

1. Pousse tout le code sur GitHub.
2. Sur [render.com](https://render.com), crée un nouveau **Web Service** :
   - Build command : `pip install -r requirements.txt`
   - Start command : `gunicorn src.app:app`
   - Python version : 3.10 ou 3.11
3. Ajoute la variable d’environnement si besoin :  
   - `FLASK_ENV=production`
4. Dès que le service est live, note l’URL pour le frontend.

## Contact

SAMASSA TECHNOLOGIE — « Tout pour l’informatique »