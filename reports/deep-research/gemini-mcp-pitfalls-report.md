# MCP (Model Context Protocol) Pitfalls and Limitations

**Research Date:** February 1, 2026  
**Methodology:** Web research synthesis (Gemini Deep Research unavailable - compiled from multiple authoritative sources)

---

## Executive Summary

The Model Context Protocol (MCP) has been widely adopted as a standardized way to connect AI agents to external tools and data sources. However, after analyzing practitioner feedback, security research, and engineering blogs, significant pitfalls emerge that practitioners should consider before adoption. Key concerns include:

1. **Massive context window overhead** from tool definitions
2. **Security vulnerabilities** enabling prompt injection and data exfiltration
3. **No native batching or workflow support**
4. **Configuration complexity** across clients
5. **Performance degradation** compared to CLI alternatives

---

## 1. Context Window Overhead

### The Token Tax Problem

MCP tool definitions consume substantial context window space, reducing the effective tokens available for actual work.

**Key findings from Geoffrey Huntley's analysis:**

- Claude 4's 200K context is reduced to ~176K after system prompts
- **GitHub MCP alone consumes 55,000 tokens** (93 tools) — now improved from initial 50K
- Multiple MCP servers can easily consume 100K+ tokens before any work begins
- Cursor caps MCP tools at 40 specifically to prevent context bloat

> "What the hell? Why would you need 128 tools or why would you want more than that? Why is Microsoft doing this or encouraging this bad practice?" — Cursor engineer, quoted by Geoffrey Huntley

### Impact on Model Performance

From Anthropic's own engineering blog:

> "As the number of connected tools grows, loading all tool definitions upfront and passing intermediate results through the context window slows down agents and increases costs."

**Specific issues:**
- Tool descriptions occupy space before reading any requests
- With thousands of tools: hundreds of thousands of tokens consumed pre-task
- Intermediate results must pass through the model, doubling token usage for data transfers
- 2-hour meeting transcript: ~50,000 additional tokens for copy operations

### The CLI Alternative

Peter Steinberger (prominent practitioner) articulates the core insight:

> "I can just refer to a CLI by name. I don't need any explanation in my agents file. The agent will try $randomcrap on the first call, the CLI will present the help menu, context now has full info how this works and from now on we good. I don't have to pay a price for any tools, unlike MCPs which are a constant cost and garbage in my context."

**CLI advantages:**
- Zero context tax — models already know common CLIs (gh, git, curl)
- Dynamic discovery through `--help`
- Same functionality, dramatically lower overhead

---

## 2. Security Vulnerabilities

### The Lethal Trifecta

Simon Willison's framework identifies three capabilities that, when combined, create critical vulnerabilities:

1. **Access to private data**
2. **Exposure to untrusted content**
3. **Ability to exfiltrate data**

**MCP servers frequently provide all three simultaneously.**

### Real-World Attack Demonstrations

#### Jira/Cursor Attack (Zenity Labs, 2025)
- External attacker sends malicious support email
- Email syncs to Jira via Zendesk integration
- Developer asks Cursor to review Jira ticket
- Encoded prompt injection (using "waffles" instead of "API keys") bypasses safety
- AWS credentials exfiltrated via URL parameter

Cursor's official response:
> "This is a known issue. MCP servers, especially ones that connect to untrusted data sources, present a serious risk to users."

#### Supabase MCP Attack (General Analysis, 2025)
- Single MCP provides all three trifecta capabilities
- Attacker injects instructions in support ticket
- Agent reads private `integration_tokens` table
- Data inserted into `support_messages` for exfiltration
- **Fix:** Use read-only mode (removes exfiltration vector)

#### Notion 3.0 AI Agents (CodeIntegrity, 2025)
- Hidden text in PDFs (white on white) contains injection
- Agent uses web search MCP to exfiltrate to attacker URL
- PDF summary request becomes data theft

#### Atlassian MCP Attack (Cato CTRL, 2025)
- External user submits malicious support ticket
- Internal user invokes MCP-connected AI
- Prompt injection in ticket executes unauthorized actions

### Prompt Injection is Unsolvable

Tim Kellogg's stark assessment:

> "Breathe deeply and repeat after me: 'it's impossible to reliably detect prompt injection attacks, and it probably always will be.'"

### MCP Colors Framework (Mitigation)

Tim Kellogg proposes a color-coding system:

| Color | Meaning | Examples |
|-------|---------|----------|
| **Red** | Untrusted content | Google search, PDFs from prospects, external data |
| **Blue** | Critical actions | Delete email, send to CEO, change permissions |

**Rule: An agent can have red OR blue, but never both.**

However, this requires:
- Labeling every tool and data input
- O(n^m) penetration testing combinations
- Ongoing maintenance as tools evolve

---

## 3. No Batching Support

### The Multi-Tool Problem

MCP has no native mechanism for batching multiple tool calls efficiently.

From Anthropic's engineering analysis:
> "Most MCP clients allow models to directly call MCP tools... Every intermediate result must pass through the model."

**Example inefficiency:**
```
TOOL CALL: gdrive.getDocument(documentId: "abc123")
→ returns full transcript to context

TOOL CALL: salesforce.updateRecord(data: [full transcript again])
→ model rewrites entire document
```

**Token waste:** 2x for every data transfer operation.

### Proposed Solution: Code Execution

Anthropic suggests converting MCP tools to TypeScript functions:

```typescript
const transcript = (await gdrive.getDocument({ documentId: 'abc123' })).content;
await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});
```

**Benefits:**
- Data flows directly, not through model context
- 98.7% token reduction (150K → 2K in their example)
- Model never sees potentially sensitive intermediate data

**Catch:** Anthropic provides no implementation — "left as an exercise for the reader."

