import os
import subprocess
from datetime import datetime

# Crée le dossier "audit" s'il n'existe pas
os.makedirs("audit", exist_ok=True)

# Date du jour pour les fichiers
today = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# --- 1. Analyse Bandit ---
bandit_output = f"audit/bandit_report_{today}.txt"
print(f" Analyse de sécurité avec Bandit...")

with open(bandit_output, "w") as f:
    subprocess.run(["bandit", "-r", "."], stdout=f)

print(f"Rapport Bandit sauvegardé dans {bandit_output}")

# --- 2. Audit des dépendances ---
audit_output = f"audit/pip_audit_report_{today}.txt"
print(f"🔬 Analyse des dépendances avec pip-audit...")

with open(audit_output, "w") as f:
    subprocess.run(["pip-audit"], stdout=f)

print(f"✅ Rapport pip-audit sauvegardé dans {audit_output}")
