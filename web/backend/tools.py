"""工具实现：read_skill, read_doc, read_profile, write_profile"""
from pathlib import Path

# 仓库根目录：web/backend/ 的上级的上级
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

SKILL_NAMES = [
    "collect-basic-info",
    "administer-ams",
    "administer-rcss",
    "administer-mini-ipip",
    "infer-profile-dimensions",
    "review-profile",
    "update-profile",
    "generate-forum-profile",
    "generate-ai-memory-prompt",
    "import-ai-memory",
    "modify-profile-schema",
]

DOC_NAMES = [
    "academic-motivation-scale",
    "mini-ipip-scale",
    "researcher-cognitive-style",
    "tashan-profile-outline",
    "tashan-profile-examples",
    "multidimensional-work-motivation-scale",
    "implementation-guide",
]


def read_skill(skill_name: str) -> str:
    """读取指定 Skill 文件内容"""
    if skill_name not in SKILL_NAMES:
        return f"错误：未知的 skill 名称 '{skill_name}'。可用：{', '.join(SKILL_NAMES)}"
    path = REPO_ROOT / ".cursor" / "skills" / skill_name / "SKILL.md"
    if not path.exists():
        return f"错误：文件不存在 {path}"
    return path.read_text(encoding="utf-8")


def read_doc(doc_name: str) -> str:
    """读取 doc 目录下的参考文档"""
    if doc_name not in DOC_NAMES:
        return f"错误：未知的 doc 名称 '{doc_name}'。可用：{', '.join(DOC_NAMES)}"
    path = REPO_ROOT / "doc" / f"{doc_name}.md"
    if not path.exists():
        return f"错误：文件不存在 {path}"
    return path.read_text(encoding="utf-8")


# read_profile 和 write_profile 由 agent.py 直接操作 session.profile 实现
