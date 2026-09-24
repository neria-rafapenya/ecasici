from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.data_provider import MockDataProvider

app = FastAPI(title='ECA SICI CCTV Demo API', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
provider = MockDataProvider()

@app.get('/api/health')
def health():
    return {'status': 'ok', 'mode': 'mock'}

@app.get('/api/dashboard')
def dashboard():
    return provider.dashboard()

@app.get('/api/installations/{installation_id}')
def installation(installation_id: str):
    return provider.installation(installation_id)
