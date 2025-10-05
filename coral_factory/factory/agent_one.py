import asyncio
import os
from pydantic import BaseModel  # type: ignore
from contextlib import AsyncExitStack
from typing import Any, Dict, List
import time

from agents import Agent, set_trace_processors # type: ignore
from agents.mcp import MCPServerStreamableHttp, MCPServerSse # type: ignore
from agents.model_settings import ModelSettings # type: ignore
# LiteLLM models are passed as strings directly, no need for LitellmModel wrapper
import os

from arcadepy import AsyncArcade # type: ignore
from agents_arcade import get_arcade_tools # type: ignore


default_timeout = 60
default_cache_tools_list = True


# TODO Add reasoning prompt to reasoning models!
REASONING_PROMPT = """
Reasoning:
- When thinking about your next step, consider each tool
- Plan ahead and think about the order of the tools to use
- Check the params required for each tool and their format
"""

BASE_PROMPT = """You are a {persona}. Use your tools to answer the users request. Format your final answer as desribed in "Expected output".
Think step by step and make sure to solve your issues. Always start by explaining how you achieved the answer.

Guidelines:
- Perform the task requested by the user and answer the user's question. Do not ask new questions to the user. Only explain what you have done to get to the answer.
{guidelines}

Expected output:
{output}

Context:
{context}
"""


class MCPConfig(BaseModel):
    name: str
    server_type: str
    params: Dict[str, Any] = {}
    timeout_seconds: int = 60
    cache_tools_list: bool = True

class AgentConfig(BaseModel):
    name: str
    mcp_servers: List[MCPConfig]
    toolkits: List[str]
    persona: str
    output: str
    guidelines: str
    context: Dict[str, Any] = {}


async def _build_mcp_servers(
    stack: AsyncExitStack,
    servers: List[Dict[str, Any]],
) -> List[Any]:
    servers: List[Any] = []
    for index, server_cfg in enumerate(servers, start=1):
        print("make config:", server_cfg)
        if not isinstance(server_cfg, dict):
            continue

        name = server_cfg.get("name") or f"MCP {index}"
        server_type = server_cfg.get("server_type") or f"HTTP"

        # Params need to include url
        if not server_cfg.get("params", {}).get("url"):
            if not server_cfg.get("url"):
                raise Exception("URL is required")
            server_cfg["params"]["url"] = server_cfg["url"]
            continue

        timeout = int(server_cfg.get("timeout_seconds", 60))
        cache_tools_list = bool(server_cfg.get("cache_tools_list", True))
        
        if server_type.lower() == "sse":
            server = await stack.enter_async_context(
                MCPServerSse(
                    name=name,
                    params=server_cfg['params'],
                    client_session_timeout_seconds=timeout,
                    cache_tools_list=cache_tools_list,
                )
            )

        else:
            server = await stack.enter_async_context(
                MCPServerStreamableHttp(
                    name=name,
                    params=server_cfg['params'],
                    cache_tools_list=cache_tools_list,
                    client_session_timeout_seconds=timeout,
                )
            )

        # Add to the list
        servers.append(server)
    
    # Return ALL
    return servers


async def build_agent(
    agent_name: str, user_id: str, model_name: str, mcp_servers: List[Dict[str, Any]],
    toolkits: List[str], api_key: str, persona: str, output: str, 
    guidelines: str, context: Dict[str, Any] = {}, tracer: List[Any] = None
) -> Agent:
    # set_tracing_disabled(True)

    if tracer:
        set_trace_processors(tracer)

    # Set Gemini API key for LiteLLM
    import logging
    
    logging.info(f"Building agent with model: {model_name}")
    logging.info(f"API key (first 20 chars): {api_key[:20]}...")
    
    # Always set the environment variable for Gemini API
    # According to https://docs.litellm.ai/docs/providers/gemini
    os.environ["GEMINI_API_KEY"] = api_key
    
    # For openai-agents SDK with LiteLLM, use format: litellm/gemini/gemini-2.5-flash
    # According to openai-agents documentation
    if "gemini" in model_name.lower() and not model_name.startswith("litellm/"):
        original_model = model_name
        model_name = f"litellm/gemini/{model_name}"
        logging.warning(f"TRANSFORMED MODEL: {original_model} → {model_name}")
    else:
        logging.warning(f"MODEL ALREADY HAS PREFIX: {model_name}")

    # In case of any MCPs
    async with AsyncExitStack() as stack:

        mcp_servers = await _build_mcp_servers(stack, mcp_servers)
        arcade_client = AsyncArcade()

        tools = None
        if len(toolkits) > 0:
            context["user_id"] = user_id
            tools = await get_arcade_tools(arcade_client, toolkits=toolkits)

        # Context: Time and __system__ 
        context_string = f"- The time is: {time.asctime()}\n"
        context_string += (context.get("__system__") or "")

        # Guidelines
        if len(guidelines) > 0:
            guidelines_string = "- " + "\n- ".join(guidelines)
        else:
            guidelines_string = ""

        # System prompt
        system_prompt = BASE_PROMPT.format(
            persona=persona,
            guidelines=guidelines_string,
            output=output,
            context=context_string
        )
            
        # Build agent with model string directly (LiteLLM auto-detects from litellm/ prefix)
        # According to openai-agents documentation
        logging.warning(f"CREATING AGENT WITH MODEL: {model_name}")
        agent_kwargs: Dict[str, Any] = {
            "name": agent_name,
            "instructions": system_prompt,
            "model": model_name,  # e.g., "litellm/gemini/gemini-2.5-flash"
            "model_settings": ModelSettings(temperature=0.7),
        }

        # Optional params
        if tools:
            agent_kwargs["tools"] = tools
        
        if mcp_servers:
            agent_kwargs["mcp_servers"] = mcp_servers

        return Agent(**agent_kwargs)