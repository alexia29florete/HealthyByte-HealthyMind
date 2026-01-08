import os
from typing import Any, Dict, Optional, Tuple
import requests

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

class ApiError(RuntimeError):
    pass

def _json(resp: requests.Response) -> Dict[str, Any]:
    try:
        return resp.json()
    except Exception:
        return {"raw": resp.text}

def signup(email: str, password: str, name: Optional[str] = None) -> Dict[str, Any]:
    resp = requests.post(
        f"{BASE_URL}/signup",
        json={"email": email, "password": password, "name": name or ""},
        timeout=30,
    )
    if resp.status_code not in (200, 201):
        raise ApiError(f"Signup failed ({resp.status_code}): {_json(resp)}")
    return _json(resp)

def login(email: str, password: str) -> str:
    resp = requests.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password},
        timeout=30,
    )
    data = _json(resp)
    if resp.status_code != 200:
        raise ApiError(f"Login failed ({resp.status_code}): {data}")
    token = data.get("access_token")
    if not token:
        raise ApiError("Login response missing access_token")
    return token

def login_or_signup(email: str, password: str) -> str:
    try:
        return login(email, password)
    except ApiError:
        # try auto-signup then login again
        signup(email, password, name=email.split("@")[0])
        return login(email, password)

def create_journal_entry(token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    resp = requests.post(
        f"{BASE_URL}/journal",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
        timeout=120,
    )
    data = _json(resp)
    if resp.status_code not in (200, 201):
        raise ApiError(f"Create journal failed ({resp.status_code}): {data}")
    return data

def get_stats_summary(token: str) -> Dict[str, Any]:
    resp = requests.get(
        f"{BASE_URL}/stats/summary",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    data = _json(resp)
    if resp.status_code != 200:
        raise ApiError(f"Stats failed ({resp.status_code}): {data}")
    return data
