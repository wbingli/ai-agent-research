# MCP Roadmap & "2.0" Status Report

*Research Date: January 31, 2026*

---

## Key Finding: There Is No "MCP 2.0"

**MCP uses date-based versioning, not semantic versioning.** There is no planned "MCP 2.0" — instead, the protocol evolves through incremental spec releases:

| Version | Release Date | Key Changes |
|---------|--------------|-------------|
| 2024-11-05 | Nov 2024 | Initial release |
| 2025-03-26 | Mar 2025 | Streamable HTTP transport, OAuth 2.1 |
| 2025-06-18 | Jun 2025 | Structured tool output, elicitation, **JSON-RPC batching REMOVED** |
| **2025-11-25** | Nov 2025 | **Current stable** — Tasks (async), icons, tool calling in sampling |
| draft | Ongoing | Minor: extensions field for optional capabilities |

---

## Current Stable Version: 2025-11-25

Released November 25, 2025. Key additions:

### Major Features
- **Tasks (Experimental)** — Async operations with polling and deferred results
- **Icons** — Metadata for tools, resources, prompts
- **Tool calling in sampling** — `tools` and `toolChoice` parameters
- **Enhanced OAuth** — OpenID Connect Discovery, incremental scope consent
- **URL mode elicitation** — Servers can request URLs from users

### Governance Changes
- Formal governance model established
- SEP (Specification Enhancement Proposal) process
- Working Groups and Interest Groups
- SDK tiering system

---

## Official Roadmap (Next Release)

The MCP team announced priorities for their **next release** (no date announced yet):

### 1. Asynchronous Operations
**Status:** In progress ([SEP-1686](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1686))

> "Currently, MCP is built around mostly synchronous operations. We're adding async support to allow servers to kick off long-running tasks while clients can check back later for results."

**Note:** The experimental "Tasks" feature in 2025-11-25 is the foundation for this.

### 2. Statelessness and Scalability
**Status:** In progress ([SEP-1442](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1442))

> "As organizations deploy MCP servers at enterprise scale... Current implementations often need to remember things between requests, which makes horizontal scaling across multiple server instances challenging."

Focus: Improving Streamable HTTP, smoothing server startup and session handling.

### 3. Server Identity (.well-known URLs)
**Status:** In design

> "Today, if you want to know what an MCP server can do, you have to connect to it first."

Plan: Servers advertise capabilities via `.well-known` URLs for pre-connection discovery.

### 4. Official Extensions
**Status:** In design

Curating proven patterns for specific industries (healthcare, finance, education) that don't belong in core spec.

### 5. SDK Support Standardization
**Status:** In progress

Clear tiering system for SDKs based on:
- Specification compliance speed
- Maintenance responsiveness
- Feature completeness

### 6. MCP Registry GA
**Status:** Preview → General Availability

The [MCP Registry](https://github.com/modelcontextprotocol/registry) launched preview September 2025, progressing toward GA.

---

## What's NOT on the Roadmap

**Critical gap:** Many pitfalls identified in our research are **not being addressed**:

| Pitfall | On Roadmap? | Notes |
|---------|-------------|-------|
| Context window overhead | ❌ No | No lazy loading, no compression |
| JSON-RPC batching | ❌ **Removed** | Actually removed in June 2025 spec |
| Security model (prompt injection) | ⚠️ Partial | Security best practices doc, but no fundamental changes |
| Code execution primitive | ❌ No | Anthropic recommends it but not in spec |
| Workflow orchestration | ⚠️ Partial | Tasks helps but no state machines |
| Small model compatibility | ❌ No | No simplified schemas |
| Tool description signing | ❌ No | No trust/verification model |

### The Batching Situation

**Shocking finding:** MCP **removed** JSON-RPC batching support in June 2025:

> "Remove support for JSON-RPC batching" — [PR #416](https://github.com/modelcontextprotocol/specification/pull/416)

This goes against the recommendation in our pitfalls research. The protocol is moving **away** from batching, not toward it.

---

## Timeline

| Date | Event |
|------|-------|
| Nov 2024 | MCP initial release |
| Mar 2025 | 2025-03-26 spec (Streamable HTTP, OAuth) |
| Jun 2025 | 2025-06-18 spec (Elicitation, **batching removed**) |
| Sep 2025 | Governance model, Working Groups, Registry preview |
| Nov 2025 | 2025-11-25 spec (Tasks, current stable) |
| TBD | Next release (async ops, scalability, server identity) |

**No announced date for next release.** The November 2025 release originally had a November 11th RC that slipped to November 14th.

---

## Working Groups

Active working groups driving development:

| Group | Focus |
|-------|-------|
| Agents Working Group | Async operations |
| Transport Working Group | Statelessness, scalability |
| Client Implementors | Client-side experience |

---

## What Would "MCP 2.0" Need?

Based on our pitfalls research, a hypothetical major version bump would need:

### Must Have
1. **Lazy tool loading** — On-demand, not upfront
2. **Batching support** — Bring back JSON-RPC batching or equivalent
3. **Security model overhaul** — Tool signing, sandboxing, information flow control
4. **Code execution primitive** — First-class support for agent-written code

### Should Have
5. **Workflow primitives** — State machines, checkpointing, parallelism
6. **Result streaming with compression**
7. **Small model profiles** — Simplified schemas
8. **Conformance test suite**

### The Reality
The MCP team is focused on incremental improvements, not a fundamental redesign. The current roadmap addresses **scalability** but not **efficiency** (context overhead) or **security** (prompt injection).

---

## Community Sentiment

From the [Latent Space podcast](https://www.latent.space/p/mcp) with MCP creators:

> "MCP has now overtaken OpenAPI in GitHub stars... but OpenAPI still has: better tooling, more mature ecosystem, formal specification process"

The MCP team is responsive to feedback but constrained by:
- Backwards compatibility concerns
- Need to support existing ecosystem
- Limited core maintainer bandwidth

---

## Conclusion

**There is no "MCP 2.0" planned.** The protocol evolves through date-versioned releases with incremental changes.

**Current focus:**
- ✅ Async operations (Tasks)
- ✅ Enterprise scalability
- ✅ Server discovery
- ✅ SDK quality

**Not being addressed:**
- ❌ Context window efficiency
- ❌ Batching (actually removed)
- ❌ Fundamental security model
- ❌ Code execution
- ❌ Small model support

For practitioners concerned about the pitfalls we identified, **the roadmap does not provide relief**. The recommended approach remains:
- Use CLIs where possible
- Implement code execution yourself
- Cap tool count
- Wait and see if community pressure drives change

---

## Sources

1. [MCP Roadmap](https://modelcontextprotocol.io/development/roadmap)
2. [Update on the Next MCP Protocol Release](https://blog.modelcontextprotocol.io/posts/2025-09-26-mcp-next-version-update/) (Sep 2025)
3. [Specification 2025-11-25 Changelog](https://modelcontextprotocol.io/specification/2025-11-25/changelog)
4. [Specification 2025-06-18 Changelog](https://modelcontextprotocol.io/specification/2025-06-18/changelog)
5. [Draft Specification Changelog](https://modelcontextprotocol.io/specification/draft/changelog)
6. GitHub Issues: SEP-1686 (Async), SEP-1442 (Statelessness)

---

*Report compiled by Clawdbot for Wenbing Li's AI Agent Research*
