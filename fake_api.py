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
    return JSONResponse(status_code=401, content = '{"detail": "Unauthorized: Invalid or missing token"}')  
#raise HTTPException(status_code=401, detail='Unauthorized: Invalid or missing token')
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
