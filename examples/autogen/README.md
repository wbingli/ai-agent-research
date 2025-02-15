# AutoGen Multi-Agent Example

This example demonstrates how to use Microsoft's AutoGen framework to create a multi-agent system that collaborates on complex tasks. The example shows how multiple AI agents can work together, each with specialized roles, to solve problems through conversation and code execution.

## Project Structure
```
./
├── multi_agent_task.py     # Main implementation of multi-agent system
├── requirements.txt        # Project dependencies
├── run_example.sh         # Helper script to run the example
└── .env                   # Environment variables (create this)
```

## Features Demonstrated

1. Multi-Agent Collaboration
   - Assistant Agent: Primary problem solver
   - Code Agent: Handles code-related tasks
   - User Proxy: Represents user in the conversation

2. Advanced Capabilities
   - Inter-agent communication
   - Code execution
   - Memory management
   - Error handling
   - Task coordination

## Requirements
- Python 3.10+
- OpenAI API key

## Environment Setup

1. Create a `.env` file in this directory with your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

2. Run the example using the provided script:
```bash
./run_example.sh
```

The script will:
- Create a virtual environment
- Install dependencies
- Run the multi-agent example
- Clean up after completion

## Implementation Details

### 1. Agent Configuration
The example configures three types of agents:
```python
# Assistant Agent - General problem solver
assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=assistant_config,
    system_message="You are a helpful AI assistant focused on problem-solving."
)

# Code Agent - Programming specialist
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=assistant_config,
    system_message="You are an expert programmer who writes clean, efficient code."
)

# User Proxy - Represents the user
user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    }
)
```

### 2. Task Execution
The example demonstrates a data analysis task:
1. Generate random data
2. Perform statistical analysis
3. Create visualizations
4. Save results

### 3. Output
The example creates a 'coding' directory containing:
- Generated Python scripts
- Data analysis results
- Visualizations

## Customization

You can modify the example by:
1. Adjusting agent configurations
2. Changing the task description
3. Adding new agent types
4. Modifying code execution settings

## Error Handling

The implementation includes:
- Timeout settings
- Maximum reply limits
- Error recovery mechanisms
- Clean workspace management

## Best Practices

1. Agent Design
   - Clear role definition
   - Focused capabilities
   - Efficient communication

2. Resource Management
   - Token usage optimization
   - Memory management
   - API rate limiting

3. Security
   - API key protection
   - Code execution safety
   - Data privacy

## Troubleshooting

1. If you encounter OpenAI API errors:
   - Verify your API key in .env
   - Check API rate limits
   - Ensure sufficient credits

2. For execution errors:
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Ensure write permissions in the coding directory

This example serves as a foundation for building more complex multi-agent systems using AutoGen, demonstrating key concepts and best practices for effective agent collaboration.
