# 🧠 Lang2Creator: MCP 기반 유튜브 트렌드 AI Agent

Lang2Creator는 FastAPI 기반 MCP Server와 Flask 기반 유튜브 트렌드 Agent로 구성된 멀티채널 처리 플랫폼입니다.  
추가로 Streamlit 기반 UI 또는 외부 클라이언트를 붙여 사용할 수 있습니다.

---

## 📁 구성

| 폴더 | 설명 |
|------|------|
| `mcp_server/` | 사용자 발화 수신 → OpenAI → 라우팅 (FastAPI) |
| `youtube_agent/` | 유튜브 썸네일/조회수 분석 기능 제공 (Flask) |

---

## 🚀 실행 방법

### 1️⃣ MCP Server 실행 (FastAPI)

```bash
cd mcp_server
cp .env.example .env  # OPENAI_API_KEY 입력
pip install -r requirements.txt
uvicorn main:app --reload
```

→ 서버는 `http://localhost:8000/ask` 에서 사용자 발화를 수신합니다.

---

### 2️⃣ YouTube Agent 실행 (Flask)

```bash
cd youtube_agent
cp .env.example .env  # YOUTUBE_API_KEY 입력
pip install -r requirements.txt
python agent.py
```

→ 서버는 `http://localhost:5001/youtube` 에서 요청을 수신합니다.

---

## 🧪 테스트 예시

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"user": "jinsoo", "text": "Creator_001의 썸네일 보여줘"}'
```

---

## 🖥️ Streamlit 연동하기 (선택)

Streamlit UI는 별도로 개발하여 MCP Server 또는 YouTube Agent를 호출하는 클라이언트 역할을 할 수 있습니다.

예시:
```bash
streamlit run streamlit_ui.py
```

> 또는 기존 프로젝트를 streamlit화 하려면 agent.py 기능을 그대로 옮겨 UI로 표현하면 됩니다.

---

## 📌 환경 파일 예시

### `.env` (in `mcp_server/`)
```
OPENAI_API_KEY=sk-xxxxx
```

### `.env` (in `youtube_agent/`)
```
YOUTUBE_API_KEY=AIzaSyxxxxx
```

---

## ✨ 향후 확장

- [ ] Redis 기반 세션 관리
- [ ] LangChain 기반 멀티 Agent Router
- [ ] Streamlit Cloud / Render.com 배포
- [ ] Discord / Voice 채널 통합

---

Made with ❤️ by jsshin2022
