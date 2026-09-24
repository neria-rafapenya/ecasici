from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app.services.data_provider import MockDataProvider

app = FastAPI(title='ECA SICI CCTV Demo API', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
provider = MockDataProvider()


class MotionEventCreate(BaseModel):
    camera_id: str = Field(min_length=1)
    confidence: int = Field(ge=0, le=100)
    started_at: str = Field(min_length=1)
    event_type: str = 'person_detected'
    objects: list[dict] = Field(default_factory=list)
    zone: str = 'zona_no_configurada'
    direction: str | None = None


class MotionEventClose(BaseModel):
    ended_at: str = Field(min_length=1)
    duration_seconds: float = Field(ge=0)

@app.get('/api/health')
def health():
    return {'status': 'ok', 'mode': 'mock'}

@app.get('/api/dashboard')
def dashboard():
    return provider.dashboard()

@app.get('/api/cameras')
def cameras():
    return provider.cameras()


@app.get('/api/events')
def events():
    return provider.events()


@app.get('/api/event-taxonomy')
def event_taxonomy():
    return provider.taxonomy()


@app.post('/api/events', status_code=201)
def create_event(payload: MotionEventCreate):
    return provider.create_motion_event(payload.camera_id, payload.confidence, payload.started_at, payload.event_type, payload.objects, payload.zone, payload.direction)


@app.patch('/api/events/{event_id}')
def close_event(event_id: str, payload: MotionEventClose):
    event = provider.close_motion_event(event_id, payload.ended_at, payload.duration_seconds)
    if not event:
        raise HTTPException(status_code=404, detail='event_not_found')
    return event

@app.get('/api/installations/{installation_id}')
def installation(installation_id: str):
    return provider.installation(installation_id)
