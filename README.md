# Sidewalk Safety Monitoring

Public case study for camera-based sidewalk dwell-time monitoring.

This repository is a sanitized version of a sidewalk monitoring workflow: configured camera ROI, person tracks, dwell-time thresholds, cooldowns, runtime status, synthetic evidence, and operator events. It is designed for portfolio review without exposing any production camera, customer, or incident data.

## Operational Problem

Sidewalk monitoring is different from generic motion detection. The system needs to know whether a person remains in a relevant outdoor ROI for too long, whether the camera is still providing fresh frames, and whether alerts are being created with enough context for an operator to act.

## What This Demonstrates

- FastAPI module for sidewalk camera analytics.
- ROI-based person-track runtime with elapsed time and confidence.
- Dwell-time event creation with cooldown logic.
- Camera health snapshot based on last frame age.
- Synthetic SVG snapshot for README screenshots and demos.

## Architecture

```text
camera frame -> person detection -> ROI track -> dwell-time rule -> operator event
                              -> runtime snapshot -> health endpoint
```

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8013
```

Open:

- `http://127.0.0.1:8013/`
- `http://127.0.0.1:8013/api/sidewalk/cameras`
- `http://127.0.0.1:8013/api/demo/sidewalk-camera/snapshot.svg`

Create a synthetic event:

```bash
curl -X POST http://127.0.0.1:8013/api/demo/sidewalk-dwell
curl http://127.0.0.1:8013/api/sidewalk/events
```

## Public-Safe Scope

All camera names, sites, detections, tracks, and events are synthetic. The repository does not include production recordings, private IPs, DVR credentials, customer identifiers, SDK files, or alert destinations.

## Skills Represented

Python, FastAPI, video analytics domain modeling, OpenCV/YOLO-oriented architecture, runtime health checks, operator event design, and security-operations thinking.
