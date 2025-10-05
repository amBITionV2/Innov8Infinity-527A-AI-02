# 🚀 Quick Start - Tool Integrations

## ✅ Setup Complete!

All your API keys and credentials are configured!

---

## 🔄 **RESTART BACKEND NOW**

```powershell
# Stop current backend (Ctrl+C if running)
# Then start fresh:
.\start-backend.ps1
```

**Why?** Backend needs to load new Twitter keys from `.env`

---

## 🧪 **Test Your Tools**

### Test 1: Run Your Stock Workflow

1. Click **BUILD**
2. Click **RUN**
3. Enter: `"Create a stock analysis for Google and share it"`

### Expected Results:

```
StockAnalyzer:
✅ Stock analysis completed

SocialMediaPoster:
✅ Tweet posted: https://twitter.com/...  ← REAL TWEET!

CalendarManager:
📅 [Browser opens for OAuth]
→ Sign in with Gmail
→ Click "Allow"
✅ Event created: https://calendar.google.com/...

Notifier:
📧 [Browser opens if not authorized yet]
→ Sign in with Gmail
→ Click "Allow"
✅ Email sent successfully!
```

---

## 📝 **OAuth Flow (First Time Only)**

### For Gmail & Calendar:

1. Agent tries to send email or create event
2. **Browser opens automatically**
3. **Sign in** with your Gmail account
4. **Click "Allow"** to grant permissions
5. **Token saved** in `token.pickle`
6. ✅ **Never needed again!**

### For Twitter:

✅ **No OAuth needed!**
- Keys in `.env` file
- Works immediately

---

## 🔍 **Check Logs**

### Backend logs will show:

```
✅ Tool executor initialized successfully
✅ Twitter API initialized
🔧 Parsing output for tool commands...
🐦 Detected TWEET command: Google stock update...
✅ Tweet posted: https://twitter.com/...
✅ Executed 1 tools
```

---

## 📱 **Verify on Platforms**

After running:

1. **Check Twitter:** https://twitter.com/
   - You should see your tweet posted!

2. **Check Gmail:** Sent folder
   - You should see the email!

3. **Check Calendar:** https://calendar.google.com/
   - You should see the event!

---

## ⚠️ **Troubleshooting**

### "Twitter shows [SIMULATED]"
→ Restart backend to load new keys

### "Browser doesn't open for OAuth"
→ Check backend is running in terminal (not as service)

### "OAuth denied"
→ Make sure you're signing in with the right Google account

### "Token expired"
→ Delete `token.pickle` and re-authorize

---

## 🎯 **Tool Commands Format**

Your agents know these formats:

### Email:
```
SEND_EMAIL: to=user@example.com | subject=Your Subject | body=Your message here
```

### Calendar:
```
CREATE_EVENT: title=Meeting Name | date=2025-10-10 | time=14:00
```

### Tweet:
```
POST_TWEET: text=Your tweet content (max 280 chars)
```

---

## ✨ **Tips**

1. **OAuth token is saved** - You only authorize once
2. **Twitter works immediately** - No browser needed
3. **Check backend logs** - See exactly what's happening
4. **Real vs Simulated** - Look for ✅ vs 📧 [SIMULATED]

---

## 🆘 **Need Help?**

Full guide: `TOOLS_SETUP_GUIDE.md`

---

**🎉 Everything is ready! Restart backend and test!**

