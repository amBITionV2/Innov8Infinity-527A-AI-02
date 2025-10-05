<div align="center">

# 🏭 FlowAI Coral Factory

### AI Agent Workflow Backend & Orchestration Engine

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5-4285F4?style=flat-square&logo=google)](https://ai.google.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-Enabled-FF6B6B?style=flat-square)](https://litellm.ai/)

**Production-ready backend for building and deploying multi-agent AI workflows**

</div>

---

## 📋 Overview

The **Coral Factory** is a FastAPI-based backend system that powers FlowAI's multi-agent orchestration engine. It handles workflow creation, agent execution, tool integration, and real-time tracing.

---

## ✨ Features

### 🤖 **Multi-Agent Orchestration**
- Sequential (Chain) execution
- Parallel (Group Chat) execution
- Managed coordination
- Single agent workflows

### 🔧 **Real Tool Integrations**
- ✅ Gmail (send emails via Google API)
- ✅ Google Calendar (create events)
- ✅ Twitter/X (post tweets via Tweepy)
- 🎭 Simulation mode for unsupported tools

### 🧠 **AI-Powered Agents**
- Google Gemini 2.5 Flash/Pro via LiteLLM
- Custom agent implementation
- Tool command parsing
- Intelligent prompt engineering

### 📊 **Execution Tracing**
- Real-time trace logging to Firebase
- Agent performance monitoring
- Tool call tracking
- Error detection and reporting

### 🔐 **Security**
- Bearer token authentication
- Firebase Admin SDK
- Environment-based configuration
- Secure API endpoints

---

## 🛠️ Technology Stack

### Core
- **Framework**: FastAPI (async Python web framework)
- **AI Engine**: Google Gemini via LiteLLM
- **Database**: Firebase Firestore
- **Containerization**: Docker

### Key Libraries
```txt
fastapi==0.100+              # Web framework
uvicorn==0.23+               # ASGI server
pydantic==2.0+               # Data validation
litellm==1.0+                # LLM abstraction layer
firebase-admin==6.0+         # Firebase SDK
google-api-python-client     # Gmail & Calendar
tweepy==4.0+                 # Twitter API
python-dotenv                # Environment management
```

---

## 🚀 Getting Started

### Prerequisites

```bash
✅ Python 3.8+
✅ pip or pipenv
✅ Firebase project with service account
✅ Google Gemini API key
✅ (Optional) Google OAuth credentials for Gmail/Calendar
✅ (Optional) Twitter API keys for X integration
```

### Installation

#### 1️⃣ Create Virtual Environment

```bash
cd coral_factory
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

#### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3️⃣ Environment Configuration

Create `.env` file:

```env
# Authentication
FACTORY_BEARER_TOKEN=bearer-token-2024

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
ARCADE_API_KEY=your_arcade_api_key_here  # Optional

# Firebase Configuration
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_SERVICE_ACCOUNT_PATH=firebase-service-account.json

# Twitter/X API Keys (Optional)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

#### 4️⃣ Firebase Setup

1. Download service account JSON from Firebase Console
2. Save as `firebase-service-account.json` in `coral_factory/`
3. Enable Firestore in your Firebase project

#### 5️⃣ Run the Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8001

# Or with auto-reload for development
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

🚀 API: http://localhost:8001

📖 Docs: http://localhost:8001/docs

---

## 📦 Project Structure

```
coral_factory/
├── app.py                        # FastAPI application & routes
├── factory/                      # Workflow engine
│   ├── builder.py                # Multi-agent orchestration
│   ├── simple_agent.py           # Agent implementation
│   ├── tools.py                  # Tool integrations (Gmail, Calendar, Twitter)
│   ├── tool_parser.py            # Tool command parsing
│   ├── trace_stream.py           # Firebase tracing processor
│   ├── agent_one.py              # Legacy agent (deprecated)
│   └── runner.py                 # Workflow runner
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container configuration
├── .env                          # Environment variables
├── credentials.json              # Google OAuth credentials
└── README.md                     # This file
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

Returns server health status (no auth required).

### Run Workflow

```http
POST /run/workflow/local
Authorization: Bearer bearer-token-2024
Content-Type: application/json

{
  "workflow_config": {
    "objective": "Analyze stock and notify user",
    "relations_type": "manager",
    "model_name": "gemini-2.5-flash",
    "api_key": "GEMINI_API_KEY",
    "agents": [...]
  },
  "user_id": "user_123",
  "user_task": "Analyze Tesla stock"
}
```

### Get Workflow Status

```http
GET /workflow/status/{trace_id}
Authorization: Bearer bearer-token-2024
```

### Get Workflow Result

```http
GET /workflow/result/{trace_id}
Authorization: Bearer bearer-token-2024
```

### Get Available Tools

```http
GET /auth/tools
Authorization: Bearer bearer-token-2024
```

---

## 🤖 Agent System

### Agent Types

#### SimpleLiteLLMAgent

Custom agent implementation using LiteLLM for direct Gemini API calls.

```python
agent = SimpleLiteLLMAgent(
    name="StockAnalyzer",
    model="gemini/gemini-2.5-flash",
    instructions=system_prompt,
    api_key=gemini_api_key,
    temperature=0.7,
    tracer=tracer,
    user_id=user_id,
    enable_tools=True
)

result = await agent.run("Analyze Tesla stock")
```

**Features:**
- Direct LiteLLM integration
- Firebase tracing
- Tool command parsing
- Conversation history
- Error handling

### Workflow Orchestration

#### Manager Pattern

```python
# Sequential execution with context passing
for agent_name, agent in agents.items():
    result = await agent.run(current_task)
    current_task = f"Previous: {result}\nOriginal: {user_task}"
```

#### Chain Pattern

```python
# Sequential with output piping
current_output = user_task
for agent_name, agent in agents.items():
    current_output = await agent.run(current_output)
```

#### Group Chat Pattern

```python
# Parallel execution
results = []
for agent_name, agent in agents.items():
    result = await agent.run(user_task)
    results.append(result)
```

---

## 🔧 Tool Integration System

### Tool Executor

```python
from factory.tools import get_tool_executor

executor = get_tool_executor()

# Send email
executor.send_email(
    to="user@example.com",
    subject="Report",
    body="Here's your report..."
)

# Create calendar event
executor.create_calendar_event(
    summary="Meeting",
    description="Team sync",
    start_time="2025-10-26T10:00:00Z",
    end_time="2025-10-26T11:00:00Z"
)

# Post tweet
executor.post_tweet("Check out FlowAI! #AI #Automation")
```

### Tool Command Parsing

Agents can output structured commands:

```python
# Agent output
"""
Stock analysis complete.

SEND_EMAIL: to=user@example.com | subject=Stock Report | body=Analysis results...
"""

# Parser automatically detects and executes
parser = ToolCommandParser(executor)
modified_output, results = parser.parse_and_execute(agent_output)
```

### Supported Tools

| Tool | Status | API | Free Tier |
|------|--------|-----|-----------|
| Gmail | ✅ Working | Google API | Yes |
| Calendar | ✅ Working | Google API | Yes |
| Twitter | ✅ Working | Tweepy v2 | Limited |
| WhatsApp | 🎭 Simulated | Twilio | Sandbox only |
| Uber | 🎭 Simulated | N/A | N/A |
| Instagram | 🎭 Simulated | N/A | N/A |

---

## 📊 Tracing System

### Firebase Integration

```python
tracer = OpenAIAgentsTracingProcessor(
    db=firestore_client,
    user_id=user_id
)

# Traces saved automatically
await agent.run(task)  # Trace stored in Firestore
```

### Trace Structure

```python
{
    "trace_id": "uuid",
    "agent_name": "StockAnalyzer",
    "start_time": datetime,
    "end_time": datetime,
    "status": "completed",
    "input": "Analyze Tesla",
    "output": "Analysis results...",
    "user_id": "user_123"
}
```

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t flowai-backend:latest .
```

### Run Container

```bash
docker run -d \
  -p 8001:8001 \
  --name flowai-backend \
  -e GEMINI_API_KEY=your_key \
  -e FIREBASE_PROJECT_ID=your_project \
  -e FIREBASE_SERVICE_ACCOUNT_PATH=/secrets/firebase.json \
  -v $(pwd)/firebase-service-account.json:/secrets/firebase.json:ro \
  flowai-backend:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8001:8001"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - FIREBASE_PROJECT_ID=${FIREBASE_PROJECT_ID}
    volumes:
      - ./firebase-service-account.json:/secrets/firebase.json:ro
```

---

## 🔐 Security

### Authentication

All API endpoints (except `/health`) require bearer token:

```http
Authorization: Bearer bearer-token-2024
```

### Environment Variables

- Never commit `.env` or `credentials.json`
- Use environment-specific configurations
- Rotate API keys regularly
- Use Firebase service accounts in production

---

## 🧪 Testing

### Manual Testing

```bash
# Health check
curl http://localhost:8001/health

# Run workflow
curl -X POST http://localhost:8001/run/workflow/local \
  -H "Authorization: Bearer bearer-token-2024" \
  -H "Content-Type: application/json" \
  -d @test_workflow.json
```

### Test Workflow Configuration

```json
{
  "workflow_config": {
    "objective": "Test workflow",
    "relations_type": "single",
    "model_name": "gemini-2.5-flash",
    "api_key": "GEMINI_API_KEY",
    "agents": [{
      "name": "TestAgent",
      "mcp_servers": [],
      "toolkits": [],
      "persona": "helpful assistant",
      "output": "clear response",
      "guidelines": "be concise"
    }]
  },
  "user_id": "test_user",
  "user_task": "Say hello"
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Firebase Connection

```bash
# Verify service account
python -c "import firebase_admin; print('✅ Firebase SDK installed')"

# Check credentials
ls -la firebase-service-account.json
```

#### Gemini API Errors

```bash
# Test API key
python -c "import litellm; litellm.completion(model='gemini/gemini-2.5-flash', messages=[{'role': 'user', 'content': 'hi'}])"
```

#### Port Already in Use

```bash
# Kill process on port 8001
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8001 | xargs kill -9
```

---

## 📈 Performance

### Optimization Tips

1. **Use caching** for repeated AI calls
2. **Batch requests** when possible
3. **Set appropriate timeouts** (default: 60s)
4. **Monitor Firebase quota** usage
5. **Use connection pooling** for DB

### Scaling

- **Horizontal**: Deploy multiple instances behind load balancer
- **Vertical**: Increase container resources
- **Database**: Use Firebase with proper indexing
- **Caching**: Add Redis for frequently accessed data

---

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LiteLLM Docs](https://docs.litellm.ai/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Tweepy Documentation](https://docs.tweepy.org/)

---

## 🤝 Contributing

See [main README](../README.md#contributing) for contribution guidelines.

---

## 📄 License

MIT License - see [main README](../README.md) for details.

---

<div align="center">

**Built with ⚡ FastAPI and 🧠 Google Gemini**

[⬆ back to top](#-flowai-coral-factory)

</div>
