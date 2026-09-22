"""Minimal tests against a stub HTTP server (stdlib)."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import pytest

from whaleshell import Client, ConnectUnsupported, Sandbox


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A003,D401
        return

    def do_GET(self):  # noqa: N802
        if self.path == "/healthz":
            self._json({"ok": True})
            return
        if self.path == "/v1/sandboxes":
            self._json({"sandboxes": [{"name": "demo", "status": "running"}]})
            return
        if self.path == "/v1/sandboxes/demo":
            self._json({"name": "demo", "status": "running"})
            return
        self.send_error(404)

    def do_PUT(self):  # noqa: N802
        if self.path.startswith("/v1/sandboxes/"):
            self.send_response(204)
            self.end_headers()
            return
        self.send_error(404)

    def do_DELETE(self):  # noqa: N802
        if self.path.startswith("/v1/sandboxes/"):
            self.send_response(204)
            self.end_headers()
            return
        self.send_error(404)

    def do_POST(self):  # noqa: N802
        if self.path == "/v1/relay/demo/exec":
            self._json({"exit_code": 0, "output": "hi\n"})
            return
        self.send_error(404)

    def _json(self, obj):
        body = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


@pytest.fixture()
def gateway_url():
    srv = HTTPServer(("127.0.0.1", 0), _Handler)
    t = Thread(target=srv.serve_forever, daemon=True)
    t.start()
    host, port = srv.server_address
    yield "http://%s:%s" % (host, port)
    srv.shutdown()


def test_crud_and_exec(gateway_url):
    with Client(gateway_url) as c:
        assert c.healthz()["ok"] is True
        c.create(Sandbox(name="demo", status="running"))
        assert len(c.list()) == 1
        assert c.get("demo").name == "demo"
        res = c.exec("demo", "echo", "hi")
        assert res.exit_code == 0 and res.output == "hi\n"
        with pytest.raises(ConnectUnsupported):
            c.connect("demo")
        c.delete("demo")
