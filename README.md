# 他山数字分身助手 (Tashan Profile Helper)

「他山数字分身系统」的科研数字分身采集助手。通过结构化对话，帮助科研人员建立、完善并维护多维度科研数字分身。

## 功能概览

- **基础信息采集**：研究阶段、学科领域、方法范式、技术能力、科研流程能力
- **量表施测**：学术动机（AMS-GSR 28）、认知风格（RCSS）、大五人格（Mini-IPIP）
- **快速推断**：在不想填量表时，根据已有信息做维度估算
- **画像审核与更新**：查看、修改、补充画像内容

## 使用方式

### Cursor 中使用

在 [Cursor](https://cursor.com) 中打开本仓库，由 Agent 根据规则（`.cursor/rules/profile-collector.mdc`）与技能（`.cursor/skills/`）进行对话式采集。

### Web 版（本地运行）

无需 Cursor，可在浏览器中通过智谱、Kimi、Qwen、DeepSeek 等大模型 API 使用。详见 [web/README.md](web/README.md)。

```bash
# 1. 配置 .env（在 web/backend 下创建 .env，填入 API Key）
cd web/backend && cp .env.example .env  # 编辑 .env

# 2. 一键启动前后端（在 web 目录下执行）
cd web && ./start.sh
# 后端 http://localhost:8000，前端 http://localhost:5173
```

可用话术示例：

| 意图     | 示例说法                           |
|----------|------------------------------------|
| 建立分身 | 「帮我建立分身」「新建档案」       |
| 填量表   | 「我想填量表」「用标准量表测量」   |
| 快速估算 | 「帮我推断」「不想填量表」         |
| 查看画像 | 「查看画像」「给我看结果」         |
| 修改信息 | 「修改」「更新」「补充」           |

## 项目结构

```
tashan-profile-helper/
├── .cursor/
│   ├── rules/          # 画像采集助手规则（始终生效）
│   └── skills/         # 各环节技能（采集、施测、推断、审核、更新等）
├── doc/                 # 量表题目与画像说明文档
├── profiles/            # 画像存储目录
│   └── _template.md     # 画像模板（唯一纳入版本控制的画像文件）
├── web/                 # Web 版（React + FastAPI）
│   ├── backend/        # 后端 API、Agent、工具
│   └── frontend/       # 前端界面
└── README.md
```

**隐私说明**：`profiles/` 下除 `_template.md` 外的个人画像文件、`web/backend/.env`（API Key）已通过 `.gitignore` 排除，不会提交到仓库。

## 画像维度

1. 基础身份（阶段、领域、范式、机构、学术网络）
2. 能力（技术栈 + 科研流程六环节）
3. 当前需求（时间占用、难点、近期想改变的事）
4. 认知风格（RCSS：横向整合 vs 垂直深度）
5. 学术动机（AMS-GSR 28：内在/外在/无动机）
6. 人格（Mini-IPIP 大五）
7. 综合解读（由 AI 根据以上维度生成建议）

详见 `doc/tashan-profile-outline.md`。


## Web 化改造参考

如果你希望把当前 Cursor 版助手改造成网站应用，可参考：`doc/web-version-guide.md`。

## 许可与致谢

本仓库为「他山数字分身系统」的本地采集与维护工具，支持 Cursor 与 Web 两种使用方式。
