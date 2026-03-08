# 他山数字分身 Web 版

## 本地运行

### 1. 配置 API Key（.env 文件）

在 `web/backend/` 目录下创建 `.env` 文件（可复制 `.env.example`）：

```bash
cd web/backend
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

`.env` 已加入 `.gitignore`，不会提交到仓库。

### 2. 一键启动前后端

在 `web/` 目录下执行：

```bash
./start.sh
```

脚本会安装后端与前端依赖，并同时启动后端（http://localhost:8000）和前端（http://localhost:5173）。浏览器访问 http://localhost:5173 即可使用。退出时按 Ctrl+C 会同时关闭前后端。

### 3. 分别启动（可选）

若需单独启动后端或前端：

**后端：**
```bash
cd web/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

若 8000 端口被占用，可改用 `--port 8001`，并修改 `web/frontend/vite.config.ts` 中的 proxy target。

**前端（新终端）：**
```bash
cd web/frontend
npm install
npm run dev
```

浏览器访问 http://localhost:5173

### 4. 使用流程

1. 在输入框输入「帮我建立分身」
2. 按提示逐步填写基础信息
3. 创建和更新过程中，画像会自动保存到仓库根目录的 `profiles/` 文件夹
4. 完成后点击「查看画像」→「下载画像」获取 profile.md 文件

## 环境变量（.env）

| 变量 | 说明 |
|:---|:---|
| LLM_PROVIDER | 当前使用的 AI 提供商：`zhipuai` \| `kimi` \| `qwen` \| `deepseek` \| `minimax`，默认 `zhipuai` |
| LLM_MODEL | 模型名称，不填则使用各提供商默认模型 |
| ZHIPUAI_API_KEY | 智谱 AI Key，[获取](https://open.bigmodel.cn/) |
| KIMI_API_KEY | Kimi / Moonshot Key |
| QWEN_API_KEY | 通义千问 / DashScope Key |
| DEEPSEEK_API_KEY | DeepSeek Key |
| MINIMAX_API_KEY | MiniMax Key（暂需单独适配） |
