"""会话管理：内存会话 + profiles 目录自动落盘。"""
import uuid
from datetime import date
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROFILES_DIR = REPO_ROOT / "profiles"
TEMPLATE_PATH = REPO_ROOT / "profiles" / "_template.md"
PROFILE_TITLE_PREFIX = "# 科研人员画像 — "
PLACEHOLDER_IDENTIFIERS = {"[姓名/标识]", "姓名/标识"}


def _load_template() -> str:
    today_str = date.today().strftime("%Y-%m-%d")
    return TEMPLATE_PATH.read_text(encoding="utf-8").replace("YYYY-MM-DD", today_str)


def _today_unnamed() -> str:
    return f"unnamed-{date.today().strftime('%Y-%m-%d')}"


def _sanitize_identifier(identifier: str) -> str:
    cleaned = identifier.strip()
    if cleaned in PLACEHOLDER_IDENTIFIERS or not cleaned:
        return _today_unnamed()
    cleaned = re.sub(r'[\\/:*?"<>|]+', "-", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned or _today_unnamed()


def _extract_profile_identifier(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(PROFILE_TITLE_PREFIX):
            return _sanitize_identifier(stripped[len(PROFILE_TITLE_PREFIX) :])
        if stripped.startswith("# "):
            return _sanitize_identifier(stripped[2:])
        break
    return _today_unnamed()


def _normalize_existing_path(path_value: str | None) -> Path | None:
    if not path_value:
        return None
    return Path(path_value)


def _session_suffix(session: dict) -> str:
    """会话唯一后缀，用于防止同名画像冲突。"""
    sid = session.get("session_id") or ""
    if sid:
        return sid.replace("-", "")[:8]
    return uuid.uuid4().hex[:8]


def _target_profile_path(content: str, session: dict) -> Path:
    identifier = _extract_profile_identifier(content)
    suffix = _session_suffix(session)
    return PROFILES_DIR / f"{identifier}-{suffix}.md"


def _relocate_file_if_needed(current_path: Path | None, target_path: Path) -> None:
    if not current_path or current_path == target_path or not current_path.exists():
        return
    if target_path.exists():
        current_path.unlink()
        return
    current_path.rename(target_path)


def save_profile(session: dict, content: str) -> Path:
    """将画像写入内存，并同步保存到 profiles 目录。"""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    target_path = _target_profile_path(content, session)
    current_path = _normalize_existing_path(session.get("profile_path"))
    _relocate_file_if_needed(current_path, target_path)
    target_path.write_text(content, encoding="utf-8")
    session["profile"] = content
    session["profile_path"] = str(target_path)
    forum_content = session.get("forum_profile", "")
    if forum_content:
        forum_target_path = _target_forum_profile_path(session)
        forum_current_path = _normalize_existing_path(session.get("forum_profile_path"))
        _relocate_file_if_needed(forum_current_path, forum_target_path)
        forum_target_path.write_text(forum_content, encoding="utf-8")
        session["forum_profile_path"] = str(forum_target_path)
    return target_path


def _target_forum_profile_path(session: dict) -> Path:
    profile_path = _normalize_existing_path(session.get("profile_path"))
    if not profile_path:
        profile_path = _target_profile_path(session.get("profile", ""), session)
    return profile_path.with_name(f"{profile_path.stem}-论坛画像.md")


def save_forum_profile(session: dict, content: str) -> Path:
    """将论坛分身写入内存，并与画像同目录保存。"""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    profile_content = session.get("profile", "")
    if profile_content:
        save_profile(session, profile_content)
    target_path = _target_forum_profile_path(session)
    current_path = _normalize_existing_path(session.get("forum_profile_path"))
    _relocate_file_if_needed(current_path, target_path)
    target_path.write_text(content, encoding="utf-8")
    session["forum_profile"] = content
    session["forum_profile_path"] = str(target_path)
    return target_path


_sessions: dict[str, dict] = {}


def get_or_create(session_id: str | None = None) -> tuple[str, dict]:
    """获取或创建会话。返回 (session_id, session_data)。"""
    if session_id and session_id in _sessions:
        s = _sessions[session_id]
        s["session_id"] = session_id
        if "forum_profile" not in s:
            s["forum_profile"] = ""
        if "profile_path" not in s:
            s["profile_path"] = None
        if "forum_profile_path" not in s:
            s["forum_profile_path"] = None
        return session_id, s
    sid = session_id or str(uuid.uuid4())
    _sessions[sid] = {
        "session_id": sid,
        "messages": [],
        "profile": _load_template(),
        "forum_profile": "",
        "profile_path": None,
        "forum_profile_path": None,
    }
    return sid, _sessions[sid]


def get(session_id: str) -> dict | None:
    """获取会话，不存在则返回 None"""
    return _sessions.get(session_id)


def reset(session_id: str) -> dict:
    """重置会话，清空消息并恢复模板画像。返回新 session 数据。"""
    _sessions[session_id] = {
        "session_id": session_id,
        "messages": [],
        "profile": _load_template(),
        "forum_profile": "",
        "profile_path": None,
        "forum_profile_path": None,
    }
    return _sessions[session_id]
