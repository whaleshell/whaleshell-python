"""HTTP client for osg-gateway (create/list/get/delete/exec)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import httpx


class ConnectUnsupported(RuntimeError):
    """Interactive connect stays on the CLI (`osg connect <name>`)."""


@dataclass
class Sandbox:
    name: str
    status: str = ""
    container_id: str = ""
    network: str = ""
    labels: Optional[Dict[str, str]] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Sandbox":
        return cls(
            name=str(d.get("name") or ""),
            status=str(d.get("status") or ""),
            container_id=str(d.get("container_id") or d.get("containerId") or ""),
            network=str(d.get("network") or ""),
            labels=d.get("labels") if isinstance(d.get("labels"), dict) else None,
        )


@dataclass
class ExecResult:
    exit_code: int
    output: str


class Client:
    """Wraps osg-gateway HTTP + relay exec."""

    def __init__(self, base_url: str, timeout: float = 70.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(base_url=self.base_url, timeout=timeout)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def healthz(self) -> Dict[str, Any]:
        r = self._http.get("/healthz")
        r.raise_for_status()
        return r.json()

    def info(self) -> Dict[str, Any]:
        r = self._http.get("/v1/info")
        r.raise_for_status()
        return r.json()

    def create(self, sb: Sandbox) -> None:
        if not sb.name:
            raise ValueError("sandbox name required")
        body: Dict[str, Any] = {"name": sb.name, "status": sb.status or "running"}
        if sb.container_id:
            body["container_id"] = sb.container_id
        if sb.network:
            body["network"] = sb.network
        if sb.labels:
            body["labels"] = sb.labels
        r = self._http.put(f"/v1/sandboxes/{sb.name}", json=body)
        if r.status_code >= 300:
            raise httpx.HTTPStatusError(
                f"upsert sandbox: {r.status_code} {r.text}",
                request=r.request,
                response=r,
            )

    def list(self) -> List[Sandbox]:
        r = self._http.get("/v1/sandboxes")
        r.raise_for_status()
        data = r.json()
        items = data.get("sandboxes") if isinstance(data, dict) else data
        if not isinstance(items, list):
            return []
        return [Sandbox.from_dict(x) for x in items if isinstance(x, dict)]

    def get(self, name: str) -> Sandbox:
        r = self._http.get(f"/v1/sandboxes/{name}")
        r.raise_for_status()
        return Sandbox.from_dict(r.json())

    def delete(self, name: str) -> None:
        r = self._http.delete(f"/v1/sandboxes/{name}")
        if r.status_code >= 300 and r.status_code != 404:
            raise httpx.HTTPStatusError(
                f"delete sandbox: {r.status_code} {r.text}",
                request=r.request,
                response=r,
            )

    def exec(self, name: str, *argv: str) -> ExecResult:
        if not name or not argv:
            raise ValueError("usage: exec(name, *argv)")
        r = self._http.post(f"/v1/relay/{name}/exec", json={"argv": list(argv)})
        r.raise_for_status()
        data = r.json()
        return ExecResult(
            exit_code=int(data.get("exit_code", data.get("exitCode", -1))),
            output=str(data.get("output") or ""),
        )

    def connect(self, name: str) -> None:
        raise ConnectUnsupported(
            f"interactive connect is not supported; use: osg connect {name}"
        )