---

## 4. Workflow and State Management Limitations

### No Native Workflow Support

MCP is designed for stateless, individual tool calls. Complex workflows require:
- Manual orchestration
- External state management
- Custom error handling

### Tasks Feature (Experimental)

MCP's experimental "Tasks" feature attempts to address this:
> "Durable execution wrappers that enable deferred result retrieval and status tracking for MCP requests"

However, this remains experimental and not widely supported.

### State Persistence Challenges

Practitioners report needing filesystem workarounds:

```typescript
// Save state manually
await fs.writeFile('./workspace/leads.csv', csvData);

// Later execution picks up
const saved = await fs.readFile('./workspace/leads.csv', 'utf-8');
```

---

## 5. Configuration Complexity

### Cross-Client Inconsistency

Each AI client implements MCP differently:
- **Claude Desktop:** Specific JSON configuration format
- **Cursor:** 40-tool limit, custom ignore files
- **VS Code:** Recently removed 128-tool limit (criticized by practitioners)
- **Different models:** Require different prompting styles

Peter Steinberger's experience:
> "I have an Agents.md file with a symlink to claude.md, since Anthropic decided not to standardize. I recognize that this is difficult and sub-optimal, since GPT-5 prefers quite different prompting than Claude."

### Tool Discovery Problems

From Shrivu Shankar (Claude Code power user):
> "Instead of a bloated API, an MCP should be a simple, secure gateway that provides a few powerful, high-level tools... In this model, MCP's job isn't to abstract reality for the agent; its job is to manage the auth, networking, and security boundaries and then get out of the way."

---

## 6. Real-World Practitioner Feedback

### "MCPs Are Marketing"

Peter Steinberger (built 5 MCPs himself):
> "IMO most are something for the marketing department to make a checkbox and be proud. Almost all MCPs really should be CLIs."

### Limited Remaining Use Cases

Shrivu Shankar on focused MCP usage:
- `download_raw_data(filters...)`
- `take_sensitive_gated_action(args...)`
- `execute_code_in_environment_with_state(code...)`

> "MCP's job isn't to abstract reality for the agent; its job is to manage the auth, networking, and security boundaries."

### The Playwright Exception

Most practitioners agree on one useful MCP:
> "I do use chrome-devtools-mcp these days to close the loop. It replaced Playwright as my to-go MCP for web debugging." — Peter Steinberger

Browser automation remains a legitimate MCP use case because:
- No CLI equivalent provides the same interactivity
- Security boundary is clearer (local browser)
- Session state matters

---

## 7. The Dynamic API Argument (Counter-Point)

Steve Krouse offers a contrarian view:
> "Normal APIs are promises to developers... But MCP servers are called by LLMs which dynamically read the spec every time... The LLM can figure it out afresh every time."

This suggests MCP servers can iterate faster than traditional APIs. However, this doesn't address:
- Token consumption
- Security concerns
- Performance overhead

---

## 8. Recommendations

### When to Use MCP

✅ **Good use cases:**
- Browser automation (Playwright MCP)
- OAuth-protected remote services requiring dynamic client registration
- Secure gateways where auth/networking justifies overhead
- When no CLI alternative exists

### When to Avoid MCP

❌ **Prefer alternatives when:**
- CLI tool exists (gh, git, aws-cli, curl)
- Token budget is constrained
- Security requirements are strict
- Simple CRUD operations suffice

### Security Hardening

1. **Classify tools** using color framework (red/blue)
2. **Never combine** untrusted input tools with critical action tools
3. **Use read-only mode** where possible (Supabase example)
4. **Disable auto-run** in development environments
5. **Implement .cursorignore** or equivalent for sensitive files
6. **Monitor agent behavior** for anomalous actions

### Token Optimization

1. **Progressive disclosure:** Load tool definitions on-demand via filesystem navigation
2. **Implement code execution:** Let agents write code to chain tools
3. **Filter before returning:** Transform results in execution environment
4. **Limit tool count:** Follow Cursor's 40-tool limit guidance
5. **Prefer CLIs:** Zero context tax for common operations

---

## Sources

1. Geoffrey Huntley - "Too many model context protocol servers and LLM allocations on the dance floor" (August 2025)
2. Anthropic Engineering - "Code execution with MCP: building more efficient AI agents" (November 2025)
3. Peter Steinberger - "Just Talk To It - the no-bs Way of Agentic Engineering" (October 2025)
4. Tim Kellogg - "MCP Colors: Systematically deal with prompt injection risk" (November 2025)
5. Zenity Labs - "AgentFlayer: When a Jira Ticket Can Steal Your Secrets" (June-August 2025)
6. Simon Willison - Multiple posts on model-context-protocol (2024-2025)
7. General Analysis - "Supabase MCP can leak your entire SQL database" (July 2025)
8. Shrivu Shankar - "How I Use Every Claude Code Feature" (November 2025)
9. Anthropic Official - Model Context Protocol documentation
10. CodeIntegrity - "The Hidden Risk in Notion 3.0 AI Agents" (September 2025)

---

## Conclusion

MCP represents an important step toward standardizing AI agent integrations. However, the current implementation has significant drawbacks:

1. **Token overhead** makes it impractical for token-constrained contexts
2. **Security model** is fundamentally vulnerable to prompt injection
3. **No batching** leads to inefficient multi-tool workflows
4. **CLIs outperform** MCPs for most common operations

The protocol may evolve to address these issues, but practitioners should approach MCP adoption with clear awareness of these trade-offs. For many use cases, traditional CLI tools and custom scripts remain superior choices.

---

*Report compiled from web research. Originally planned as Gemini Deep Research but executed via manual source synthesis due to authentication constraints.*
