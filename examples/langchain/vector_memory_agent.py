#!/usr/bin/env python3
"""
LangChain Vector Database and Memory Systems Example.
Demonstrates integration with vector databases, memory management, and tool usage.
"""

import os
from typing import List, Dict
from dotenv import find_dotenv, load_dotenv
from termcolor import cprint

from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory, ConversationBufferMemory
from langchain.agents import Tool, AgentExecutor, create_structured_chat_agent
from langchain.tools import BaseTool
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
dotenv_path = find_dotenv()
print(f"Loading environment variables from: {dotenv_path}")
load_dotenv()

class DocumentManager:
    """Manages document storage and retrieval using vector database."""

    def __init__(self, persist_directory: str = "data/vectorstore"):
        """Initialize document manager with vector store."""
        self.embeddings = OpenAIEmbeddings()
        self.persist_directory = persist_directory

        # Create persistence directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize vector store
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

        # Initialize text splitter for document chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to vector store."""
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)

        # Add to vector store
        self.vectorstore.add_documents(texts)
        print(f"Added {len(texts)} document chunks to vector store")

    def search_documents(self, query: str, k: int = 4) -> List[Document]:
        """Search for relevant documents."""
        return self.vectorstore.similarity_search(query, k=k)

class CustomTools:
    """Collection of custom tools for the agent."""

    def __init__(self, document_manager: DocumentManager):
        """Initialize tools with document manager."""
        self.document_manager = document_manager

    def get_tools(self) -> List[BaseTool]:
        """Get list of available tools."""
        return [
            Tool(
                name="SearchDocuments",
                func=self.document_manager.search_documents,
                description="Search for relevant documents using a query string"
            )
        ]

def setup_memory_systems(vectorstore: Chroma) -> Dict:
    """Configure different memory systems."""
    return {
        "vector_memory": VectorStoreRetrieverMemory(
            retriever=vectorstore.as_retriever(),
            input_key="input"
        ),
        "conversation_memory": ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    }

def create_agent(
    llm: ChatOpenAI,
    tools: List[BaseTool],
    memory: Dict,
    verbose: bool = True
) -> AgentExecutor:
    """Create an agent with tools and memory."""
    # Create the agent
    agent = create_structured_chat_agent(
        llm=llm,
        tools=tools,
        verbose=verbose
    )

    # Create the agent executor
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=memory["vector_memory"],
        verbose=verbose
    )

def main():
    """Main function demonstrating vector store and memory capabilities."""
    # Initialize document manager
    doc_manager = DocumentManager()

    # Create sample documents
    sample_docs = [
        Document(
            page_content="LangChain is a framework for developing applications powered by language models.",
            metadata={"source": "documentation"}
        ),
        Document(
            page_content="Vector databases are essential for efficient similarity search in large document collections.",
            metadata={"source": "tutorial"}
        )
    ]

    # Add documents to vector store
    print("\nAdding sample documents to vector store...")
    doc_manager.add_documents(sample_docs)

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7
    )

    # Set up tools
    tools = CustomTools(doc_manager).get_tools()

    # Set up memory systems
    memory = setup_memory_systems(doc_manager.vectorstore)

    # Create agent
    print("\nCreating agent with vector store and memory...")
    agent_executor = create_agent(llm, tools, memory)

    # Example queries
    queries = [
        "What is LangChain?",
        "How are vector databases used?",
        "Can you explain the relationship between LangChain and vector databases?"
    ]

    # Run queries
    print("\nExecuting example queries...")
    for query in queries:
        print(f"\nQuery: {query}")
        try:
            response = agent_executor.invoke({"input": query})
            print(f"Response: {response['output']}")
        except Exception as e:
            print(f"Error processing query: {str(e)}")

    print("\nExample completed! Check the 'data' directory for vector store data.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise
