# osg Python SDK

HTTP client for **osg-gateway** (registry + relay exec). Interactive TTY stays on the CLI (`osg connect`).

```bash
pip install -e sdk/python
```

```python
from osg import Client, Sandbox

with Client("http://127.0.0.1:7443") as c:
    c.create(Sandbox(name="demo", status="running"))
    print(c.list())
    print(c.exec("demo", "echo", "hi"))
```

See [docs/SDK.md](../../docs/SDK.md).
