<div align="center">

# 🎨 FlowAI Frontend

### Modern Web Interface for AI Agent Workflows

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)](https://reactjs.org/)

**Beautiful, responsive UI for building and managing AI agent workflows**

</div>

---

## 📋 Overview

The FlowAI frontend is a **Next.js 15** web application that provides an intuitive interface for designing, deploying, and monitoring multi-agent AI workflows. Built with modern React patterns, TypeScript, and Tailwind CSS.

---

## ✨ Features

### 🎨 **Beautiful UI/UX**
- Modern, responsive design system
- Dark/Light theme support
- Smooth animations and transitions
- Mobile-friendly interface

### 🤖 **AI-Powered Chat**
- Natural language workflow creation
- Real-time AI responses via Gemini
- Streaming text display
- Tool call visualization

### 🎨 **Visual Workflow Canvas**
- Interactive node-based editor
- Drag-and-drop agent design
- Real-time workflow updates
- Beautiful visualizations with React Flow

### 📊 **Execution Monitoring**
- Live trace viewing panel
- Agent performance tracking
- Tool call inspection
- Error detection and logging

### 🔐 **Authentication**
- Firebase Authentication
- Google Sign-In
- Secure session management
- User profile management

### 🎛️ **Dual Workflow Modes**
- **Let AI Decide**: Quick, smart workflow generation
- **Detailed Setup**: Step-by-step guided workflow creation

---

## 🛠️ Technology Stack

### Core
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript 5.0
- **Styling**: Tailwind CSS v3.4
- **UI Components**: shadcn/ui (Radix UI primitives)

### Key Libraries
```json
{
  "ai": "^5.0.60",              // Vercel AI SDK
  "@ai-sdk/google": "^2.0.17",  // Google Gemini integration
  "react-flow-renderer": "^11", // Workflow visualization
  "firebase": "^10.0.0",        // Auth & Database
  "react-markdown": "^9.0",     // Markdown rendering
  "framer-motion": "^11",       // Animations
  "lucide-react": "^0.400",     // Icons
  "sonner": "^1.0",             // Toast notifications
  "zod": "^3.25"                // Schema validation
}
```

---

## 🚀 Getting Started

### Prerequisites

```bash
Node.js 18+ and npm (or bun)
Firebase project with Auth & Firestore enabled
Google Gemini API key
```

### Installation

#### 1️⃣ Install Dependencies

```bash
cd frontend
npm install

# Or with bun
bun install
```

#### 2️⃣ Environment Setup

   ```bash
   cp env_example .env.local
   ```

Edit `.env.local`:

```env
   # Firebase Client Configuration
   NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
   NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
   NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Coral Factory Backend
FACTORY_URL=http://localhost:8001
FACTORY_TOKEN=bearer-token-2024
```

#### 3️⃣ Run Development Server

   ```bash
   npm run dev

# Or with bun
   bun dev
   ```

🌐 Open: http://localhost:3000

---

## 📦 Available Scripts

```bash
npm run dev      # Start development server (with Turbopack)
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

---

## 🏗️ Project Structure

```
src/
├── app/                          # Next.js App Router
│   ├── api/                      # API Routes
│   │   ├── chat/route.ts         # AI chat endpoint
│   │   ├── deploy/route.ts       # Workflow execution
│   │   └── export/route.ts       # Workflow export
│   ├── auth/page.tsx             # Authentication page
│   ├── projects/                 # Project pages
│   │   ├── page.tsx              # Projects list
│   │   └── [id]/page.tsx         # Individual project
│   ├── settings/page.tsx         # User settings
│   ├── privacy/page.tsx          # Privacy policy
│   ├── terms/page.tsx            # Terms of service
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Landing page
│   └── globals.css               # Global styles
│
├── components/                   # React Components
│   ├── chat/                     # Chat Interface
│   │   ├── ChatPane.tsx          # Main chat container
│   │   ├── Composer.tsx          # Message input
│   │   ├── Message.tsx           # Message display
│   │   ├── ToolRenderer.tsx      # Tool call visualization
│   │   ├── TracesPanel.tsx       # Execution traces
│   │   └── WorkflowModeSelector.tsx # Mode toggle
│   ├── workflow/                 # Workflow Canvas
│   │   ├── workflow-canvas.tsx   # Main canvas
│   │   ├── agent-node.tsx        # Agent node component
│   │   ├── tool-node.tsx         # Tool node component
│   │   └── start-end-node.tsx    # Start/End nodes
│   ├── ui/                       # Reusable UI Components
│   │   ├── button.tsx            # Button component
│   │   ├── input.tsx             # Input component
│   │   ├── dialog.tsx            # Dialog component
│   │   └── ...                   # Other shadcn/ui components
│   ├── navigation.tsx            # Top navigation
│   ├── Footer.tsx                # Footer component
│   ├── landing-hero.tsx          # Landing page hero
│   └── animated-coral.tsx        # Animated background
│
├── contexts/                     # React Contexts
│   └── AuthContext.tsx           # Authentication & user state
│
├── hooks/                        # Custom React Hooks
│   └── use-auto-resize-textarea.ts
│
├── lib/                          # Utilities & Configuration
│   ├── firebase.ts               # Firebase initialization
│   ├── system-prompt.ts          # AI system prompts
│   ├── workflow-parser.ts        # Workflow parsing logic
│   └── utils.ts                  # Helper functions
│
└── types/                        # TypeScript Definitions
    ├── chat.ts                   # Chat-related types
    ├── workflow.ts               # Workflow types
    ├── traces.ts                 # Trace types
    └── ui.ts                     # UI component types
```

---

## 🎨 Key Components

### Chat Interface

```typescript
// Main chat component with AI integration
<ChatInterface 
  projectId={projectId}
  initialMessages={messages}
  projectName={projectName}
/>
```

**Features:**
- Streaming AI responses
- Tool call visualization
- Message history
- Auto-scroll to latest
- Markdown rendering

### Workflow Canvas

```typescript
// Interactive workflow designer
<WorkflowCanvas 
  nodes={nodes}
  edges={edges}
  onNodesChange={handleNodesChange}
  onEdgesChange={handleEdgesChange}
/>
```

**Features:**
- Drag-and-drop nodes
- Visual agent connections
- Real-time updates
- Export workflow configuration

### Mode Selector

```typescript
// Toggle between AI and manual modes
<WorkflowModeSelector 
  mode={workflowMode}
  onModeChange={setWorkflowMode}
/>
```

**Modes:**
- **Let AI Decide**: Auto-build with smart defaults
- **Detailed Setup**: Step-by-step guided creation

---

## 🔌 API Integration

### Chat API

```typescript
// src/app/api/chat/route.ts
POST /api/chat
{
  "messages": [...],
  "projectId": "abc123",
  "userId": "user_xyz",
  "workflowMode": "ai" | "detailed"
}
```

### Export API

```typescript
// src/app/api/export/route.ts
POST /api/export
{
  "workflow_config": {...},
  "user_id": "user_xyz",
  "project_id": "abc123"
}
```

### Deploy API

```typescript
// src/app/api/deploy/route.ts
POST /api/deploy
{
  "query": "analyze stock...",
  "userId": "user_xyz",
  "projectId": "abc123"
}
```

---

## 🎨 Styling & Theming

### Theme Configuration

```typescript
// tailwind.config.ts
{
  theme: {
    extend: {
      colors: {
        primary: {...},
        secondary: {...},
        accent: {...}
      }
    }
  }
}
```

### Dark Mode Support

```typescript
// Automatic theme detection
<ThemeProvider
  attribute="class"
  defaultTheme="system"
  enableSystem
>
  {children}
</ThemeProvider>
```

---

## 🔒 Authentication Flow

1. **Sign In** → Firebase Auth (Google OAuth)
2. **Session Management** → Firebase SDK
3. **User Context** → React Context API
4. **Protected Routes** → useAuth hook

```typescript
// Example protected component
const { user } = useAuth();
if (!user) router.push('/auth');
```

---

## 📊 State Management

### Firebase Integration

```typescript
// Real-time project updates
const unsubscribe = onSnapshot(projectRef, (doc) => {
  setProject(doc.data());
});
```

### Context Structure

```typescript
interface AuthContextType {
  user: User | null;
  getUserProjects: () => Promise<Project[]>;
  createProject: () => Promise<string>;
  updateProjectWorkflow: () => Promise<void>;
  // ... more methods
}
```

---

## 🚀 Performance Optimization

### Next.js Features

- **Turbopack**: Fast development builds
- **App Router**: Optimized routing
- **Server Components**: Reduced client bundle
- **Streaming**: Incremental page loading

### React Optimization

- **Code Splitting**: Dynamic imports
- **Memoization**: useMemo, useCallback
- **Virtualization**: Large lists (React Flow)
- **Suspense**: Loading states

---

## 🧪 Development Tips

### Hot Reload

```bash
# Changes auto-reload in dev mode
npm run dev
```

### Add New Component

```bash
# Add shadcn/ui component
npx shadcn@latest add button
npx shadcn@latest add dialog
```

### Debug API Calls

```typescript
// Enable logging in API routes
console.log('API Route - Request:', request);
console.log('API Route - Response:', response);
```

---

## 🐛 Troubleshooting

### Common Issues

#### Frontend won't start
```bash
rm -rf node_modules .next
npm install
npm run dev
```

#### Firebase errors
- Check API keys in `.env.local`
- Verify Firebase project settings
- Ensure Firestore is enabled

#### Styling issues
```bash
# Rebuild Tailwind
npm run dev
# Or force rebuild
rm -rf .next
```

#### Type errors
```bash
# Check TypeScript
npx tsc --noEmit
```

---

## 🎯 Best Practices

### Component Structure
- Keep components small and focused
- Use TypeScript for type safety
- Extract reusable logic to hooks
- Follow React best practices

### Styling
- Use Tailwind utility classes
- Create reusable component variants
- Maintain consistent spacing
- Follow design system

### Performance
- Minimize re-renders
- Use React.memo for expensive components
- Implement proper loading states
- Optimize images and assets

---

## 📱 Responsive Design

### Breakpoints

```typescript
// Tailwind breakpoints
sm: 640px   // Mobile landscape
md: 768px   // Tablet
lg: 1024px  // Desktop
xl: 1280px  // Large desktop
```

### Mobile Optimization

- Touch-friendly UI elements
- Responsive navigation
- Optimized images
- Fast page loads

---

## 🚢 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Environment Variables

Add in Vercel dashboard:
- `NEXT_PUBLIC_FIREBASE_*`
- `GEMINI_API_KEY`
- `FACTORY_URL`
- `FACTORY_TOKEN`

### Build Configuration

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install"
}
```

---

## 📖 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [React Flow Docs](https://reactflow.dev/)
- [Firebase Web SDK](https://firebase.google.com/docs/web/setup)

---

## 🤝 Contributing

See [main README](../README.md#contributing) for contribution guidelines.

---

<div align="center">

**Built with ❤️ using Next.js and TypeScript**

[⬆ back to top](#-flowai-frontend)

</div>
