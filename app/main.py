from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response

from app.providers import Camera, PROVIDERS


app = FastAPI(
    title="Live Stream Gateway Demo",
    version="1.0.0",
    description="Public-safe multi-vendor live stream gateway demo.",
)


CAMERAS = [
    Camera("cam-social-01", "Elevator Social", "Demo Tower", "generic-hikvision", "worker-live-01"),
    Camera("cam-service-01", "Elevator Service", "Demo Tower", "generic-intelbras", "worker-live-01"),
    Camera("cam-lobby-01", "Lobby", "Demo Plaza", "generic-dahua", "worker-live-02"),
]


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
    <main style="font-family:system-ui;max-width:900px;margin:40px auto;line-height:1.5">
      <h1>Live Stream Gateway Demo</h1>
      <p>Vendor-neutral routing for live video clients.</p>
      <ul>
        <li><a href="/api/cameras">Cameras</a></li>
        <li><a href="/api/cameras/cam-social-01/stream">Hikvision-style descriptor</a></li>
        <li><a href="/api/cameras/cam-service-01/stream">Intelbras-style descriptor</a></li>
        <li><a href="/api/demo/cam-lobby-01/snapshot.svg">Synthetic snapshot</a></li>
      </ul>
    </main>
    """


@app.get("/api/cameras")
def list_cameras() -> list[dict]:
    return [camera.__dict__ for camera in CAMERAS]


@app.get("/api/cameras/{camera_id}/stream")
def stream_descriptor(camera_id: str) -> dict:
    camera = _camera(camera_id)
    provider = PROVIDERS.get(camera.vendor)
    if provider is None:
        raise HTTPException(status_code=422, detail="No provider for camera vendor")
    return provider.descriptor(camera)


@app.get("/api/demo/{camera_id}/snapshot.svg")
def synthetic_snapshot(camera_id: str) -> Response:
    camera = _camera(camera_id)
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540">
      <rect width="960" height="540" fill="#101828"/>
      <rect x="70" y="60" width="820" height="420" rx="10" fill="#1d2939" stroke="#98a2b3"/>
      <text x="90" y="115" font-family="Arial" font-size="32" fill="#f9fafb">{camera.name}</text>
      <text x="90" y="160" font-family="Arial" font-size="22" fill="#d0d5dd">{camera.site} / {camera.vendor}</text>
      <circle cx="720" cy="250" r="70" fill="#12b76a" opacity="0.25"/>
      <text x="658" y="260" font-family="Arial" font-size="22" fill="#d1fadf">LIVE DEMO</text>
    </svg>
    """
    return Response(content=svg.strip(), media_type="image/svg+xml")


@app.get("/api/system/health")
def health() -> dict:
    return {
        "service": "live-stream-gateway-demo",
        "state": "HEALTHY",
        "providers": sorted(PROVIDERS.keys()),
        "cameras_total": len(CAMERAS),
    }


def _camera(camera_id: str) -> Camera:
    for camera in CAMERAS:
        if camera.id == camera_id:
            return camera
    raise HTTPException(status_code=404, detail="Camera not found")

