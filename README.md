# My AI Agent Research

This is repo I'm looking into the AI agent technologies and current market trends, focus on AI Agent frameworks and AI Agent applications.

## Generated Docs

- [Open API Deep Research Report](reports/open-api-deep-research.md)
- [Gemini Deep Research Report](reports/gemini-deep-research-report.md)
- [Browse Use Deep Search Report](reports/browse-use-deep-search-report.md)

## Websites & Videos & Channels

 - [Athina AI Hub](https://hub.athina.ai/): The Athina AI Hub is a dedicated resource for AI development teams, offering valuable insights, curated content, and actionable knowledge.
 - [WorldofAI@youtube](https://www.youtube.com/@intheworldofai):  This youtube channel has many AI agents and actually source code on the latest AI agents news.

 ## Articles & Links

 - [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
 - [Github Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents)
 - [Best AI Agent Papers in 2024](https://juteq.ca/biggest-ai-agent-paper-releases-2024/)

## Papers

 - [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
    - https://react-lm.github.io/
 - [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)
 - [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
 - [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://www.microsoft.com/en-us/research/uploads/prod/2024/11/MagenticOne.pdf)



## AI Agent

 - [OpenAI Swarm](https://github.com/openai/swarm)
 - [BondAI](examples/bondai/README.md)
 - [Cline](https://cline.bot/)
 - [Model Context Protocol](https://modelcontextprotocol.io/)
   - MCP Servers: https://github.com/modelcontextprotocol/servers
   - [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
   - [Awesome MCP Clients](https://github.com/punkpeye/awesome-mcp-clients/)
   - [MCP Servers Category](https://glama.ai/mcp/servers)
   - [Smithery MCP registry](https://smithery.ai/)


### BondAI Framework Evaluation

- https://bondai.dev
- https://github.com/krohling/bondai

Why I try this one first?  Well, I randomly picked this one from the awesome-ai-agents list, :)

#### Overview
The BondAI framework demonstrates an interesting approach to AI agents by implementing a multi-agent architecture. Based on my evaluation of the web crawler example (`examples/bondai/`), here's a comprehensive analysis:

#### Evaluation

**Strengths:**
 - Simple and easy to use
 - Well documented

**Limitations:**
- I think it's dead, no more update for a year.
- Less observability how framework and agents work together
- No web UI or integration with other Web UI tools
- Limited built-in agents and tools
- Small community and limited third-party integrations
- Not update-to-date with library dependencies

#### My Conclusion
It's a simple framework to understand the basic concept of AI agents, but it's almost dead and not suitable for any production use Coding Agents

### Browse Use Evaluation

#### Overview
Browse Use provides a simple browse agent that can be used for anything related to browsing the web.

#### Evaluation

**Strengths:**
- Simple and easy to use for browsing the web
- Support to use local Chrome instance, good for accessing and authentication for private web pages
- Good examples and documentation
- Great web UI and deep research mode by leveraging the browsing capabilities

**Limitations:**
- Limited to browsing the web, not integrate with other tools or agents
- Not integrated with other agents and multiple agent collaboration mode
- Based on langchain agent, not seems to be used by other frameworks

#### My Conclusion
Browse use is a good tool for anything related to browsing the web, but it's not well integrated with other agents and tools, and based on langchain agent, not seems to be used by other frameworks.


### Coding Agents

### Cline
Most excited coding agent so far. Everyone should try this one.
https://cline.bot/

#### My Experience
- Great experience with the live file editing, looks like a real pair programming with AI. Other coding agent will just modify the code in the background, which is not as interactive as Cline.
- I choice the model claude+Sonnet 3.5, which works well with the code. I think this model is well trained for the coding task and with agent mode.
- I use OpenRouter as API router, the Anthropic API has too low API rate limit, really bad experience with it.
- Some medium level tasks (e.g. an API with unit test and refactoring) normally takes around less than 10 minutes to complete, with some of user input.
- The cost is kind of high, for a medium task is around $2~5. I think it's worth it since I'm not spend all of my time on coding.


