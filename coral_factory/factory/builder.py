from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List
import os
import logging

# Use simple LiteLLM agent instead of openai-agents
from factory.simple_agent import build_simple_agent, SimpleLiteLLMAgent
from factory.agent_one import AgentConfig
from factory.trace_stream import OpenAIAgentsTracingProcessor

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Global variables
agents = {}
global_context = None

class RelationsType(str, Enum):
    single = "single"
    manager = "manager"
    chain = "chain"
    group_chat = "group-chat"
    triage = "triage"

class WorkflowConfig(BaseModel):
    objective: str
    relations_type: RelationsType
    model_name: str
    api_key: str
    agents: List[AgentConfig]

async def delegate_task(agent_name: str, task: str):
    """Delegate task to a specific agent"""
    logging.info(f"Calling agent {agent_name} with task {task}")
    result = await agents[agent_name].run(task, context=global_context)
    logging.info(f"Agent {agent_name} returned:\n{result[:100]}...\n\n")
    return result


async def builder(json_config: Dict[str, Any], user_id: str, tracer: list):
    """
    Builds the manager agent and returns it.

    Manager agent contains all the agents and can call them to solve the user's task.
    """
    global agents
    
    # Build overview for manager agent
    overview = "You are a manager agent. Solve the user's task by delegating tasks to the appropriate agents and delegating the tasks to them.\n"
    overview += "Think step by step and do not ask the user for clarification, just execute the task as best as you can."
    overview += "You have access to the following agents:\n"

    for agent in json_config["agents"]:
        overview += f"{agent['name']}: {agent['persona']}\n"

    agents = {}
    for agent in json_config["agents"]:

        agent['context'] = {
            "__system__": f"The time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }

        agents[agent['name']] = await build_simple_agent(
            agent_name=agent['name'],
            user_id=user_id,
            model_name=json_config["model_name"],
            mcp_servers=agent['mcp_servers'],
            toolkits=agent['toolkits'],
            api_key=json_config["api_key"],
            persona=agent['persona'],
            output=agent['output'],
            guidelines=agent['guidelines'],
            context=agent['context'],
            tracer=tracer
        )

    return agents, overview


async def start_agents(workflow_config: WorkflowConfig, user_task: str, user_id: str):
    global global_context
    global_context = {
        "user_id": user_id,
    }

    # SET API KEY AT THE START - CRITICAL FOR LITELLM!
    os.environ["GEMINI_API_KEY"] = workflow_config.api_key
    logging.warning(f"SET GEMINI_API_KEY IN ENVIRONMENT: {workflow_config.api_key[:20]}...")

    tracer = None
    firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
    firebase_service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    
    logging.info(f"Firebase config check:")
    logging.info(f"  FIREBASE_PROJECT_ID: {firebase_project_id}")
    logging.info(f"  FIREBASE_SERVICE_ACCOUNT_PATH: {firebase_service_account_path}")
    logging.info(f"  user_id: {user_id}")
    
    if firebase_project_id and firebase_service_account_path:
        logging.info("Creating OpenAIAgentsTracingProcessor...")
        try:
            tracer = [OpenAIAgentsTracingProcessor(
                firebase_project_id=firebase_project_id,
                firebase_service_account_path=firebase_service_account_path,
                user_id=user_id
            )]
            logging.info("Tracer created successfully!")
        except Exception as e:
            logging.error(f"Failed to create tracer: {e}")
            import traceback
            logging.error(traceback.format_exc())
    else:
        logging.warning("Firebase not configured - traces will not be saved!")

    if len(workflow_config.agents) == 0:
        raise ValueError("No agents provided")

    builder_json = workflow_config.model_dump()
    agents, overview = await builder(builder_json, user_id=user_id, tracer=tracer)

    if workflow_config.relations_type == "manager":
        # Manager: Run all agents in sequence, each building on the previous
        logging.info(f"Starting manager workflow with {len(agents)} agents")
        results = []
        current_task = user_task
        
        for agent_name, agent in agents.items():
            logging.info(f"Running agent: {agent_name}")
            try:
                result = await agent.run(current_task)
                results.append(f"**{agent_name}:**\n{result}\n")
                # Pass the result to the next agent as context
                current_task = f"Previous agent ({agent_name}) output:\n{result}\n\nOriginal task: {user_task}\n\nContinue with your part of the workflow."
                logging.info(f"Agent {agent_name} completed successfully")
            except Exception as e:
                logging.error(f"Agent {agent_name} failed: {e}")
                results.append(f"**{agent_name}:** ❌ Failed - {str(e)}\n")
        
        # Combine all results
        final_result = "\n---\n\n".join(results)
        return final_result

    elif workflow_config.relations_type == "chain":
        # Chain: Run agents in sequence, passing output to next
        logging.info(f"Starting chain workflow with {len(agents)} agents")
        current_output = user_task
        
        for agent_name, agent in agents.items():
            logging.info(f"Running agent: {agent_name}")
            current_output = await agent.run(current_output)
            logging.info(f"Agent {agent_name} completed")
        
        return current_output

    elif workflow_config.relations_type == "group-chat":
        # Group chat: All agents process the task and combine results
        logging.info(f"Starting group chat with {len(agents)} agents")
        results = []
        
        for agent_name, agent in agents.items():
            logging.info(f"Running agent: {agent_name}")
            try:
                result = await agent.run(user_task)
                results.append(f"**{agent_name}:**\n{result}\n")
                logging.info(f"Agent {agent_name} completed")
            except Exception as e:
                logging.error(f"Agent {agent_name} failed: {e}")
                results.append(f"**{agent_name}:** ❌ Failed - {str(e)}\n")
        
        return "\n---\n\n".join(results)

    elif workflow_config.relations_type == "triage":
        # Triage: Use first agent to route, then execute appropriate agent
        # For now, run all agents in sequence
        logging.info(f"Starting triage workflow with {len(agents)} agents")
        results = []
        
        for agent_name, agent in agents.items():
            logging.info(f"Running agent: {agent_name}")
            try:
                result = await agent.run(user_task)
                results.append(f"**{agent_name}:**\n{result}\n")
                logging.info(f"Agent {agent_name} completed")
            except Exception as e:
                logging.error(f"Agent {agent_name} failed: {e}")
                results.append(f"**{agent_name}:** ❌ Failed - {str(e)}\n")
        
        return "\n---\n\n".join(results)

    elif workflow_config.relations_type == "single":
        first_agent_name = workflow_config.agents[0].name
        first_agent = agents[first_agent_name]
        logging.info(f"Running single agent: {first_agent_name}")
        result = await first_agent.run(user_task)
        return result



## TODO
# https://openai.github.io/openai-agents-python/handoffs/
# custom handoffs with predefined inputs!!!

## TODO
## OpenAI websearch support
## OpenAI file support

## TODO
## ASYNC tools calling
## More agent patterns -> handoffs, chain, group-chat, etc.

## TODO
## Proper context passing for user_id

## TODO
## Add smitery API key resolution


## TODO
## - Anomynizer??
## - Langfuse integration
## - Config gaurdrails????