# Live Stream Gateway Demo

Public portfolio demo of a multi-vendor VMS live gateway.

The project models how a frontend or business system can request a camera stream without needing to know the vendor-specific runtime details behind it. The gateway resolves the camera, finds its binding, selects the provider, and returns a normalized stream descriptor.

## What This Demonstrates

- API gateway design with FastAPI
- provider abstraction for multiple camera/VMS vendors
- catalog-based routing
- health-first operational behavior
- clean public demo without vendor SDKs or private endpoints

## Run Locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/api/cameras`
- `http://127.0.0.1:8000/api/cameras/cam-social-01/stream`

## Design

Real production systems often need different stream paths for Hikvision, Intelbras, Dahua, RTSP bridges, MJPEG snapshots, and WebSocket viewers. This demo keeps the same architectural idea but replaces private vendor code with safe provider classes.

## Portfolio Note

No proprietary SDK, private camera URL, credential, video frame, or customer network detail is included.

