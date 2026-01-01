# Changelog

All notable changes to the Agent Discovery Exchange (AX) specification are documented in this file.

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

