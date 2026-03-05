"""FastAPI 入口：POST /chat（SSE 流式）、GET /download、CORS"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agent import run_agent
from sessions import get_or_create, get, reset

app = FastAPI(title="他山画像 Web API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    content: str


@app.post("/chat", response_class=StreamingResponse)
async def chat_stream(req: ChatRequest):
    """流式对话：SSE 返回"""
    session_id, session = get_or_create(req.session_id)
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")

    def generate():
        import json
        try:
            for chunk in run_agent(req.message, session, stream=True):
                yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-Id": session_id,
        },
    )


@app.post("/chat/sync")
async def chat_sync(req: ChatRequest) -> ChatResponse:
    """非流式对话：一次性返回完整回复（用于调试或简单场景）"""
    session_id, session = get_or_create(req.session_id)
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")

    result = ""
    for chunk in run_agent(req.message, session, stream=False):
        result = chunk
    return ChatResponse(session_id=session_id, content=result)


@app.get("/profile/{session_id}")
async def get_profile(session_id: str):
    """获取当前会话的发展画像和论坛画像内容"""
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在或已过期")
    return {
        "profile": session["profile"],
        "forum_profile": session.get("forum_profile", ""),
    }


@app.get("/download/{session_id}")
async def download_profile(session_id: str):
    """下载发展画像 .md 文件"""
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在或已过期")

    from fastapi.responses import Response

    return Response(
        content=session["profile"].encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="profile.md"',
        },
    )


@app.get("/download/{session_id}/forum")
async def download_forum_profile(session_id: str):
    """下载论坛画像 .md 文件"""
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在或已过期")

    from fastapi.responses import Response

    content = session.get("forum_profile", "")
    if not content:
        raise HTTPException(status_code=404, detail="尚未生成论坛画像")

    return Response(
        content=content.encode("utf-8"),
        media_type="text/markdown; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="forum-profile.md"',
        },
    )


@app.post("/session/reset/{session_id}")
async def session_reset(session_id: str):
    """重置会话：清空消息，恢复空白画像"""
    session = get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    reset(session_id)
    return {"ok": True, "session_id": session_id}


@app.get("/session")
async def session_get(session_id: str | None = None):
    """获取或创建会话，返回 session_id"""
    sid, _ = get_or_create(session_id)
    return {"session_id": sid}
