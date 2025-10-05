"""
Simple tool integrations for Gmail, Google Calendar, and X (Twitter)
These are called directly by the agent via command parsing
"""

import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Executes tool commands for agents"""
    
    def __init__(self):
        self.gmail_service = None
        self.calendar_service = None
        self.twitter_client = None
        self._initialized = False
    
    def initialize(self):
        """Initialize API clients (called once at startup)"""
        if self._initialized:
            return
        
        try:
            # Initialize Gmail and Calendar
            self._init_google_services()
            # Initialize Twitter
            self._init_twitter()
            self._initialized = True
            logger.info("✅ Tool executor initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Tool initialization failed: {e}")
            logger.warning("Tools will return simulated responses")
    
    def _init_google_services(self):
        """Initialize Gmail and Calendar APIs"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            import pickle
            
            SCOPES = [
                'https://www.googleapis.com/auth/gmail.send',
                'https://www.googleapis.com/auth/calendar'
            ]
            
            creds = None
            token_path = 'token.pickle'
            
            # Load existing token
            if os.path.exists(token_path):
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
            
            # Refresh or get new token
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # DON'T run OAuth in background thread - it will block!
                    # Instead, just skip and simulate
                    logger.warning("⚠️ OAuth needed but not running interactively")
                    logger.warning("Run this command separately to authorize:")
                    logger.warning("  python -c 'from factory.tools import get_tool_executor; get_tool_executor()'")
                    return
            
            # Build services
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            self.calendar_service = build('calendar', 'v3', credentials=creds)
            logger.info("✅ Google services initialized")
            
        except ImportError as e:
            logger.warning(f"Google API libraries not installed: {e}")
        except Exception as e:
            logger.warning(f"Failed to initialize Google services: {e}")
    
    def _init_twitter(self):
        """Initialize Twitter API v2"""
        try:
            import tweepy
            
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_secret = os.getenv('TWITTER_ACCESS_SECRET')
            
            if all([api_key, api_secret, access_token, access_secret]):
                # Use API v2 for free tier
                self.twitter_client = tweepy.Client(
                    consumer_key=api_key,
                    consumer_secret=api_secret,
                    access_token=access_token,
                    access_token_secret=access_secret
                )
                logger.info("✅ Twitter API v2 initialized")
            else:
                logger.warning("Twitter API keys not configured")
                
        except ImportError:
            logger.warning("Tweepy not installed")
        except Exception as e:
            logger.warning(f"Failed to initialize Twitter: {e}")
    
    # ==================== GMAIL ====================
    
    def send_email(self, to: str, subject: str, body: str) -> str:
        """Send an email via Gmail"""
        try:
            if self.gmail_service:
                from email.mime.text import MIMEText
                import base64
                
                message = MIMEText(body)
                message['to'] = to
                message['subject'] = subject
                
                raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
                
                result = self.gmail_service.users().messages().send(
                    userId='me',
                    body={'raw': raw}
                ).execute()
                
                logger.info(f"✅ Email sent to {to}")
                return f"✅ Email sent successfully to {to} (ID: {result['id']})"
            else:
                # Simulated response
                logger.info(f"📧 [SIMULATED] Email to {to}: {subject}")
                return f"📧 [SIMULATED] Email sent to {to} with subject: {subject}"
                
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return f"❌ Failed to send email: {str(e)}"
    
    # ==================== GOOGLE CALENDAR ====================
    
    def create_calendar_event(
        self, 
        title: str, 
        date: str, 
        time: str = "10:00",
        duration_hours: int = 1
    ) -> str:
        """Create a Google Calendar event"""
        try:
            if self.calendar_service:
                # Parse date and time
                start_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                end_datetime = start_datetime + timedelta(hours=duration_hours)
                
                event = {
                    'summary': title,
                    'start': {
                        'dateTime': start_datetime.isoformat(),
                        'timeZone': 'America/New_York',
                    },
                    'end': {
                        'dateTime': end_datetime.isoformat(),
                        'timeZone': 'America/New_York',
                    },
                }
                
                result = self.calendar_service.events().insert(
                    calendarId='primary',
                    body=event
                ).execute()
                
                logger.info(f"✅ Calendar event created: {title}")
                return f"✅ Event created: {title} on {date} at {time} - {result.get('htmlLink')}"
            else:
                # Simulated response
                logger.info(f"📅 [SIMULATED] Event: {title} on {date} at {time}")
                return f"📅 [SIMULATED] Calendar event created: {title} on {date} at {time}"
                
        except Exception as e:
            logger.error(f"Failed to create calendar event: {e}")
            return f"❌ Failed to create event: {str(e)}"
    
    # ==================== TWITTER/X ====================
    
    def post_tweet(self, text: str) -> str:
        """Post a tweet to X (Twitter) using API v2"""
        try:
            if self.twitter_client:
                # Truncate if too long (280 char limit)
                if len(text) > 280:
                    text = text[:277] + "..."
                
                # Use create_tweet for API v2
                response = self.twitter_client.create_tweet(text=text)
                tweet_id = response.data['id']
                tweet_url = f"https://twitter.com/user/status/{tweet_id}"
                
                logger.info(f"✅ Tweet posted: {text[:50]}...")
                return f"✅ Tweet posted: {tweet_url}"
            else:
                # Simulated response
                logger.info(f"🐦 [SIMULATED] Tweet: {text[:50]}...")
                return f"🐦 [SIMULATED] Tweet posted: {text[:100]}"
                
        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            # Check if it's access level issue
            if "403" in str(e) or "access level" in str(e).lower():
                logger.warning("⚠️ Twitter Free tier detected - using simulation")
                logger.info(f"🐦 [SIMULATED] Tweet: {text[:50]}...")
                return f"🐦 [SIMULATED - Free Tier] Tweet: {text[:100]}"
            return f"❌ Failed to post tweet: {str(e)}"
    
    # ==================== TOOL DISPATCHER ====================
    
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> str:
        """Execute a tool by name with parameters"""
        try:
            tool_map = {
                'send_email': self.send_email,
                'create_calendar_event': self.create_calendar_event,
                'post_tweet': self.post_tweet,
            }
            
            if tool_name not in tool_map:
                return f"❌ Unknown tool: {tool_name}"
            
            func = tool_map[tool_name]
            result = func(**params)
            return result
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return f"❌ Tool execution failed: {str(e)}"


# Global instance
_tool_executor = None

def get_tool_executor() -> ToolExecutor:
    """Get or create the global tool executor instance"""
    global _tool_executor
    if _tool_executor is None:
        _tool_executor = ToolExecutor()
        _tool_executor.initialize()
    return _tool_executor

