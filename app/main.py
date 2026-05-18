from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, Field

from app.monitor import SidewalkSafetyMonitor


app = FastAPI(
    title='Sidewalk Safety Monitoring',
    version='2.0.0',
    description='Public case study for sidewalk dwell-time monitoring and camera health operations.',
)
monitor = SidewalkSafetyMonitor()


class PersonDetectionIn(BaseModel):
    track_id: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: list[float] = Field(min_length=4, max_length=4)
    elapsed_s: float = Field(ge=0.0)


@app.get('/', response_class=HTMLResponse)
def index() -> str:
    return '''
    <main style="font-family:system-ui;max-width:920px;margin:40px auto;line-height:1.5">
      <p style="text-transform:uppercase;font-size:12px;letter-spacing:.08em;color:#476582">public case study</p>
      <h1>Sidewalk Safety Monitoring</h1>
      <p>
        Sanitized monitoring service for sidewalk cameras: ROI, person tracks,
        dwell-time threshold, camera runtime and operator events.
        Dahua/Intelbras is represented as one operational platform family in this demo.
      </p>
      <ul>
        <li><a href="/api/sidewalk/cameras">Configured cameras</a></li>
        <li><a href="/api/sidewalk/events">Events</a></li>
        <li><a href="/api/demo/sidewalk-camera/snapshot.svg">Synthetic snapshot</a></li>
      </ul>
      <p>Use <code>POST /api/demo/sidewalk-dwell</code> to create a synthetic sidewalk dwell event.</p>
    </main>
    '''


@app.get('/api/sidewalk/cameras')
def cameras() -> list[dict]:
    return monitor.cameras()


@app.get('/api/sidewalk/cameras/{camera_id}/runtime')
def runtime(camera_id: str) -> dict:
    if camera_id not in monitor.camera_ids():
        raise HTTPException(status_code=404, detail='Camera not found')
    return monitor.runtime(camera_id)


@app.post('/api/sidewalk/cameras/{camera_id}/detections')
def ingest_detection(camera_id: str, payload: PersonDetectionIn) -> dict:
    if camera_id not in monitor.camera_ids():
        raise HTTPException(status_code=404, detail='Camera not found')
    return monitor.ingest_detection(
        camera_id=camera_id,
        track_id=payload.track_id,
        confidence=payload.confidence,
        bbox=payload.bbox,
        elapsed_s=payload.elapsed_s,
    )


@app.post('/api/demo/sidewalk-dwell')
def demo_sidewalk_dwell() -> dict:
    return monitor.ingest_detection(
        camera_id='sidewalk-front-a01',
        track_id='person-509',
        confidence=0.89,
        bbox=[0.42, 0.22, 0.55, 0.88],
        elapsed_s=342.0,
    )


@app.get('/api/sidewalk/events')
def events() -> list[dict]:
    return monitor.events()


@app.get('/api/system/health')
def health() -> dict:
    return monitor.health()


@app.get('/api/demo/sidewalk-camera/snapshot.svg')
def synthetic_snapshot() -> Response:
    svg = '''
    <svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">
      <rect width="960" height="540" fill="#172033"/>
      <rect x="90" y="330" width="780" height="90" fill="#4b5563"/>
      <rect x="90" y="420" width="780" height="55" fill="#1f2937"/>
      <polygon points="230,140 720,130 800,420 170,420" fill="rgba(61,220,151,.18)" stroke="#3ddc97" stroke-width="4"/>
      <rect x="430" y="205" width="86" height="190" fill="rgba(74,168,255,.30)" stroke="#4aa8ff" stroke-width="4"/>
      <circle cx="472" cy="180" r="28" fill="rgba(74,168,255,.30)" stroke="#4aa8ff" stroke-width="4"/>
      <text x="118" y="88" font-family="Arial" font-size="32" fill="#f9fafb">Synthetic sidewalk monitoring frame</text>
      <text x="118" y="126" font-family="Arial" font-size="20" fill="#cbd5e1">ROI, person track and dwell-time event boundary</text>
    </svg>
    '''
    return Response(svg.strip(), media_type='image/svg+xml')
