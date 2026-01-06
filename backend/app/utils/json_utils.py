import json
from typing import Any, Optional

def dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def loads(s: Optional[str], default: Any):
    if not s:
        return default
    try:
        return json.loads(s)
    except Exception:
        return default
