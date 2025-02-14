# My AI Agent Research

This is repo I'm looking into the AI agent technologies and current market trends, focus on AI Agent frameworks and AI Agent applications.

## Generated Docs

- [Gemini Deep Research Report](reports/gemini-deep-research-report.md)
- [Browse Use Deep Search Report](reports/browse-use-deep-search-report.md)

## Videos & Channels

 - [WorldofAI@youtube](https://www.youtube.com/@intheworldofai):  This youtube channel has many AI agents and actually source code on the latest AI agents news.

 ## Articles

 - [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
 - [Github Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents)

## Papers

 - [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
    - https://react-lm.github.io/
 - [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)
 - [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)



## AI Agent Frameworks

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


## Coding Agents

### Cline
Most excited coding agent so far. Everyone should try this one.
https://cline.bot/

#### My Experience
- Great experience with the live file editing, looks like a real pair programming with AI. Other coding agent will just modify the code in the background, which is not as interactive as Cline.
- I choice the model claude+Sonnet 3.5, which works well with the code. I think this model is well trained for the coding task.
- I use OpenRouter as API router, the Anthropic API has too low API rate limit, really bad experience with it.
- Some medium level tasks (e.g. an API with unit test and refactoring) normally takes around less than 10 minutes to complete, with some of user input.
- The cost is kind of high, for a medium task is around $2~5. I think it's worth it since I'm not spend all of my time on coding.


