"""whaleshell — Python SDK for the whaleshell gateway."""

from .client import Client, ConnectUnsupported, ExecResult, Sandbox

__all__ = ["Client", "ConnectUnsupported", "ExecResult", "Sandbox"]
