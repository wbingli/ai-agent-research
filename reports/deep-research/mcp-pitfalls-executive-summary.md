# MCP Pitfalls: Executive Summary

*Synthesized from Claude, Gemini, OpenAI, and Grok research reports*  
*January 31, 2026*

---

## The Bottom Line

**MCP solves interoperability but is fundamentally flawed for production agents.**

The Model Context Protocol has achieved rapid adoption as the standard for AI-tool integration. However, our multi-source research reveals critical problems that the industry has not adequately addressed. For many use cases, **CLI tools outperform MCP** with zero token overhead.

---

## Critical Findings

### 1. 🔥 Context Window Tax is Brutal

| MCP Server | Token Cost |
|------------|------------|
| GitHub MCP (93 tools) | **55,000 tokens** |
| Multiple servers combined | 100,000+ tokens |
| Cursor's enforced limit | 40 tools max |

**Impact:** Before your agent reads a single user message, MCP has consumed 25-50% of available context. Every follow-up message pays this tax again.

> *"Use GitHub's MCP and see 23K tokens gone. Or use the `gh` CLI which has basically the same feature set, models already know how to use it, and pay zero context tax."* — Peter Steinberger

**Verdict:** CLI tools beat MCPs for token efficiency in almost every case.

---

### 2. 🚨 Security is Fundamentally Broken

**The Lethal Trifecta** (Simon Willison):
1. Access to private data ✓
2. Exposure to untrusted content ✓
3. Ability to exfiltrate data ✓

**MCP servers routinely provide all three.**

#### Documented Attacks (Real, Not Theoretical)

| Attack | Target | Method |
|--------|--------|--------|
| Tool Poisoning | Cursor | Malicious instructions hidden in tool descriptions exfiltrate SSH keys |
| Jira Exploit | Cursor + Jira MCP | Encoded prompt injection via support ticket steals AWS credentials |
| WhatsApp Exploit | WhatsApp MCP | Full chat history exfiltration via hidden payloads |
| Supabase Attack | Supabase MCP | Reads private tables, inserts data for exfiltration |
| Notion PDF | Notion 3.0 AI | White-on-white text in PDFs triggers data theft |

#### Attack Vectors

- **Tool Poisoning Attacks (TPA):** Malicious instructions in tool descriptions invisible to users
- **MCP Rug Pulls:** Servers change tool descriptions after installation without re-authorization  
- **Tool Shadowing:** Malicious server overrides instructions from trusted servers
- **Fourth-party Injection:** Trusted MCP reads untrusted data containing injections

> *"Breathe deeply and repeat: 'it's impossible to reliably detect prompt injection attacks, and it probably always will be.'"* — Tim Kellogg

**Verdict:** MCP's security model assumes tool descriptions are trustworthy. They're not.

---

### 3. 💸 No Batching = Double Token Waste

Every intermediate result passes through the model context:

```
TOOL CALL: gdrive.getDocument("meeting_transcript")
→ 50,000 tokens loaded into context

TOOL CALL: salesforce.updateRecord(data: [same 50K tokens])
→ Model rewrites entire document AGAIN
```

**Result:** 2x token cost for every data transfer operation.

#### The Fix: Code Execution

Anthropic's own recommendation (which they haven't implemented):

```typescript
// Data flows directly, never enters model context
const transcript = await gdrive.getDocument({ documentId: 'abc123' });
await salesforce.updateRecord({ data: { Notes: transcript } });
```

**Token savings: 98.7%** (Cloudflare "Code Mode" testing)

**Verdict:** MCP should be a gateway for code execution, not a tool-calling API.

---

### 4. 🔧 No Workflow Support

MCP treats each tool call as atomic and isolated. Missing primitives:

| Feature | Status |
|---------|--------|
| Multi-step workflows | ❌ Not supported |
| State machines | ❌ Not supported |
| Checkpointing | ❌ Not supported |
| Rollback/compensation | ❌ Not supported |
| Parallel execution | ❌ Not supported |
| Event subscriptions | ❌ Not supported |
| Tasks (experimental) | ⚠️ Not widely supported |

**Verdict:** Complex agent workflows require external orchestration (LangGraph, etc.).

