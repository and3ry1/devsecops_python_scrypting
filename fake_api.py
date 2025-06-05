from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import random
import time
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()

app = FastAPI()
API_TOKEN = os.getenv('API_TOKEN', 'your_default_token_here')

# 🔐 Middleware pour vérifier le token
@app.middleware('http')
async def check_token(request: Request, call_next):
    auth = request.headers.get('Authorization')
    if not auth or auth != f'Bearer {API_TOKEN}':
        logger.warning("❌ Requête non autorisée (mauvais token)")  # Log de sécurité
        return JSONResponse(status_code=401, content='{"detail": "Unauthorized: Invalid or missing token"}')
    logger.info(f"🔑 Requête autorisée depuis {request.client.host}")  # Log d'accès OK
    return await call_next(request)

# 📡 GET /status : retourne un état simulé
@app.get('/status')
def get_status(app: Optional[str] = 'unknown'):
    fake_response_time = round(random.uniform(0.1, 1.5), 2)
    status = random.choice(['OK', 'DEGRADED', 'DOWN'])
    time.sleep(0.5)

    logger.info(f"📥 /status appelé pour app={app} ➜ status={status}, response_time={fake_response_time}s")

    return JSONResponse(content={
        'app': app,
        'status': status,
        'response_time': fake_response_time,
        'timestamp': time.time()
    })

# 📥 POST /login : authentification simulée
class LoginData(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(data: LoginData):
    if not data.username.strip() or not data.password.strip():
        logger.error("🚫 Tentative de login sans identifiants valides")
        raise HTTPException(status_code=400, detail='Username and password are required')

    logger.info(f"✅ Login réussi pour l’utilisateur : {data.username}")
    return {"token": API_TOKEN}
