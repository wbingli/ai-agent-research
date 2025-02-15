import os
import json
import boto3
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

class BedrockAgentClient:
    def __init__(
        self,
        agent_id: str,
        agent_alias: str = "DRAFT",
        region: Optional[str] = None
    ):
        """
        Initialize the Bedrock Agent client.

        Args:
            agent_id: The ID of the Bedrock agent
            agent_alias: The alias of the agent (default: "DRAFT")
            region: AWS region (optional, defaults to environment variable)
        """
        self.agent_id = agent_id
        self.agent_alias = agent_alias
        self.region = region or os.getenv("AWS_REGION", "us-west-2")

        # Initialize Bedrock client
        self.bedrock_agent = boto3.client(
            "bedrock-agent-runtime",
            region_name=self.region
        )

    def invoke(self, prompt: str) -> Dict[Any, Any]:
        """
        Invoke the Bedrock agent with a prompt.

        Args:
            prompt: The natural language prompt for the agent

        Returns:
            Dict containing the agent's response
        """
        try:
            response = self.bedrock_agent.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=self.agent_alias,
                sessionId=self._generate_session_id(),
                inputText=prompt
            )

            return {
                "completion": response.get("completion"),
                "session_id": response.get("sessionId"),
                "response_metadata": response.get("ResponseMetadata")
            }

        except Exception as e:
            print(f"Error invoking agent: {str(e)}")
            raise

    def _generate_session_id(self) -> str:
        """Generate a unique session ID for the conversation."""
        import uuid
        return str(uuid.uuid4())

class TaskRequest(BaseModel):
    """Model for task requests to the agent."""
    task_description: str
    priority: Optional[str] = "medium"
    deadline: Optional[str] = None

def main():
    """Example usage of the Bedrock Agent."""
    # Initialize the agent client
    agent = BedrockAgentClient(
        agent_id=os.getenv("BEDROCK_AGENT_ID"),
        agent_alias=os.getenv("BEDROCK_AGENT_ALIAS", "DRAFT")
    )

    # Example task: Create a task management system
    task = TaskRequest(
        task_description="Create a new project task for implementing user authentication",
        priority="high",
        deadline="2024-03-01"
    )

    # Construct the prompt
    prompt = f"""
    Please help me create a new task with the following details:
    - Description: {task.task_description}
    - Priority: {task.priority}
    - Deadline: {task.deadline}

    Please create the task and return the task ID and status.
    """

    try:
        # Invoke the agent
        response = agent.invoke(prompt)

        # Print the response
        print("\nAgent Response:")
        print(json.dumps(response, indent=2))

    except Exception as e:
        print(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main()
