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
# fake_api.py


app = FastAPI()
API_TOKEN = os.getenv('API_TOKEN', 'your_default_token_here')


#middleware pour vérifier le token d'authentification
# Si le token n'est pas présent ou incorrect, renvoie une erreur 401 Unauthorized
@app.middleware('http')
async def check_token(request: Request, call_next):
  auth = request.headers.get('Authorization')
  if not auth or auth != f'Bearer {API_TOKEN}':
    return JSONResponse(status_code=401, content = '{"detail": "Unauthorized: Invalid or missing token"}')  
    raise HTTPException(status_code=401, detail='Unauthorized: Invalid or missing token')
  return await call_next(request)


#route Get/status - statut simulé
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

#route POST /login - login simulé


class LoginData(BaseModel):
    username: str
    password: str

@app.post('/login')
def login(data: LoginData):
    if not data.username.strip() or not data.password.strip():
        raise HTTPException(status_code=400, detail='Username and password are required')
    return {"token": API_TOKEN}


