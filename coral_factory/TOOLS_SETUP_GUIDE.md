# 🛠️ Tool Integration Setup Guide

This guide will help you set up Gmail, Google Calendar, and X (Twitter) integrations for your AI agents.

## 📋 Overview

Your agents can now:
- ✅ Send real emails via Gmail
- ✅ Create real calendar events in Google Calendar
- ✅ Post real tweets to X (Twitter)

## 🚀 Quick Start

### Option 1: Full Setup (Real Tools)
Follow all steps below to enable real tool integrations.

### Option 2: Testing Mode (Simulated)
Skip setup - agents will simulate actions and log them. Great for testing!

---

## 📧 Gmail Setup

### Step 1: Enable Gmail API

1. Go to https://console.cloud.google.com/
2. Create a new project or select existing one
3. Click "Enable APIs and Services"
4. Search for "Gmail API" and enable it

### Step 2: Create OAuth Credentials

1. Go to "Credentials" in the left sidebar
2. Click "Create Credentials" → "OAuth client ID"
3. Configure consent screen if prompted:
   - User Type: External
   - App name: "FlowAI Agents"
   - User support email: your email
   - Developer contact: your email
4. Application type: **Desktop app**
5. Name: "FlowAI Gmail Client"
6. Click "Create"
7. **Download the JSON file**
8. Rename it to `credentials.json`
9. Place it in `coral_factory/` directory

### Step 3: First Run Authorization

The first time an agent tries to send an email:
1. A browser window will open
2. Sign in with your Gmail account
3. Click "Allow" to grant permissions
4. Token will be saved automatically

---

## 📅 Google Calendar Setup

### Step 1: Enable Calendar API

1. In the same Google Cloud Console project
2. Click "Enable APIs and Services"
3. Search for "Google Calendar API" and enable it

### Step 2: Use Same OAuth Credentials

✅ You can use the same `credentials.json` from Gmail setup!

The OAuth consent screen will ask for both Gmail and Calendar permissions.

---

## 🐦 X (Twitter) Setup

### Step 1: Create Twitter Developer Account

1. Go to https://developer.twitter.com/
2. Sign up for developer access
3. Wait for approval (usually instant to 24 hours)

### Step 2: Create an App

1. Go to Developer Portal → Projects & Apps
2. Click "Create App"
3. App name: "FlowAI Agent"
4. Get your keys:
   - API Key
   - API Secret Key
   - Access Token
   - Access Token Secret

### Step 3: Add Keys to Environment

Edit `coral_factory/.env` and add:

```env
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_secret_here
```

---

## 🔧 Installation

### 1. Install Python Dependencies

```bash
cd coral_factory
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import google.auth; import tweepy; print('✅ All libraries installed!')"
```

---

## 🧪 Testing

### Test 1: Check if Tools are Ready

```bash
cd coral_factory
.\venv\Scripts\Activate.ps1
python -c "from factory.tools import get_tool_executor; te = get_tool_executor(); print('✅ Tools initialized')"
```

### Test 2: Run Your Workflow

1. Start backend: `.\start-backend.ps1`
2. Start frontend: `cd frontend; npm run dev`
3. Create a workflow with agents that use tools
4. Click RUN!

Watch the backend logs for:
- `📧 Detected EMAIL command`
- `📅 Detected CALENDAR command`
- `🐦 Detected TWEET command`

---

## 📝 Agent Usage Examples

### Example 1: Email Agent

```
Agent Persona: "Email notification specialist"

Agent will output:
SEND_EMAIL: to=user@example.com | subject=Your Report | body=Here is your daily report...
```

### Example 2: Calendar Agent

```
Agent Persona: "Calendar scheduler"

Agent will output:
CREATE_EVENT: title=Team Meeting | date=2025-10-10 | time=14:00
```

### Example 3: Social Media Agent

```
Agent Persona: "Social media manager"

Agent will output:
POST_TWEET: text=Check out our latest update! #AI #Automation
```

---

## 🔍 Troubleshooting

### Issue: "credentials.json not found"
**Solution:** Place `credentials.json` in `coral_factory/` directory (same folder as `app.py`)

### Issue: "No module named 'google.auth'"
**Solution:** 
```bash
pip install --upgrade google-auth google-auth-oauthlib google-api-python-client
```

### Issue: "Twitter authentication failed"
**Solution:** 
- Check `.env` file has all 4 Twitter keys
- Make sure keys are correct (no extra spaces)
- Verify app has "Read and Write" permissions in Twitter Developer Portal

### Issue: "Tools return [SIMULATED]"
**Solution:** 
- This is normal if credentials aren't set up
- Agents will simulate actions
- Set up credentials for real integrations

### Issue: "Browser doesn't open for OAuth"
**Solution:**
- Run backend from command line (not as service)
- Check firewall isn't blocking localhost

---

## 📊 How It Works

### 1. Agent Output
Agent generates response with special commands:
```
Here's the analysis...

SEND_EMAIL: to=user@example.com | subject=Analysis | body=Results are ready
```

### 2. Parser Detection
Tool parser detects the `SEND_EMAIL:` command

### 3. Execution
Executes the actual Gmail API call

### 4. Result
Replaces command with result:
```
✅ Email sent successfully to user@example.com (ID: 18f2a3b...)
```

---

## 🎯 Tips

1. **Start with Simulated Mode**
   - Test workflow logic first
   - Set up real tools when ready

2. **OAuth Token Management**
   - `token.pickle` is created after first auth
   - Backup this file to avoid re-authorizing

3. **Twitter Rate Limits**
   - Free tier: Limited tweets per day
   - Monitor usage in Twitter Developer Portal

4. **Security**
   - Keep `credentials.json` and `.env` secure
   - Never commit them to Git
   - Already added to `.gitignore`

---

## 🆘 Need Help?

Check backend logs for detailed error messages:
```bash
# Backend will show:
✅ Tool executor initialized successfully
📧 Detected EMAIL command: to=user@example.com
✅ Email sent to user@example.com
```

---

## ✅ Success Checklist

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] Calendar API enabled
- [ ] `credentials.json` downloaded and placed
- [ ] Twitter Developer account approved
- [ ] Twitter app created
- [ ] Twitter keys added to `.env`
- [ ] Python dependencies installed
- [ ] First OAuth authorization completed
- [ ] `token.pickle` file exists
- [ ] Tools tested and working!

---

🎉 **You're all set!** Your AI agents can now interact with the real world!

