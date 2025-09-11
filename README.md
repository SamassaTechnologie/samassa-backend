# samassa-backend

API minimale prête pour Render (Flask).

## Commandes (local)
- Installer dépendances:
  ```
  pip install -r requirements.txt
  ```
- Lancer localement:
  ```
  python app.py
  ```
- Pour la production sur Render, la commande de démarrage recommandée est:
  ```
  gunicorn app:app
  ```

## Endpoints disponibles
- `/` : page d'accueil
- `/api/clients` : GET → liste clients de démonstration
- `/api/generate_invoice` : POST → génère une facture PDF (JSON attendu)

Exemple de payload pour `/api/generate_invoice`:
```
{
  "invoice_number":"SAM-001",
  "client_name":"Client Test",
  "items":[{"description":"Intervention","qty":1,"price":15000}]
}
```

> Note: Ce backend utilise `reportlab` pour générer un PDF simple sans dépendances système lourdes.
> Si tu veux utiliser `WeasyPrint` (meilleure mise en forme HTML → PDF), il faudra ajouter des bibliothèques système (cairo, pango) qui sont plus complexes sur Render.