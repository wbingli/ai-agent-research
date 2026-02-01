# MCP (Model Context Protocol) Pitfalls and Limitations: A Comprehensive Analysis

*Research Report - January 2026*

## Executive Summary

The Model Context Protocol (MCP) has rapidly become the de-facto standard for connecting AI assistants to external systems since its November 2024 launch by Anthropic. However, real-world deployment has revealed significant pitfalls and limitations that practitioners must understand. This report analyzes the key challenges across context efficiency, security, production readiness, and practical workflow constraints.

---

## Table of Contents

1. [Context Window Overhead from Tool Definitions](#1-context-window-overhead-from-tool-definitions)
2. [Comparison to Native Function Calling and CLI Tools](#2-comparison-to-native-function-calling-and-cli-tools)
3. [Batching and Workflow Limitations](#3-batching-and-workflow-limitations)
4. [Security and Prompt Injection Concerns](#4-security-and-prompt-injection-concerns)
5. [Real-World Practitioner Pain Points](#5-real-world-practitioner-pain-points)
6. [What Needs to Change for Production Readiness](#6-what-needs-to-change-for-production-readiness)
7. [Key Recommendations](#7-key-recommendations)

---

## 1. Context Window Overhead from Tool Definitions

### The Token Tax Problem

One of the most significant but underappreciated issues with MCP is the massive token cost of loading tool definitions into context. Geoffrey Huntley's analysis ("Too Many MCP Servers on the Dance Floor") highlights this critical issue:

> "The usable context window for tools like Amp or Cursor is around 176,000 tokens—Claude 4's 200,000 minus around 24,000 for the system prompt. Adding just the popular GitHub MCP defines 93 additional tools and swallows another **55,000** of those valuable tokens!"

**Key Statistics:**
- GitHub MCP alone: ~55,000 tokens (was ~50,000 tokens at launch before optimization)
- Microsoft VS Code recently removed the 128 tool limit, which practitioners consider harmful
- Cursor caps MCP tools at 40 specifically to prevent context bloat
- Every tool definition occupies space *before the agent even reads the user's request*

### Degraded Performance with More Tools

LLM reliability **negatively correlates** with the amount of instructional context provided. This is counterintuitive for users who believe more integrations equals better performance:

> "As the servers get bigger (i.e., more tools) and users integrate more of them, an assistant's performance will degrade all while increasing the cost of every single request." — Shrivu Shankar

The problem compounds because:
1. Tool definitions are loaded upfront into every conversation
2. Users pay for these tokens in *every follow-up message*
3. More irrelevant tools = worse reasoning accuracy from the LLM

---

## 2. Comparison to Native Function Calling and CLI Tools

### CLI Tools: Near-Zero Token Cost

Experienced practitioners have largely moved away from MCP for coding workflows in favor of CLI tools:

> "Use GitHub's MCP and see 23k tokens gone. Or use the `gh` CLI which has basically the same feature set, models already know how to use it, and pay zero context tax." — Peter Steinberger

**Why CLIs outperform MCP for many use cases:**
- LLMs already know how to use popular CLI tools (git, gh, curl, etc.)
- Zero upfront token cost—tool discovery happens on-demand
- CLI help text serves as documentation at call time, not load time
- Agents can run `--help` to learn tool interfaces dynamically

### The "Scripting" Model vs. Tool Calling

Shrivu Shankar's evolution of agent autonomy models:

1. **Single Prompt**: Giving the agent all context in one massive prompt (brittle, doesn't scale)
2. **Tool Calling** (Classic MCP): Hand-crafted tools abstracting reality (creates new abstractions and context bottlenecks)
3. **Scripting**: Agent accesses raw environment—binaries, scripts, docs—and writes code on the fly

> "The 'Scripting' model (now formalized by Skills) is better, but it needs a secure way to access the environment. This to me is the new, more focused role for MCP."

### When MCP Still Makes Sense

MCP's legitimate use cases have narrowed to:
- **Authentication gateway**: Managing auth, networking, and security boundaries
- **Stateful environments**: Complex, stateful tools like Playwright
- **High-level data access**: A few powerful tools like `download_raw_data(filters...)`, `take_sensitive_gated_action(args...)`

> "Instead of a bloated API, an MCP should be a simple, secure gateway that provides a few powerful, high-level tools... then get out of the way."

---

## 3. Batching and Workflow Limitations

### Intermediate Results Consume Context

Anthropic's engineering blog identifies the second major inefficiency: intermediate tool results pass through the model context window between operations.

**Example Problem:**
```
User: "Download my meeting transcript from Google Drive and attach it to the Salesforce lead."

TOOL CALL: gdrive.getDocument(documentId: "abc123")
→ returns full transcript (loaded into context)

TOOL CALL: salesforce.updateRecord(...)
→ model writes entire transcript into context AGAIN
```

For a 2-hour meeting transcript, this could mean **50,000 additional tokens** processed. Larger documents may exceed context limits entirely.

### No Built-in Batching or Orchestration

Current MCP design forces linear, round-trip execution:
1. Agent requests tool
2. MCP executes
3. Result returns to agent context
4. Agent decides next step
5. Repeat

This creates problems for:
- **Complex workflows** requiring multiple dependent operations
- **Large data processing** where filtering should happen before context loading
- **Error handling** requiring sophisticated retry logic

### Code Execution as a Workaround

Anthropic's proposed solution involves presenting MCP servers as code APIs rather than direct tool calls:

```typescript
// With code execution - filter in execution environment
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(row => row["Status"] === 'pending');
console.log(`Found ${pendingOrders.length} pending orders`);
console.log(pendingOrders.slice(0, 5)); // Only log first 5
```

This approach achieved **98.7% token savings** in Cloudflare's testing ("Code Mode").

---

## 4. Security and Prompt Injection Concerns

### The Lethal Trifecta

Simon Willison's "Lethal Trifecta" framework identifies the catastrophic risk when three capabilities combine:

1. **Access to private data** — The primary purpose of most MCP tools
2. **Exposure to untrusted content** — Any text/images controlled by an attacker
3. **Ability to exfiltrate data** — HTTP requests, links, API calls

> "If your agent combines these three features, an attacker can easily trick it into accessing your private data and sending it to that attacker."

**Documented Exploits (partial list):**
- Microsoft 365 Copilot (June 2025)
- GitHub's official MCP server (May 2025)
- GitLab Duo Chatbot (May 2025)
- Notion 3.0 AI Agents (September 2025)
- Cursor with Jira MCP (August 2025)

### Tool-Level Prompt Injection

MCP tools have elevated privilege in the prompt hierarchy:

> "Tools, what MCP allows third-parties to provide, are often trusted as part of an assistant's system prompts giving them even more authority to override agent behavior."

**Exploitation vectors include:**
- **Rug pull attacks**: Server can redefine tool names/descriptions dynamically after user confirmation
- **Fourth-party injection**: Trusted MCP server "trusts" data from untrusted sources (e.g., Supabase MCP reading malicious database content)
- **Tool name masquerading**: Bad MCP exposes `write_secure_file()` to hijack legitimate `write_file()` calls

### MCP Colors Framework

Tim Kellogg's security classification system:

- **Red tools**: Expose agent to untrusted (potentially malicious) instructions
- **Blue tools**: Involve critical actions (state changes, exfiltration potential)

**Rule: An agent can have red OR blue tools, but not both.**

> "From a security perspective, [connecting many tools dynamically] is nuts. You're saying you want to release this AI agent thing, and you're not sure how you want to use it??"

### OAuth Implementation Chaos

The initial MCP spec deliberately omitted authentication. The subsequent OAuth implementation has been problematic:

> "The updated MCP OAuth spec is a mess" — Christian Posta

MCP requires OAuth dynamic client registration (RFC 7591), which "practically nobody actually implemented prior to MCP."

---

## 5. Real-World Practitioner Pain Points

### Tool Discovery Failures

Users expect semantic search across integrated data. Reality is different:

> "They asked 'find the FAQ I wrote yesterday for Bob' and while the agent ran several `list_files()`, none of the file titles had 'bob' or 'faq' in the name so it said the file doesn't exist."

MCP tools rarely implement sophisticated search—they expose raw CRUD operations that can't handle fuzzy user intent.

### Context Window Exhaustion

> "They asked 'how many times have I said AI in docs I've written' and after around 30 `read_file()` operations the agent gives up as it nears its full context window."

Simple aggregation queries become impossible without specialized tools.

### Dangerous Auto-Confirmation Patterns

> "A user might connect up Google Drive and Substack MCPs to Claude and use it to draft a post on a recent medical experience. Claude, being helpful, autonomously reads relevant lab reports from Google Drive and includes unintended private details in the post."

Users fall into "YOLO mode" auto-confirmation when most tools are harmless, then get burned by irreversible actions.

### Token Billing Surprises

> "Agent developers are starting to feel the heat since a user's service costs can be heavily dependent on the MCP integrations and their token-efficiency."

1MB of output = ~$1 per request containing that data, billed in **every follow-up message**.

### Model Sensitivity Variance

> "Different LLMs have different sensitivities to tool names and descriptions. Claude could work better with MCPs that use `<xml>` tool description encodings and ChatGPT might need markdown ones."

Users blame the application rather than the MCP design or model choice.

---

## 6. What Needs to Change for Production Readiness

### Protocol-Level Improvements

1. **Max result length limits** — Force MCP developers to be mindful of token efficiency
2. **Standardized auth** — Clear, community-managed authentication specification
3. **Tool categorization** — Built-in security classification (red/blue/neutral)
4. **Progressive disclosure** — Standard patterns for lazy-loading tool definitions

### Architecture Pattern: Code Execution + MCP

Anthropic's recommended approach:
1. Generate TypeScript files from MCP tools
2. Agent discovers tools via filesystem navigation
3. Agent writes code to wire tools together
4. Intermediate results stay in execution environment

**Benefits:**
- 98%+ token savings
- Privacy-preserving (PII tokenization)
- State persistence across operations
- Skill accumulation over time

### Simplified MCP Server Design

Instead of exposing 50+ REST-like tools, MCP servers should provide:

```
- download_raw_data(filters...)
- take_sensitive_gated_action(args...)
- execute_code_in_environment_with_state(code...)
```

> "MCP's job isn't to abstract reality for the agent; its job is to manage the auth, networking, and security boundaries and then get out of the way."

### Human-in-the-Loop Guardrails

- Deterministic "block-at-commit" validation hooks
- Color-based tool access policies
- Explicit confirmation for blue (critical action) tools
- User education about data flow

---

## 7. Key Recommendations

### For MCP Server Developers

1. **Minimize tool count** — Fewer, more powerful tools beat many granular ones
2. **Implement result truncation** — Don't return full documents by default
3. **Support search/filter parameters** — Reduce data before it reaches context
4. **Document token costs** — Users need to understand the overhead
5. **Default to secure patterns** — Require explicit confirmation for state changes

### For Agent Builders

1. **Prefer CLI tools** for common integrations (git, gh, curl, etc.)
2. **Cap MCP tool count** — 40 tools maximum, like Cursor
3. **Implement code execution** for MCP orchestration
4. **Use progressive disclosure** — Load tool definitions on-demand
5. **Classify tools by security color** — Never mix red and blue

### For End Users

1. **Understand the Lethal Trifecta** — Avoid combining private data + untrusted content + exfiltration
2. **Don't auto-confirm everything** — Be especially careful with write/delete/send tools
3. **Monitor token usage** — MCP integrations can dramatically increase costs
4. **Fewer tools = better performance** — More integrations often hurts accuracy

---

## Sources and References

1. Anthropic. "Introducing the Model Context Protocol" (November 2024)
2. Anthropic Engineering. "Code Execution with MCP: Building More Efficient Agents" (November 2025)
3. Simon Willison. "The Lethal Trifecta for AI Agents" (June 2025)
4. Simon Willison. Model Context Protocol tag archive (2024-2025)
5. Geoffrey Huntley. "Too Many MCP Servers and LLM Allocations on the Dance Floor" (August 2025)
6. Tim Kellogg. "MCP Colors: Systematically Deal with Prompt Injection Risk" (November 2025)
7. Shrivu Shankar. "How I Use Every Claude Code Feature" (2025)
8. Shrivu Shankar. "Everything Wrong with MCP" (2025)
9. Peter Steinberger. "Just Talk To It—the No-BS Way of Agentic Engineering" (October 2025)
10. Cloudflare Engineering. "Code Mode" (2025)
11. Kenton Varda. MCP OAuth analysis (November 2025)
12. Zenity Labs. "When a Jira Ticket Can Steal Your Secrets" (August 2025)

---

## About This Report

This report was compiled through comprehensive web research of technical blogs, documentation, GitHub discussions, and practitioner experiences. The findings represent the state of MCP understanding as of January 2026, including insights from major contributors like Simon Willison, Anthropic's engineering team, and production users building agentic systems.

*Note: Originally intended as OpenAI/ChatGPT deep research, conducted via multi-source web synthesis due to authentication constraints.*
