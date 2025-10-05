"""
Parser to extract tool commands from agent responses
Handles structured output from agents and executes tools
"""

import re
import logging
from typing import Dict, Any, Optional, Tuple, List

logger = logging.getLogger(__name__)


class ToolCommandParser:
    """Parses agent output for tool commands and executes them"""
    
    # Command patterns
    EMAIL_PATTERN = r'SEND_EMAIL:\s*to=([^|]+)\|\s*subject=([^|]+)\|\s*body=(.+?)(?=\n[A-Z_]+:|$)'
    CALENDAR_PATTERN = r'CREATE_EVENT:\s*title=([^|]+)\|\s*date=([^|]+)\|\s*time=([^|]+)'
    TWEET_PATTERN = r'POST_TWEET:\s*text=(.+?)(?=\n[A-Z_]+:|$)'
    
    def __init__(self, tool_executor):
        self.tool_executor = tool_executor
    
    def parse_and_execute(self, agent_output: str) -> Tuple[str, List[str]]:
        """
        Parse agent output, execute any tools, and return modified output
        
        Returns:
            (modified_output, tool_results) - Output with tool results, and list of results
        """
        tool_results = []
        modified_output = agent_output
        
        # Check for email commands
        email_matches = re.finditer(self.EMAIL_PATTERN, agent_output, re.DOTALL)
        for match in email_matches:
            to = match.group(1).strip()
            subject = match.group(2).strip()
            body = match.group(3).strip()
            
            logger.info(f"📧 Detected EMAIL command: to={to}")
            result = self.tool_executor.send_email(to, subject, body)
            tool_results.append(result)
            
            # Replace command with result in output
            modified_output = modified_output.replace(match.group(0), result)
        
        # Check for calendar commands
        calendar_matches = re.finditer(self.CALENDAR_PATTERN, agent_output, re.DOTALL)
        for match in calendar_matches:
            title = match.group(1).strip()
            date = match.group(2).strip()
            time = match.group(3).strip()
            
            logger.info(f"📅 Detected CALENDAR command: {title}")
            result = self.tool_executor.create_calendar_event(title, date, time)
            tool_results.append(result)
            
            # Replace command with result
            modified_output = modified_output.replace(match.group(0), result)
        
        # Check for tweet commands
        tweet_matches = re.finditer(self.TWEET_PATTERN, agent_output, re.DOTALL)
        for match in tweet_matches:
            text = match.group(1).strip()
            
            logger.info(f"🐦 Detected TWEET command: {text[:50]}...")
            result = self.tool_executor.post_tweet(text)
            tool_results.append(result)
            
            # Replace command with result
            modified_output = modified_output.replace(match.group(0), result)
        
        # Log if no tools were detected
        if not tool_results:
            logger.debug("No tool commands detected in agent output")
        else:
            logger.info(f"✅ Executed {len(tool_results)} tools")
        
        return modified_output, tool_results
    
    def extract_structured_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured data from agent output
        Useful for parsing key-value pairs
        """
        data = {}
        
        # Pattern: key: value or key=value
        pattern = r'([a-zA-Z_]+)[:=]\s*([^\n]+)'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            key = match.group(1).strip().lower()
            value = match.group(2).strip()
            data[key] = value
        
        return data


def enhance_agent_prompt_with_tools(persona: str) -> str:
    """
    Add tool usage instructions to agent persona
    """
    tool_instructions = """

AVAILABLE TOOLS (use when needed):

1. EMAIL:
   Format: SEND_EMAIL: to=email@example.com | subject=Your Subject | body=Your message here

2. CALENDAR:
   Format: CREATE_EVENT: title=Event Name | date=2025-10-05 | time=14:00

3. TWITTER/X:
   Format: POST_TWEET: text=Your tweet content here (max 280 chars)

INSTRUCTIONS:
- Use these EXACT formats when you want to execute a tool
- After using a tool, continue with your response
- You can use multiple tools in one response
- The tool will execute and you'll see the result
"""
    
    return persona + tool_instructions

