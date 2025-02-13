# BondAI Web Crawler Example

A web crawler implementation using BondAI's multi-agent architecture.

## Requirements
- Python 3.10
- uv package manager

## Environment Setup with UV

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Ensure Python 3.10 is available
# On macOS using pyenv:
pyenv install 3.10
pyenv local 3.10

# 3. Create and activate a new virtual environment with Python 3.10
uv venv --python=python3.10 venv

# For macOS/Linux:
source venv/bin/activate
# For Windows:
# venv/Scripts/activate

# Verify Python version
python --version  # Should output Python 3.10.x

# 4. Install dependencies using uv
uv pip install -r requirements.txt

# 5. Configure OpenAI API key
# Create a .env file in this directory
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## Project Structure
```
./
├── bondai_crawler_test.py  # Main crawler script
├── requirements.txt        # Project dependencies
├── venv/                  # Python virtual environment (Python 3.10)
└── .env                   # Environment variables (create this)
```

## Usage
```bash
# Ensure your virtual environment is activated
source venv/bin/activate  # macOS/Linux
# venv/Scripts/activate   # Windows

# Run the crawler with a specific URL
# Example with the original AI agents repository
python bondai_crawler_test.py https://bondai.dev/
```

The crawler will:
1. Visit the specified URL
2. Extract and summarize the main content
3. List all hyperlinks found on the page
4. Present the results in a structured format

## Features
- Multi-agent architecture for separation of concerns
- Built-in web crawling tools (WebsiteQueryTool, WebsiteExtractHyperlinksTool)
- Event-driven tool selection with visual feedback
- In-memory core storage for maintaining context
- GPT-4 integration for intelligent processing
- Command-line interface for flexible URL input

## Troubleshooting

1. Python version issues:
   - Ensure you have Python 3.10 installed: `python --version`
   - If using pyenv: `pyenv install 3.10` and `pyenv local 3.10`
   - Create a new venv if you had one with a different Python version

2. If you see OpenAI API key errors:
   - Ensure your .env file exists and contains the correct API key
   - Make sure you're running the script from this directory

3. If you see import errors:
   - Verify your virtual environment is activated
   - Try reinstalling dependencies: `uv pip install -r requirements.txt`