---

### 5. 📉 Small Models Can't Handle MCP

| Issue | Prevalence |
|-------|------------|
| Tool amnesia (forgetting tools exist) | ~67% failure rate (Qwen3-4B) |
| Tool hallucination (inventing tools) | Common |
| Format errors (invalid JSON) | Common |
| Selection errors (wrong tools) | Common |

**Verdict:** MCP is effectively a large-model protocol. Small/local models need fine-tuning or reduced tool sets.

---

### 6. 🔄 Spec Still in Flux

- HTTP+SSE transport → Streamable HTTP (breaking change)
- OAuth dynamic client registration (RFC 7591) — "practically nobody implemented this before MCP"
- Resources/Prompts primitives often unsupported by clients
- No conformance test suite
- Different clients implement different subsets

**Verdict:** Wait for stabilization before production deployment.

---

## When to Use MCP

✅ **Good use cases:**
- Browser automation (Playwright MCP) — no CLI equivalent
- OAuth-protected remote services requiring secure auth gateway
- When no CLI alternative exists

❌ **Prefer alternatives when:**
- CLI tool exists (gh, git, aws-cli, curl)
- Token budget is constrained
- Security requirements are strict
- Need transactional guarantees
- Simple CRUD operations suffice

---

## The Practitioner Consensus

> *"IMO most MCPs are something for the marketing department to make a checkbox. Almost all MCPs really should be CLIs."* — Peter Steinberger (built 5 MCPs)

> *"Instead of a bloated API, an MCP should be a simple, secure gateway that provides a few powerful, high-level tools... then get out of the way."* — Shrivu Shankar

> *"MCP's job isn't to abstract reality for the agent; its job is to manage the auth, networking, and security boundaries."* — Multiple sources

---

## Recommendations for MCP 2.0

1. **Lazy tool loading** — Load definitions on-demand, not upfront
2. **Code execution primitive** — Let agents write code to chain tools
3. **Security framework** — Tool signing, version pinning, sandboxing
4. **Batching support** — Native multi-call operations
5. **Workflow primitives** — State machines, checkpointing, parallelism
6. **Small model profiles** — Simplified schemas for constrained contexts
7. **Result streaming with compression** — Reduce context overhead
8. **Conformance test suite** — Ensure client/server compatibility

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| GitHub MCP token cost | 55,000 tokens | Huntley |
| Cursor tool limit | 40 tools max | Cursor |
| Code execution token savings | 98.7% | Cloudflare |
| Small model MCP success rate | ~33% | Reddit r/LocalLLaMA |
| Documented real-world exploits | 5+ | Multiple security researchers |

---

## Sources

All four research reports synthesized:
- `claude-mcp-pitfalls-analysis.md` — First-principles technical analysis
- `gemini-mcp-pitfalls-report.md` — Huntley, Steinberger, Willison, Kellogg research
- `grok-mcp-pitfalls-report.md` — Invariant Labs security research, attack demos
- `openai-mcp-pitfalls-report.md` — Practitioner pain points, code execution patterns

**Primary sources cited across reports:**
- Geoffrey Huntley — Token allocation analysis
- Simon Willison — Security research, Lethal Trifecta framework
- Tim Kellogg — MCP Colors security classification
- Peter Steinberger — Practitioner insights, CLI advocacy
- Invariant Labs — Tool Poisoning, Rug Pull, Shadowing attacks
- Anthropic Engineering — Code execution recommendations
- Zenity Labs — Jira/Cursor attack demonstration
- Shrivu Shankar — "Everything Wrong with MCP"

---

## Conclusion

MCP is a **useful standard for simple integrations** but **not production-ready for complex agentic systems**. The protocol's context overhead, security vulnerabilities, and workflow limitations require significant workarounds.

**For serious agent builders:**
- Use CLIs where possible (zero token cost)
- Implement code execution for MCP orchestration
- Classify tools by security color (never mix red and blue)
- Cap tool count at 40
- Wait for spec stabilization

The path forward likely involves either MCP 2.0 with fundamental changes, or complementary protocols that address these gaps.

---

*Executive summary compiled by Clawdbot for Wenbing Li's AI Agent Research*
