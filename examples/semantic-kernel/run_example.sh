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

# Create necessary directories
echo "Creating directories..."
mkdir -p data
mkdir -p prompts/summarize
mkdir -p prompts/analyze

# Ensure semantic function files are in place
if [ ! -f "prompts/summarize/config.json" ] || [ ! -f "prompts/summarize/skprompt.txt" ] || \
   [ ! -f "prompts/analyze/config.json" ] || [ ! -f "prompts/analyze/skprompt.txt" ]; then
    echo "Error: Missing semantic function files in prompts directory"
    exit 1
fi

# Run the example
echo "Running Semantic Kernel example..."
python semantic_functions.py

# Deactivate virtual environment
deactivate

echo "Example completed. Check output for results."
