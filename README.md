<h1 align="center">osg (Python)</h1>

<p align="center">
  <strong>Python SDK for osg-gateway</strong><br>
  Create, list, and relay-exec sandboxes over HTTP.
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
  <a href="https://pypi.org/project/osg/"><img src="https://img.shields.io/badge/pip-osg-blue" alt="pip"></a>
</p>

<p align="center">
  <sub>Part of the <a href="https://github.com/zorneth">zorneth / osg</a> ecosystem</sub>
</p>

---

## Overview

HTTP client for **osg-gateway** (registry + relay exec). Interactive TTY stays on the CLI (`osg connect`).

---

## Installation

```bash
pip install osg
# or editable from the hub workspace:
pip install -e .
```

---

## Quick Start

```python
from osg import Client, Sandbox

with Client("http://127.0.0.1:7443") as c:
    c.create(Sandbox(name="demo", status="running"))
    print(c.list())
    print(c.exec("demo", "echo", "hi"))
```

---

## Related

| Resource | Link |
|----------|------|
| Organization | [https://github.com/zorneth](https://github.com/zorneth) |
| Go SDK | [zorneth/osg-sdk](https://github.com/zorneth/osg-sdk) |
| Gateway | [zorneth/osg-gateway](https://github.com/zorneth/osg-gateway) |

## License

MIT © zorneth
