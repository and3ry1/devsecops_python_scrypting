# devsecops_python_scrypting
🎯 Objectif du TP

Créer un outil de surveillance sécurisé qui :

Appelle une API (simulée en local),
Sauvegarde les résultats dans des fichiers,
Utilise des logs structurés,
Respecte les bonnes pratiques de sécurité (DevSecOps),
Passe des audits (Bandit, pip-audit).

1. Préparation de l’environnement
Vous allez créer une structure du projet qui ressemble à cela :


│
├── monitor.py
├── fake_api.py
├── .env
├── .env.example
├── requirements.txt
├── logs/
└── reports/
Le projet doit être versionné sur Github.

🔧 Installation
Le fichier requirements.txt aura au minimum :


requests
python-dotenv
fastapi
uvicorn
mysql-connector-python # facultatif pour bonus
Pour rappel :


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
🧪 2. Mise en place de l’API simulée
📌 Créer un serveur Flask local

Voici un fichier fake_api.py fait par un stagiaire Chad Gépaité, il ne marche pas forcément. Pour être sûr, on pourra checker la doc de FastAPI.


from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import random
import time

app = FastAPI()

API_TOKEN = 'CeciEstUnTokenDeTestVousPouvezLeCacherDansDotEnv'

@app.middleware('http')
async def check_token(request: Request, call_next):
  auth = request.headers.get('Authorization')
  if not auth or auth != f'Bearer {API_TOKEN}':
    raise HTTPException(status_code=401, detail='Unauthorized: Invalid or missing token')
  return await call_next(request)

@app.get('/status')
def get_status(app: Optional[str] = 'unknown'):
  fake_response_time = round(random.uniform(0.1, 1.5), 2)
  status = random.choice(['OK', 'DEGRADED', 'DOWN'])
  time.sleep(0.5)

  return JSONResponse(content={
    'app': app,
    'status': status,
    'response_time': fake_response_time,
    'timestamp': time.time()
  })
On peut lancer l'API avec :


uvicorn fake_api:app --reload
Elle écoute sur : http://127.0.0.1:8000/status?app=NomApp

En bonus, vous pouvez ajouter une route /login en POST où on envoie un login et un mot de passe (username et password) et si les champs ne sont pas vides, on envoie le token en réponse.

🔐 3. Création du script de surveillance
📌 Écrire monitor.py

Fonctionnalités :

Charge les secrets depuis .env
Appelle l’API avec timeout
Sauvegarde les résultats dans reports/
Loggue dans logs/
Tiens en bonus, on voudrait pouvoir monitorer plusieurs applications en fonction d'une liste ou d'un fichier.

🧪 4. Audit sécurité
🔎 Analyse statique avec Bandit


pip install bandit
bandit -r .
🧬 Analyse des dépendances


pip install pip-audit
pip-audit
Créer un script check_code.py qui lance la validation automatiquement.

📜 5. Bonnes pratiques de logs
Utiliser logging avec RotatingFileHandler
Format lisible et horodaté
Ne jamais logguer de secrets
Créer un répertoire logs/ si nécessaire
En bonus, pour ceux qui sont vraiment motivés, on peut créer un handler custom pour sauvegarder les log de logging dans Mongo.

🧾 6. Fichier .env
Fichier .env :


API_TOKEN=
API_URL=
APPS=
🐬 7. Bonus – Sauvegarde en base MySQL (optionnel)
Voici le script pour créer la table :


create table app_status (
  id int auto_increment primary key,
  timestamp datetime,
  app_name varchar(255),
  status varchar(50),
  response_time float
)
Insérer les données depuis Python avec mysql-connector-python.

✅ 8. Résultat attendu
Script exécutable :


python monitor.py
Résultat :

✅ Un log propre
✅ Un fichier ./reports/2025-06-04-App.json
✅ Pas de secret en clair
✅ Audit OK