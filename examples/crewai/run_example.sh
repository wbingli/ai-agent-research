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

# Run the example
echo "Running CrewAI task orchestration example..."
python task_orchestration.py

# Deactivate virtual environment
deactivate

echo "Example completed. Check research_output.md for results."
