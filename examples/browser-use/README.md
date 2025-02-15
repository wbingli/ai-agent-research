# Browser-Use Agent Example: GitHub Star

This example demonstrates how to use browser-use's Agent functionality to star a GitHub repository using natural language instructions. The agent automatically handles browser automation based on a simple text prompt.

## Requirements
- Python 3.12
- uv package manager
- Google Chrome (must be closed before running)

## Environment Setup with UV

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Ensure Python 3.12 is available
# On macOS using pyenv:
pyenv install 3.12
pyenv local 3.12

# 3. Create and activate a new virtual environment with Python 3.12
uv venv --python=python3.12 venv

# For macOS/Linux:
source venv/bin/activate
# For Windows:
# venv/Scripts/activate

# Verify Python version
python --version  # Should output Python 3.12.x

# 4. Install dependencies using uv
uv pip install -r requirements.txt

# 5. Configure environment variables
# Create a .env file in this directory
echo "OPENAI_API_KEY=your_api_key_here" > .env
# Optional: Add GitHub credentials if you want to star while logged in
echo "GITHUB_USERNAME=your_username" >> .env
echo "GITHUB_PASSWORD=your_password" >> .env
```

## Project Structure
```
./
├── star_with_agent.py    # Main script using browser-use Agent
├── requirements.txt      # Project dependencies
├── venv/                # Python virtual environment (Python 3.12)
└── .env                 # Environment variables (create this)
```

## Usage
```bash
# Ensure your virtual environment is activated
source venv/bin/activate  # macOS/Linux
# venv/Scripts/activate  # Windows

# Run the script
python star_with_agent.py
```

## How It Works

The script uses browser-use's Agent class, which combines:
- LangChain for natural language processing
- Browser automation capabilities
- GPT-4 for understanding and executing tasks

The agent interprets a natural language task description and automatically performs the necessary browser interactions to accomplish it.

## Customization

You can modify the `task` parameter in the script to perform different browser automation tasks. The agent will interpret the natural language instructions and perform the appropriate actions.

Example tasks:
```python
task='Go to https://github.com/browser-use/browser-use and star the repository'
# or
task='Search for browser-use on GitHub and star their main repository'
```
