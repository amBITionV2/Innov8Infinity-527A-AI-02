<div align="center">

# 🌊 FlowAI

### Build AI Agent Workflows with Natural Language

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Design, deploy, and orchestrate multi-agent AI workflows effortlessly**

[✨ Features](#-features) • [🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🎯 Use Cases](#-use-cases) • [🤝 Contributing](#-contributing)

![FlowAI Architecture](https://github.com/user-attachments/assets/3932f79f-6293-43fe-8dc8-ee944fd698c6)

</div>

---

## 🎯 What is FlowAI?

FlowAI is a **natural language platform** for building, deploying, and managing **multi-agent AI workflows**. Design complex agent systems through conversation or visual interfaces—no code required.

### 🌟 Key Highlights

- 🧠 **AI-Powered Design** - Describe your workflow in natural language, AI builds it for you
- 🎨 **Visual Workflow Canvas** - Interactive node-based editor for designing agent relationships
- 🔗 **Real Tool Integrations** - Gmail, Google Calendar, Twitter/X with simulation mode for others
- 🚀 **Production Ready** - Docker containerization, Firebase backend, REST API
- 📊 **Real-Time Monitoring** - Live trace viewing and execution analytics
- 🎛️ **Dual Modes** - "Let AI Decide" for quick builds or "Detailed Setup" for full control

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 **Natural Language Interface**
- Describe workflows in plain English
- AI automatically designs agents
- Smart tool assignment
- Intelligent workflow orchestration

</td>
<td width="50%">

### 🎨 **Visual Workflow Builder**
- Drag-and-drop interface
- Interactive node-based design
- Real-time workflow updates
- Beautiful, intuitive UI

</td>
</tr>
<tr>
<td width="50%">

### 🔧 **Real Tool Integrations**
- ✅ Gmail (send emails)
- ✅ Google Calendar (create events)
- ✅ Twitter/X (post tweets)
- 🎭 Simulation mode for any other tool

</td>
<td width="50%">

### 📊 **Execution Monitoring**
- Real-time trace viewing
- Agent performance analytics
- Tool call tracking
- Error detection and logging

</td>
</tr>
<tr>
<td width="50%">

### 🏗️ **Production Architecture**
- Docker containerization
- Firebase persistence
- REST API endpoints
- Multi-agent orchestration

</td>
<td width="50%">

### 🎯 **Multi-Agent Patterns**
- **Single**: One agent workflow
- **Chain**: Sequential execution
- **Group Chat**: Parallel agents
- **Manager**: Coordinated orchestration

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

```bash
✅ Node.js 18+ and npm
✅ Python 3.8+
✅ Docker (optional)
✅ Firebase account
✅ Google Gemini API key
```

### 🎬 Get Started in 5 Minutes

#### 1️⃣ Clone the Repository

   ```bash
git clone https://github.com/amBITionV2/Innov8Infinity-527A-AI-02.git
cd Innov8Infinity-527A-AI-02
   ```

#### 2️⃣ Set Up Frontend

   ```bash
   cd frontend
   cp env_example .env.local

# Edit .env.local with your credentials:
# - Firebase configuration
# - Gemini API key

   npm install
   npm run dev
   ```

🌐 Frontend: http://localhost:3000

#### 3️⃣ Set Up Backend

   ```bash
   cd coral_factory
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
   source venv/bin/activate

pip install -r requirements.txt

# Edit .env with your credentials
   uvicorn app:app --host 0.0.0.0 --port 8001
   ```

🔧 Backend API: http://localhost:8001

#### 4️⃣ Create Your First Workflow

1. Open http://localhost:3000
2. Type: `"Analyze Tesla stock and email me the report"`
3. Click **Build** → **Run**
4. Check your email! 📧

---

## 📸 Screenshots

<details>
<summary>Click to expand screenshots</summary>

### Landing Page
![Landing Page](https://github.com/user-attachments/assets/f7a2cb72-6357-4a65-be92-c9f2eb8a6a0a)

### Workflow Design
![Workflow Canvas](https://github.com/user-attachments/assets/7b3fcc90-e8cc-4cf4-bd38-fc6b94bd48a1)


### AI Chat Interface
![Chat Interface](https://github.com/user-attachments/assets/3b8a50dc-f56d-42ef-a1eb-9780133c701a)


### Execution & Results
![Execution](https://github.com/user-attachments/assets/94b446c2-fca3-4373-84e6-f85e2202cbfc)


</details>

---

## 🏗️ Architecture

FlowAI follows a **microservices architecture** with clear separation of concerns:

```
┌─────────────────┐    REST API     ┌──────────────────────┐
│                 │ ───────────────> │                      │
│   Frontend      │                  │   Coral Factory      │
│   (Next.js)     │ <─────────────── │   (FastAPI)          │
│                 │   WebSocket      │                      │
└─────────────────┘                  └──────────────────────┘
         │                                        │
         │ Firebase Auth                          │ Agent
         │ & Firestore                           │ Execution
         ▼                                        ▼
┌─────────────────┐                  ┌──────────────────────┐
│                 │                  │  Multi-Agent Engine  │
│   Firebase      │ <───────────────── Tool Integrations   │
│   - Auth        │    Trace Data    │  - Gmail            │
│   - Firestore   │                  │  - Calendar         │
│   - Storage     │                  │  - Twitter/X        │
└─────────────────┘                  └──────────────────────┘
```

### Data Flow

1. **User Input** → Natural language workflow description
2. **AI Processing** → Gemini generates workflow configuration
3. **Workflow Building** → Agents created with tools and instructions
4. **Execution** → Multi-agent orchestration with real tool calls
5. **Monitoring** → Real-time traces saved to Firebase
6. **Results** → Output displayed to user with execution details

---

## 📦 Project Structure

```
flowai/
├── frontend/                      # Next.js Web Application
│   ├── src/
│   │   ├── app/                  # Next.js App Router pages
│   │   │   ├── api/              # API routes (chat, export, deploy)
│   │   │   ├── auth/             # Authentication pages
│   │   │   ├── projects/         # Project management
│   │   │   └── settings/         # User settings
│   │   ├── components/           # React components
│   │   │   ├── chat/             # Chat interface components
│   │   │   ├── workflow/         # Workflow canvas components
│   │   │   └── ui/               # Reusable UI components
│   │   ├── contexts/             # React contexts (Auth)
│   │   ├── lib/                  # Utilities (Firebase, system prompts)
│   │   └── types/                # TypeScript definitions
│   └── public/                   # Static assets
│
├── coral_factory/                # AI Agent Workflow Backend
│   ├── app.py                    # FastAPI server with auth
│   ├── factory/                  # Workflow creation engine
│   │   ├── builder.py            # Multi-agent orchestration
│   │   ├── simple_agent.py       # Agent implementation
│   │   ├── tools.py              # Tool integrations (Gmail, etc.)
│   │   ├── tool_parser.py        # Tool command parsing
│   │   └── trace_stream.py       # Firebase tracing
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Container configuration
│   └── .env                      # Environment variables
│
├── HACKATHON_DEMO_GUIDE.md       # Demo strategy and scripts
└── README.md                     # This file
```

---

## 🎯 Use Cases

### 🏢 Business Automation

```
"Monitor support emails, categorize by urgency, 
and route to the appropriate team"
```

### 📊 Data Analysis

```
"Analyze top 5 tech stocks daily, generate report, 
and post insights on Twitter"
```

### 📅 Personal Assistant

```
"Check my calendar, summarize today's meetings, 
and email me the summary"
```

### 🚀 Social Media Management

```
"Research AI trends, create engaging content, 
and schedule posts across platforms"
```

---

## 🔧 Technology Stack

### Frontend
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript 5.0
- **Styling**: Tailwind CSS v3
- **UI Components**: shadcn/ui (Radix UI)
- **State Management**: React Context API
- **AI SDK**: Vercel AI SDK with Google provider
- **Workflow Visualization**: React Flow
- **Authentication**: Firebase Auth
- **Database**: Firebase Firestore

### Backend
- **Framework**: FastAPI (Python)
- **AI Models**: Google Gemini 2.5 (via LiteLLM)
- **Agent Engine**: Custom multi-agent orchestration
- **Tool Integrations**: Gmail, Google Calendar, Tweepy (Twitter)
- **Database**: Firebase Firestore
- **Containerization**: Docker
- **Authentication**: Bearer token

---

## 🚢 Deployment

### Frontend (Vercel)

```bash
cd frontend
npm run build

# Deploy to Vercel
vercel --prod
```

### Backend (Docker)

```bash
cd coral_factory

# Build image
docker build -t flowai-backend:latest .

# Run container
docker run -p 8001:8001 \
  -e GEMINI_API_KEY=your_key \
  -e FIREBASE_PROJECT_ID=your_project \
  flowai-backend:latest
```

### Environment Variables

**Frontend (`.env.local`):**
```env
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
GEMINI_API_KEY=
FACTORY_URL=http://localhost:8001
```

**Backend (`.env`):**
```env
GEMINI_API_KEY=
FIREBASE_PROJECT_ID=
FIREBASE_SERVICE_ACCOUNT_PATH=
TWITTER_API_KEY=
TWITTER_API_SECRET=
```

---

## 📖 Documentation

- [Frontend README](./frontend/README.md) - Web application setup
- [Backend README](./coral_factory/README.md) - Backend system details
- [Hackathon Demo Guide](./HACKATHON_DEMO_GUIDE.md) - Demo strategy and scripts

---

## 🎓 Key Concepts

### Workflow Modes

- **Let AI Decide**: AI auto-builds workflow from description (fast, smart defaults)
- **Detailed Setup**: Step-by-step guidance for precise control

### Agent Relations Types

- **Single**: One agent handles the entire task
- **Chain**: Agents execute sequentially, passing output to next agent
- **Group Chat**: Agents work in parallel on the same task
- **Manager**: Coordinated agents with task delegation

### Tool Simulation

For tools not yet integrated (WhatsApp, Uber, Instagram):
- Agent simulates realistic execution
- Shows expected output format
- Demonstrates workflow logic
- Easy to replace with real API calls

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow TypeScript/Python best practices
- Write clear, descriptive commit messages
- Update documentation for new features
- Test both frontend and backend integration
- Ensure no linter errors

---

## 🐛 Troubleshooting

<details>
<summary>Common Issues & Solutions</summary>

### Frontend won't start
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run dev
```

### Backend quota errors (429)
- Check Gemini API key quota
- Get new API key from different Google account
- Wait for daily quota reset (midnight UTC)

### Firebase connection issues
- Verify `firebase-service-account.json` exists
- Check Firebase project ID matches
- Ensure Firestore is enabled in Firebase console

### Tool integrations not working
- Verify API credentials in `.env`
- Check `credentials.json` for Google APIs
- Run OAuth flow: `python -c "from factory.tools import get_tool_executor; get_tool_executor()"`

</details>

---

## 📊 Project Stats

- **3** Real tool integrations (Gmail, Calendar, Twitter)
- **4** Workflow orchestration patterns
- **2** User modes (AI-driven, step-by-step)
- **250+** Gemini API calls per day (free tier)
- **Production-ready** architecture

---

## 🌟 Highlights

✨ **Natural Language First** - No code required
🎨 **Beautiful UI** - Modern, responsive design
🚀 **Production Ready** - Docker, Firebase, REST API
🔧 **Extensible** - Easy to add new tools and agents
📊 **Observable** - Real-time execution monitoring
🤖 **AI-Powered** - Gemini 2.5 intelligence

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) for the amazing React framework
- [FastAPI](https://fastapi.tiangolo.com/) for the blazing-fast Python backend
- [Google Gemini](https://ai.google.dev/) for powerful AI capabilities
- [Firebase](https://firebase.google.com/) for seamless backend services
- [shadcn/ui](https://ui.shadcn.com/) for beautiful UI components
- [React Flow](https://reactflow.dev/) for workflow visualization

---

<div align="center">

### 💬 Questions or Issues?

Open an [issue](https://github.com/amBITionV2/Innov8Infinity-527A-AI-02/issues) or reach out to the team!

**Built with ❤️ in BIT**

[![GitHub stars](https://img.shields.io/github/stars/amBITionV2/Innov8Infinity-527A-AI-02?style=social)](https://github.com/amBITionV2/Innov8Infinity-527A-AI-02)
[![GitHub repo](https://img.shields.io/badge/GitHub-Innov8Infinity--527A--AI--02-181717?style=social&logo=github)](https://github.com/amBITionV2/Innov8Infinity-527A-AI-02)

</div>
