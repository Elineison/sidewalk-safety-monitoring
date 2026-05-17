from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Camera:
    id: str
    name: str
    site: str
    vendor: str
    worker: str


class StreamProvider(Protocol):
    vendor: str

    def descriptor(self, camera: Camera) -> dict:
        ...


class HikvisionWsProvider:
    vendor = "generic-hikvision"

    def descriptor(self, camera: Camera) -> dict:
        return {
            "camera_id": camera.id,
            "provider": self.vendor,
            "transport": "websocket",
            "url": f"/ws/demo/{camera.id}",
            "worker": camera.worker,
        }


class IntelbrasMjpegProvider:
    vendor = "generic-intelbras"

    def descriptor(self, camera: Camera) -> dict:
        return {
            "camera_id": camera.id,
            "provider": self.vendor,
            "transport": "mjpeg",
            "url": f"/api/demo/{camera.id}/mjpeg",
            "worker": camera.worker,
        }


class DahuaSnapshotProvider:
    vendor = "generic-dahua"

    def descriptor(self, camera: Camera) -> dict:
        return {
            "camera_id": camera.id,
            "provider": self.vendor,
            "transport": "snapshot-polling",
            "url": f"/api/demo/{camera.id}/snapshot.svg",
            "worker": camera.worker,
        }


PROVIDERS: dict[str, StreamProvider] = {
    HikvisionWsProvider.vendor: HikvisionWsProvider(),
    IntelbrasMjpegProvider.vendor: IntelbrasMjpegProvider(),
    DahuaSnapshotProvider.vendor: DahuaSnapshotProvider(),
}

