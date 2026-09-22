<h1 align="center">whaleshell (Python)</h1>

<p align="center">
  <strong>Python SDK for whaleshell-gateway</strong><br>
  Create, list, and relay-exec sandboxes over HTTP.
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
  <a href="https://pypi.org/project/whaleshell/"><img src="https://img.shields.io/badge/pip-whaleshell-blue" alt="pip"></a>
</p>

<p align="center">
  <sub>Part of the <a href="https://github.com/whaleshell">whaleshell</a> ecosystem</sub>
</p>

---

## Overview

HTTP client for **whaleshell-gateway** (registry + relay exec). Interactive TTY stays on the CLI (`whaleshell connect`).

---

## Installation

```bash
pip install whaleshell
# or editable from the hub workspace:
pip install -e .
```

---

## Quick Start

```python
from whaleshell import Client, Sandbox

with Client("http://127.0.0.1:7443") as c:
    c.create(Sandbox(name="demo", status="running"))
    print(c.list())
    print(c.exec("demo", "echo", "hi"))
```

---

## Related

| Resource | Link |
|----------|------|
| Organization | [https://github.com/whaleshell](https://github.com/whaleshell) |
| Go SDK | [whaleshell/whaleshell-sdk](https://github.com/whaleshell/whaleshell-sdk) |
| Gateway | [whaleshell/whaleshell-gateway](https://github.com/whaleshell/whaleshell-gateway) |

## License

MIT © whaleshell
