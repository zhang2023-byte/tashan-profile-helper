"""内存会话管理：session_id → {messages, profile}"""
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE_PATH = REPO_ROOT / "profiles" / "_template.md"


def _load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")


_sessions: dict[str, dict] = {}


def get_or_create(session_id: str | None = None) -> tuple[str, dict]:
    """获取或创建会话。返回 (session_id, session_data)。"""
    if session_id and session_id in _sessions:
        s = _sessions[session_id]
        if "forum_profile" not in s:
            s["forum_profile"] = ""
        return session_id, s
    sid = session_id or str(uuid.uuid4())
    _sessions[sid] = {
        "messages": [],
        "profile": _load_template(),
        "forum_profile": "",
    }
    return sid, _sessions[sid]


def get(session_id: str) -> dict | None:
    """获取会话，不存在则返回 None"""
    return _sessions.get(session_id)


def reset(session_id: str) -> dict:
    """重置会话，清空消息并恢复模板画像。返回新 session 数据。"""
    _sessions[session_id] = {
        "messages": [],
        "profile": _load_template(),
        "forum_profile": "",
    }
    return _sessions[session_id]
