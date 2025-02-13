#!/usr/bin/env python3
"""
Example of using BondAI's built-in tools for web crawling.
"""

import os
import argparse
from termcolor import cprint
from bondai.agents import Agent, AgentEventNames, ConversationalAgent
from bondai.agents.group_chat import GroupConversation, UserProxy
from bondai.models.openai import DefaultOpenAIConnectionParams, OpenAILLM, OpenAIModelNames
from bondai.tools.website import WebsiteQueryTool
from bondai.tools.website import WebsiteExtractHyperlinksTool as ExtractHyperlinksTool
from bondai.tools import AgentTool
from bondai.memory import MemoryManager, InMemoryCoreMemoryDataSource
from dotenv import find_dotenv, load_dotenv

def parse_arguments():
    parser = argparse.ArgumentParser(description='BondAI web crawler')
    parser.add_argument('url', help='URL to crawl')
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_arguments()

    # Configure OpenAI connection
    dotenv_path = find_dotenv()
    print(f"Loading environment variables from: {dotenv_path}")
    load_dotenv()

    openai_key = os.getenv("OPENAI_API_KEY")
    DefaultOpenAIConnectionParams.configure_openai_connection(api_key=openai_key)

    task = f"""Visit {args.url} and extract the following information:
1. The main content of the page about tools
2. Summarize the key points about BondAI tools
3. Extract a list of hyperlinks from this website

Format your response in the following structure:

## Main Content
[Provide a concise summary of the main content about tools]

## Links
[List any extracted hyperlinks, or None if none were found]
"""

    # Create the task execution agent with tools
    task_execution_agent = Agent(
        llm=OpenAILLM(OpenAIModelNames.GPT4_0613),
        tools=[WebsiteQueryTool(), ExtractHyperlinksTool()],
        max_tool_retries=5,
        memory_manager=MemoryManager(
            core_memory_datasource=InMemoryCoreMemoryDataSource(
                sections={"task": "No information has been stored about the current task."},
                max_section_size=10000,
            )
        ),
    )

    # Add tool selection event handler
    @task_execution_agent.on(AgentEventNames.TOOL_SELECTED)
    def tool_selected(agent, tool_message):
        if tool_message.tool_arguments and "thought" in tool_message.tool_arguments:
            message = f"Using tool {tool_message.tool_name}: {tool_message.tool_arguments['thought']}"
        else:
            message = f"Using tool {tool_message.tool_name}..."
        cprint(message, "green")

    # Create the user liaison agent
    user_liaison_agent = ConversationalAgent(
        llm=OpenAILLM(OpenAIModelNames.GPT4_0613),
        name="User Liaison",
        persona="I am a helpful assistant that coordinates between users and the task execution system.",
        persona_summary="Friendly coordinator between users and task execution",
        instructions="Help users interact with the task execution system and present results in a clear, organized manner.",
        tools=[AgentTool(task_execution_agent)],
        enable_conversation_tools=False,
        enable_conversational_content_responses=True,
        enable_exit_conversation=False,
        memory_manager=MemoryManager(
            core_memory_datasource=InMemoryCoreMemoryDataSource(
                sections={"user": "No information has been stored about the user."},
            )
        ),
    )

    # Set up the group conversation
    user_proxy = UserProxy(parse_recipients=False)
    group_conversation = GroupConversation(
        conversation_members=[user_proxy, user_liaison_agent]
    )

    # Run the task through the user liaison
    print(f"\nExecuting web crawling task for URL: {args.url}\n")
    group_conversation.send_message(
        recipient_name="User Liaison",
        message=task
    )

if __name__ == "__main__":
    main()
