"""LLM 客户端抽象：支持 ZhipuAI、Kimi、Qwen、DeepSeek 等 OpenAI 兼容 API"""
from openai import OpenAI

from config import LLM_PROVIDER, get_api_key, LLM_MODEL, OPENAI_COMPAT_BASE_URLS


def create_client() -> OpenAI | None:
    """根据 LLM_PROVIDER 创建对应的 OpenAI 兼容客户端"""
    api_key = get_api_key()
    if not api_key:
        return None

    base_url = OPENAI_COMPAT_BASE_URLS.get(LLM_PROVIDER)
    if not base_url:
        # MiniMax 等非标准接口暂不支持，可在此扩展
        return None

    return OpenAI(api_key=api_key, base_url=base_url)


def get_model() -> str:
    return LLM_MODEL
