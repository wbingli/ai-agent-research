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

# Must upgrade openai as the bondai openai dependency version is broken
# openai>=1.63.0
uv pip install -U openai

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

## Example output
```
>python bondai_crawler_test.py https://github.com/wbingli/ai-agent-research
Loading environment variables from: /Users/Wenbing.Li/repos/ai-agent-research/examples/bondai/.env

Executing web crawling task for URL: https://github.com/wbingli/ai-agent-research

Using tool website_query: I need to understand the main content of the website to provide a concise summary for the user.
Using tool website_extract_hyperlinks: I need to extract all the hyperlinks from the website to complete the task.
Using tool response_query...
Using tool response_query: I need to extract the hyperlinks from the large response to complete the task.
Using tool response_query: I need to extract the hyperlinks from the large response to complete the task.
Using tool website_extract_hyperlinks: Trying again to extract hyperlinks from the website.
Using tool response_query: I need to extract the hyperlinks from the large response to complete the task.
Using tool website_query: Trying to extract hyperlinks from the content of the website.
Using tool final_answer...
Using tool final_answer...

The main content of the website is a repository for AI agent research. It includes information about AI agent frameworks, applications, papers, articles, and videos related to AI agents. It also provides an evaluation of the BondAI framework. The hyperlinks mentioned in the content are: [https://bondai.dev](https://bondai.dev) and [https://github.com/krohling/bondai](https://github.com/krohling/bondai).
```
