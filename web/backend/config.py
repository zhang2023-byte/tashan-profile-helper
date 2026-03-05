"""配置：从 .env 或环境变量读取，支持多 AI 提供商"""
import os
from pathlib import Path

from dotenv import load_dotenv

# 加载 .env（优先从 web/backend 目录，其次项目根目录）
_env_paths = [
    Path(__file__).resolve().parent / ".env",
    Path(__file__).resolve().parent.parent.parent / ".env",
]
for p in _env_paths:
    if p.exists():
        load_dotenv(p)
        break
else:
    load_dotenv()  # 默认加载当前目录

# 当前使用的提供商：zhipuai | kimi | qwen | deepseek | minimax
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "zhipuai").lower()

# 各提供商 API Key（按需配置）
ZHIPUAI_API_KEY = os.environ.get("ZHIPUAI_API_KEY", "")
KIMI_API_KEY = os.environ.get("KIMI_API_KEY", "")
QWEN_API_KEY = os.environ.get("QWEN_API_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")

# 各提供商默认模型（可被 LLM_MODEL 覆盖）
DEFAULT_MODELS = {
    "zhipuai": "glm-4.7",
    "kimi": "moonshot-v1-8k",
    "qwen": "qwen-plus",
    "deepseek": "deepseek-chat",
    "minimax": "abab6.5s-chat",
}

LLM_MODEL = os.environ.get("LLM_MODEL", "") or DEFAULT_MODELS.get(LLM_PROVIDER, "glm-4.7")

# 各提供商 OpenAI 兼容 API 的 base_url（仅 OpenAI 兼容的提供商使用）
OPENAI_COMPAT_BASE_URLS = {
    "zhipuai": "https://open.bigmodel.cn/api/paas/v4",
    "kimi": "https://api.moonshot.cn/v1",
    "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "deepseek": "https://api.deepseek.com/v1",
}


def get_llm_config() -> tuple[str, str]:
    """返回 (api_key, model) 或 (api_key, base_url, model)。"""
    keys = {
        "zhipuai": ZHIPUAI_API_KEY,
        "kimi": KIMI_API_KEY,
        "qwen": QWEN_API_KEY,
        "deepseek": DEEPSEEK_API_KEY,
        "minimax": MINIMAX_API_KEY,
    }
    api_key = keys.get(LLM_PROVIDER, "")
    return api_key, LLM_MODEL


def get_api_key() -> str:
    """获取当前配置的 API Key"""
    key, _ = get_llm_config()
    return key
