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

# Create the coding directory if it doesn't exist
mkdir -p coding

# Run the example
echo "Running AutoGen multi-agent example..."
python multi_agent_task.py

# Deactivate virtual environment
deactivate

echo "Example completed. Check the 'coding' directory for output files."
