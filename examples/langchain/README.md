# LangChain Vector Database and Memory Systems Example

This example demonstrates how to use LangChain to create an AI agent with vector database integration and sophisticated memory management. It shows how to implement efficient information retrieval, context management, and tool integration patterns.

## Project Structure
```
./
├── vector_memory_agent.py    # Main implementation with vector DB and memory
├── requirements.txt          # Project dependencies
├── run_example.sh           # Helper script to run the example
├── data/                    # Directory for sample data and vector storage
└── .env                     # Environment variables (create this)
```

## Features Demonstrated

1. Vector Database Integration
   - Document embedding and storage
   - Similarity search
   - Context retrieval
   - Efficient information access

2. Memory Management
   - Conversation history
   - Context window management
   - Long-term memory storage
   - Memory pruning strategies

3. Tool Integration
   - Custom tool development
   - Tool chaining
   - Error handling
   - Result caching

## Requirements
- Python 3.10+
- OpenAI API key
- Chroma DB (vector store)

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
- Initialize the vector database
- Run the LangChain example
- Clean up after completion

## Implementation Details

### 1. Vector Database Setup
```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Initialize embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    collection_name="documentation",
    embedding_function=embeddings
)
```

### 2. Memory Management
```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain.memory import ConversationBufferMemory

# Configure memory systems
retriever_memory = VectorStoreRetrieverMemory(
    vectorstore=vectorstore,
    input_key="input"
)

conversation_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
```

### 3. Agent Configuration
```python
from langchain.agents import Tool, AgentExecutor
from langchain.agents import create_structured_chat_agent

# Create agent with memory and tools
agent = create_structured_chat_agent(
    llm=chat_model,
    tools=tools,
    memory=retriever_memory,
    verbose=True
)
```

## Example Tasks

The implementation demonstrates:
1. Document storage and retrieval
2. Contextual question answering
3. Memory-aware conversations
4. Tool-augmented processing

## Customization

You can modify the example by:
1. Adding different vector stores
2. Implementing custom memory systems
3. Creating specialized tools
4. Adjusting retrieval parameters

## Error Handling

The implementation includes:
- Database connection management
- Memory overflow protection
- Tool execution error handling
- Context window management

## Best Practices

1. Vector Database
   - Regular maintenance
   - Index optimization
   - Backup strategies
   - Performance monitoring

2. Memory Management
   - Context relevance
   - Memory cleanup
   - Storage efficiency
   - Privacy considerations

3. Tool Integration
   - Modular design
   - Error recovery
   - Result validation
   - Performance optimization

## Troubleshooting

1. If you encounter OpenAI API errors:
   - Verify your API key in .env
   - Check API rate limits
   - Ensure sufficient credits

2. For vector database issues:
   - Check database connection
   - Verify index integrity
   - Monitor storage usage
   - Optimize query patterns

3. For memory-related problems:
   - Monitor memory usage
   - Check context window limits
   - Verify storage paths
   - Review cleanup policies

This example demonstrates LangChain's capabilities for building sophisticated AI agents with efficient information retrieval and memory management, providing a foundation for developing context-aware AI applications.
