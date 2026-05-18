from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Dict, List


@dataclass
class PersonTrack:
    track_id: str
    first_seen_at: float
    last_seen_at: float
    elapsed_s: float
    confidence: float
    bbox: List[float]
    event_sent: bool = False


@dataclass
class CameraRuntime:
    camera_id: str
    last_frame_at: float = field(default_factory=time)
    tracks: Dict[str, PersonTrack] = field(default_factory=dict)


class SidewalkSafetyMonitor:
    def __init__(self) -> None:
        self._cameras = [
            {
                'id': 'sidewalk-front-a01',
                'name': 'Câmera da calçada frontal',
                'site': 'Perímetro residencial A',
                'platform_family': 'dahua-intelbras',
                'threshold_s': 300.0,
                'cooldown_s': 90.0,
                'analysis_fps': 2.0,
                'roi': [
                    {'x': 0.24, 'y': 0.20},
                    {'x': 0.78, 'y': 0.20},
                    {'x': 0.86, 'y': 0.90},
                    {'x': 0.18, 'y': 0.90},
                ],
            },
            {
                'id': 'sidewalk-service-b02',
                'name': 'Câmera da calçada de serviço',
                'site': 'Perímetro residencial B',
                'platform_family': 'dahua-intelbras',
                'threshold_s': 420.0,
                'cooldown_s': 120.0,
                'analysis_fps': 2.0,
                'roi': [
                    {'x': 0.28, 'y': 0.18},
                    {'x': 0.72, 'y': 0.18},
                    {'x': 0.82, 'y': 0.92},
                    {'x': 0.20, 'y': 0.92},
                ],
            },
        ]
        self._runtimes = {camera['id']: CameraRuntime(camera_id=camera['id']) for camera in self._cameras}
        self._events: List[dict] = []
        self._last_event_at: Dict[str, float] = {}

    def camera_ids(self) -> set[str]:
        return {camera['id'] for camera in self._cameras}

    def cameras(self) -> list[dict]:
        return [{**camera, 'runtime': self.runtime(camera['id'])} for camera in self._cameras]

    def runtime(self, camera_id: str) -> dict:
        runtime = self._runtimes[camera_id]
        now = time()
        return {
            'camera_id': camera_id,
            'state': 'RUNNING',
            'last_frame_age_s': round(now - runtime.last_frame_at, 3),
            'tracks': [self._track_payload(track) for track in runtime.tracks.values()],
        }

    def ingest_detection(self, camera_id: str, track_id: str, confidence: float, bbox: list[float], elapsed_s: float) -> dict:
        runtime = self._runtimes[camera_id]
        camera = self._camera(camera_id)
        now = time()
        runtime.last_frame_at = now
        track = runtime.tracks.get(track_id)
        if track is None:
            track = PersonTrack(
                track_id=track_id,
                first_seen_at=now - elapsed_s,
                last_seen_at=now,
                elapsed_s=elapsed_s,
                confidence=confidence,
                bbox=bbox,
            )
            runtime.tracks[track_id] = track
        else:
            track.last_seen_at = now
            track.elapsed_s = max(track.elapsed_s, elapsed_s)
            track.confidence = confidence
            track.bbox = bbox
        event = self._maybe_create_event(camera, track)
        return {'track': self._track_payload(track), 'event': event}

    def events(self) -> list[dict]:
        return list(self._events)

    def health(self) -> dict:
        snapshots = [self.runtime(camera['id']) for camera in self._cameras]
        stale = [item['camera_id'] for item in snapshots if item['last_frame_age_s'] > 45]
        return {
            'service': 'sidewalk-safety-monitoring',
            'state': 'HEALTHY' if not stale else 'DEGRADED',
            'cameras_total': len(self._cameras),
            'cameras_running': len(self._cameras) - len(stale),
            'open_events': len([event for event in self._events if event['status'] == 'open']),
            'issues': [{'camera_id': camera_id, 'reason': 'no_recent_frames'} for camera_id in stale],
        }

    def _maybe_create_event(self, camera: dict, track: PersonTrack) -> dict | None:
        now = time()
        last_event_at = self._last_event_at.get(camera['id'], 0.0)
        cooldown_ok = now - last_event_at >= float(camera['cooldown_s'])
        if track.event_sent or track.elapsed_s < float(camera['threshold_s']) or not cooldown_ok:
            return None
        track.event_sent = True
        self._last_event_at[camera['id']] = now
        event = {
            'id': f"evt-sidewalk-{len(self._events) + 1:04d}",
            'type': 'sidewalk_dwell_time',
            'severity': 'warning',
            'camera_id': camera['id'],
            'camera_name': camera['name'],
            'site': camera['site'],
            'track_id': track.track_id,
            'duration_s': round(track.elapsed_s, 1),
            'confidence': round(float(track.confidence), 3),
            'operator_note': 'Pessoa permaneceu na ROI da calçada acima do limite configurado.',
            'created_at': now,
            'status': 'open',
        }
        self._events.append(event)
        return event

    def _camera(self, camera_id: str) -> dict:
        for camera in self._cameras:
            if camera['id'] == camera_id:
                return camera
        raise KeyError(camera_id)

    @staticmethod
    def _track_payload(track: PersonTrack) -> dict:
        return {
            'track_id': track.track_id,
            'elapsed_s': round(float(track.elapsed_s), 1),
            'confidence': round(float(track.confidence), 3),
            'bbox': track.bbox,
            'event_sent': track.event_sent,
        }
