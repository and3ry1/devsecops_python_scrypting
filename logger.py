import logging
from logging.handlers import RotatingFileHandler
import os

# 📁 Crée le dossier "logs" s’il n’existe pas déjà
os.makedirs("logs", exist_ok=True)

# 🏷️ Création d’un logger nommé "app_logger"
logger = logging.getLogger("app_logger")

# 🛠️ Niveau de log par défaut = INFO
# Autres niveaux possibles : DEBUG, WARNING, ERROR, CRITICAL
logger.setLevel(logging.INFO)

# 🔁 RotatingFileHandler : gère les fichiers de logs avec rotation
# - logs/app.log : chemin du fichier log
# - maxBytes : taille max avant de créer un nouveau fichier (ici 1 Mo)
# - backupCount : nombre de fichiers à garder avant de supprimer les plus anciens (ici 5)
handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=1_000_000,
    backupCount=5
)

# 📄 Définition du format du log :
# - %(asctime)s : date/heure
# - %(levelname)s : niveau du message (INFO, ERROR...)
# - %(message)s : contenu du log
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s: %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

# 🔗 On associe le format au handler
handler.setFormatter(formatter)

# 🔄 On évite de rajouter plusieurs fois le même handler (exécution multiple du script)
if not logger.hasHandlers():
    logger.addHandler(handler)
