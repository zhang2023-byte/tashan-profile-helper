# 将 Tashan Profile Helper 包装成网站版本（实施指南）

本文面向当前仓库（以 Cursor + Agent 交互为核心）的改造场景，给出一条可落地的 Web 化路径。

## 1. 先明确「网站版」目标

建议先冻结一版 MVP（最小可用版本），避免一上来把量表、推断、导出、团队管理全部做完。

MVP 建议包含：

1. 用户登录（邮箱验证码或三方登录）。
2. 新建画像与查看画像列表。
3. 对话式采集基础信息（阶段、领域、方法、能力等）。
4. 至少 1 个量表在线施测（例如 Mini-IPIP）。
5. 自动生成画像摘要并可手动编辑。
6. 数据本地化存储（数据库）与基础隐私同意。

## 2. 总体架构建议

可采用经典三层：

- **前端**：Next.js（App Router）
- **后端 API**：Next.js Route Handlers 或独立 FastAPI/NestJS
- **数据层**：PostgreSQL + 对象存储（可选）

推荐起步方案（开发效率优先）：

- Next.js 全栈（前后端同仓）
- Prisma 管理数据库
- Redis（可选）做对话状态缓存
- OpenAI/兼容模型 API 负责结构化提问与总结

## 3. 从当前仓库迁移什么

本仓库的核心资产主要是：

- `doc/` 下的量表与画像维度设计
- `profiles/_template.md` 的画像结构
- Cursor 规则与技能里的对话流程（如果你后续把 `.cursor/` 一并纳入 Web 项目）

迁移原则：

1. **把“提示词流程”改成“后端工作流”**：由 API 控制每一步状态与可追踪日志。
2. **把“Markdown 文件画像”改成“结构化数据库画像”**：便于检索、统计和权限控制。
3. **把“单机本地文件”改成“用户隔离的数据域”**：每条数据都绑定 `user_id`。

## 4. 数据库模型（建议）

至少准备以下表：

- `users`：用户基础信息、登录方式
- `profiles`：一份用户画像主记录（版本号、状态）
- `profile_dimensions`：画像分维度内容（基础身份、能力、需求等）
- `assessments`：量表实例（类型、开始/提交时间、得分）
- `assessment_answers`：逐题作答记录
- `conversations`：对话会话
- `messages`：会话消息（用户、系统、助手）
- `consents`：隐私授权记录

关键设计点：

- `profiles` 使用 `version` 字段支持历史回溯。
- `messages` 留存 `tool_call` / `model` / `prompt_version`，方便审计。
- 量表答案和 AI 推断结果分表，避免混淆“测得”与“估算”。

## 5. 后端能力拆分

可以先做 4 个核心 API：

1. `POST /api/chat`：接收用户输入，返回下一轮提问与已更新的结构化字段。
2. `POST /api/assessments/:type/submit`：提交量表答案并计算分数。
3. `POST /api/profile/generate-summary`：生成综合解读（可重复生成）。
4. `GET /api/profile/:id`：读取完整画像（用于展示与编辑）。

建议把“提示词 + JSON 输出约束 + 字段映射”封装为独立 service，避免散落在路由里。

## 6. 前端页面最小集合

- `/login`：登录页
- `/dashboard`：画像列表
- `/profile/new`：新建采集流程
- `/profile/[id]`：画像详情（分维度编辑 + 重新生成总结）
- `/assessment/[type]`：量表填写页

交互上建议采用：

- 左侧步骤导航（基础信息 -> 量表 -> 总结）
- 右侧聊天/表单混合采集
- 顶部始终显示“数据仅用于画像分析”的隐私提示

## 7. 隐私与合规（必须尽早做）

至少做到：

1. 首次进入时收集明确同意（consent）。
2. 支持用户删除画像和会话数据。
3. 传输全程 HTTPS；敏感字段加密或脱敏。
4. 记录模型供应商与数据流向说明。
5. 后台日志避免落地可识别个人隐私文本。

## 8. 迭代路线图（4 周示例）

- **第 1 周**：产品原型 + 数据库设计 + 登录体系
- **第 2 周**：对话采集 + 画像字段写入 + 基础详情页
- **第 3 周**：接入 1~2 个量表 + 自动计分 + 总结生成
- **第 4 周**：隐私合规、压测、灰度上线

## 9. 技术栈推荐（快速落地版）

- 前端：Next.js + Tailwind + shadcn/ui
- 后端：Next.js API Routes/Route Handlers
- ORM：Prisma
- DB：PostgreSQL（Neon/Supabase/RDS）
- 鉴权：Clerk/Auth.js/Supabase Auth
- 部署：Vercel（前后端）+ 托管 PostgreSQL

## 10. 先做哪三件事

如果你现在就要开工，建议按顺序做：

1. 把 `profiles/_template.md` 拆解成数据库字段草案。
2. 写出 `/api/chat` 的 JSON 输入输出协议（先不连模型，返回 mock）。
3. 做一个可点击 Demo：登录 -> 新建画像 -> 聊天采集 -> 查看详情。

---

如果你希望，我可以下一步直接给你：

- 一份可运行的 Next.js 项目脚手架目录；
- Prisma schema 初稿；
- `/api/chat` 的请求/响应 JSON 协议与示例代码。
