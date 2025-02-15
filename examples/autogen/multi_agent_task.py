#!/usr/bin/env python3
"""
AutoGen Multi-Agent Example demonstrating collaboration between different types of agents.
This example shows how multiple agents can work together to solve a complex task.
"""

import os
import autogen
from dotenv import find_dotenv, load_dotenv
from termcolor import cprint

# Load environment variables
dotenv_path = find_dotenv()
print(f"Loading environment variables from: {dotenv_path}")
load_dotenv()

# Configure OpenAI
config_list = [
    {
        'model': 'gpt-4',
        'api_key': os.getenv('OPENAI_API_KEY'),
    }
]

# Create agent configurations
assistant_config = {
    "seed": 42,  # for reproducibility
    "temperature": 0.7,
    "config_list": config_list,
    "timeout": 120,
}

# Initialize agents
assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=assistant_config,
    system_message="You are a helpful AI assistant focused on problem-solving."
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=assistant_config,
    system_message="You are an expert programmer who writes clean, efficient code."
)

user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

def main():
    """
    Main function to demonstrate multi-agent collaboration.
    """
    # Example task: Create a simple data analysis script
    task = """
    Please help me with the following task:
    1. Create a Python script that generates random data
    2. Perform basic statistical analysis
    3. Create a visualization
    4. Save the results to a file

    The solution should be well-documented and efficient.
    """

    # Start the conversation
    user_proxy.initiate_chat(
        assistant,
        message=task
    )

    # The conversation will automatically continue between agents
    # Each agent will contribute based on their expertise
    # The conversation ends when a termination message is detected
    # or max_consecutive_auto_reply is reached

if __name__ == "__main__":
    # Create coding directory if it doesn't exist
    os.makedirs("coding", exist_ok=True)

    print("\nStarting AutoGen Multi-Agent Example...")
    print("----------------------------------------")
    main()
    print("----------------------------------------")
    print("Example completed. Check the 'coding' directory for output files.")
