import os
import requests
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv
import json

#  Charge les secrets depuis .env
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', 'your_default_token_here')
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000/status')

def load_apps():
    apps = []
    if os.path.exists('apps.txt'):
        with open('apps.txt', 'r') as f:
            apps = f.read().splitlines()
    else:
        apps = os.getenv('APPS', 'my_app').split(',')
    return [app.strip() for app in apps if app.strip()]

# Crée les dossiers nécessaires
os.makedirs("logs", exist_ok=True)
os.makedirs("reports", exist_ok=True)

#  Loggue dans logs/
logger = logging.getLogger('monitor')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('logs/monitor.log', maxBytes=5*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#  Vérifie que l'URL API est correcte
if not API_URL.startswith('http'):
    logger.error("API_URL must start with 'http' or 'https'")
    raise ValueError("Invalid API_URL configuration")
logger.info(f"Using API_URL: {API_URL}")

def get_status(app: str = 'unknown'):
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    try:
        # Appelle l’API avec timeout
        response = requests.get(API_URL, headers=headers, params={'app': app}, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Status for {app}: {data}")
        return data
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {'error': 'HTTP error occurred', 'details': str(http_err)}
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        return {'error': 'Request error occurred', 'details': str(req_err)}

def save_report(data, app_name):
    # Sauvegarde les résultats dans reports/
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"reports/{date_str}-{app_name}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def main():
    for app_name in APPS:
        status = get_status(app=app_name.strip())
        if 'error' in status:
            logger.error(f"Failed to retrieve status for {app_name}: {status['details']}")
        else:
            save_report(status, app_name)
            logger.info(f"Status for {app_name} saved successfully.")

if __name__ == '__main__':
    main()
