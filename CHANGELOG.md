# Changelog

This changelog tracks substantive changes to the AX drafts.\
Editorial changes, formatting updates, and example additions are not individually listed.

## v0.1 [draft-agent-discovery-00] — December 2025
- Initial public draft of Agent Discovery Exchange (AX)

## v0.2 [draft-agent-discovery-01] — January 2026

### Added
- Introduced **capability hashing** to enable deterministic change detection of an agent’s capability surface.
- Defined canonicalization and hashing semantics for capability comparison and caching.

### Unchanged
- **No changes to AX discovery semantics.**
- Discovery mechanism, document location, and protocol advertisement remain identical to draft-agent-discovery-00.

### Notes
- Capability hashing is explicitly scoped to change detection only.
- Trust, attestation, signing, and authorization remain out of scope and are deferred to future drafts.

## [Draft-00] — 05 January 2026

### Clarified
- Discovery mechanism is based solely on HTTPS retrieval from a `.well-known` path in alignment with RFC 8615.
- AX does not define registries, trust models, authorization, or execution semantics.

### Not Changed
- Scope of the specification.
- Intended role of AX as discovery-only infrastructure.

## [Draft-01] — 05 January 2026

### Added
- Capability hashing to enable efficient detection of changes in advertised agent capabilities.
- Explicit clarification that AX discovery is non-authoritative and does not imply trust, endorsement, or availability.

### Clarified
- HTTPS `.well-known/agent-exchange` is the only required discovery mechanism.
- DNS-based indirection and federation are explicitly deferred to future drafts or optional extensions.
- AX is registry-agnostic and intended as a pre-registration discovery layer for registries, exchanges, and coordination systems.

### Not Changed
- Discovery semantics and retrieval behavior.
- Separation between discovery, governance, and execution.

## v0.3 [draft-agent-discovery-02] — 20 January 2026

### Added

 - Optional trust tier declarations as non-authoritative discovery metadata
 - Attestation statements for expressing provenance and verification signals
 - Explicit support for multiple, independent attestation authorities
 - Clear layering clarification separating discovery, trust signaling, and execution governance
 - Consumer guidance on interpreting trust signals as advisory inputs only
 - Illustrative (non-normative) trust and attestation example

### Clarified

 - Trust signals do not imply authorization, approval, or endorsement
 - AX remains registry-agnostic and execution-neutral
 - Attestation mechanisms and formats are intentionally unconstrained

### Deferred

 - Agent-to-agent relationship semantics and reputation propagation
 - Federation scoring models and trust graph construction
 - Execution-time policy enforcement and approval workflows

### No Change

 - Core discovery mechanism and AX document structure
 - Protocol-agnostic positioning (MCP, A2A, REST, GraphQL)
 - Backward compatibility with Draft-00 and Draft-01