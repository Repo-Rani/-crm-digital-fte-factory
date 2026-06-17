# Research & Technical Decisions: Customer Success AI Agent (Phase 1)

This document outlines the research findings and key technical decisions made during the Incubation Phase of the Customer Success AI Agent.

## Decision 1: Sentiment Analysis Strategy
**Decision**: Use a keyword-based scoring algorithm with contextual modifiers (CAPS lock, punctuation, emoji).
**Rationale**: High-complexity NLP models (like Transformers) are out of scope for a 16-hour prototype. Keyword matching provides transparent, predictable results that are easy to debug and tune for the 60 sample tickets.
**Alternatives Considered**: 
- External sentiment APIs (Rejected: Adds dependency and latency).
- Pre-trained NLTK/VADER (Rejected: Keyword-based is simpler to implement from scratch for this specific domain).

## Decision 2: Knowledge Base Search Implementation
**Decision**: Simple text search using keyword relevance score per section.
**Rationale**: The `product-docs.md` is relatively small (1,750 words). Splitting by headings and calculating a relevance score (matches / query length) is efficient enough for sub-second responses without needing vector search (pgvector), which is reserved for Phase 2.
**Alternatives Considered**:
- Full-text search (FTS) in a database (Rejected: No database in Phase 1).
- Vector embeddings (Rejected: Phase 2 scope).

## Decision 3: MCP Server Integration
**Decision**: Use the `mcp` Python SDK to implement a local server exposing 7 tools.
**Rationale**: The Model Context Protocol (MCP) is the standard for extending AI capabilities. The Python SDK allows for seamless integration with the `CustomerSuccessAgent` class.
**Alternatives Considered**:
- Custom REST API (Rejected: MCP provides a more standardized way for "Claude Code" or other agents to interact with the prototype).

## Decision 4: Channel Simulation
**Decision**: Implement simulated handlers that transform `sample-tickets.json` entries into raw-style dicts.
**Rationale**: Simulating real API payloads (Gmail Message objects, Twilio Webhook payloads) ensures that the core agent loop handles "dirty" data correctly from the start, simplifying the transition to real APIs in Phase 2.
**Alternatives Considered**:
- Passing clean objects directly to the agent (Rejected: Doesn't test the `normalize_message` logic).

## Decision 5: Memory and State
**Decision**: In-memory `dict` stored within a `ConversationMemory` class.
**Rationale**: Meets the prototype requirement for speed and simplicity. Persistence across sessions is not required for Phase 1.
**Alternatives Considered**:
- SQLite (Rejected: Adds unnecessary file I/O complexity for a single-pass incubation phase).
