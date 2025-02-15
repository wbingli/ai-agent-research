import os
import sys
from pathlib import Path
import asyncio
from dotenv import find_dotenv, load_dotenv

from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig

# Load environment variables from .env file
dotenv_path = find_dotenv()
print(f"Loading environment variables from: {os.path.abspath(dotenv_path)}")
dot_end = load_dotenv()

# Initialize browser with Chrome in debug mode
browser = Browser(
    config=BrowserConfig(
        # NOTE: Chrome must be closed for debug mode
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    )
)

async def main():
    agent = Agent(
        task=(
            'Go to https://github.com/browser-use/browser-use and star the repository. '
            'If login is needed, use the GITHUB_USERNAME and GITHUB_PASSWORD environment variables.'
            'If Chrome browse needs to use profile, select Wenbing Li profile.'
        ),
        llm=ChatOpenAI(model='anthropic/claude-3.5-sonnet',
                       api_key=os.getenv("OPENROUTER_API_KEY"),
                       base_url="https://openrouter.ai/api/v1"),
        browser=browser,
    )

    try:
        await agent.run()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        await browser.close()
        input('Press Enter to close...')

if __name__ == '__main__':
    asyncio.run(main())
