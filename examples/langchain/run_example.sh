#!/bin/bash

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Create and activate virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create data directory if it doesn't exist
mkdir -p data/vectorstore

# Run the example
echo "Running LangChain vector memory example..."
python vector_memory_agent.py

# Deactivate virtual environment
deactivate

echo "Example completed. Check the 'data' directory for vector store data."
