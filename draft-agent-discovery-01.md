```
Internet-Draft                                              A. Sempf
Intended status: Informational                          January 2026
Expires: July 2026
```
# Agent Discovery Exchange (AX)

## Status of This Memo

This Internet-Draft is submitted as an informational document. It represents work in progress and may be updated, replaced, or obsoleted at any time.

## Abstract

Agent Discovery Exchange (AX) defines a lightweight, internet-native mechanism for discovering autonomous agents and exchanging machine-readable metadata about their capabilities and supported interaction protocols. This document extends draft-agent-discovery-00 by introducing capability hashing, enabling deterministic change detection of an agent’s functional surface while preserving forward compatibility and separation of concerns.

AX is intentionally limited to discovery and metadata exchange. It does not define execution semantics, trust enforcement, authorization, or economic models, and is designed to complement existing agent execution and interaction protocols.

## Terminology

In addition to RFC 2119 terminology:

 - **Capability Hash**: A deterministic cryptographic digest representing the declared functional surface of an agent.
 - **Capability Surface**: The subset of an AX document that materially affects how a consumer
  would interact with an agent.
 - **AX Consumer**: An agent or system that retrieves and evaluates an AX document.
 - **AX Producer**: An agent or system that publishes an AX document.

## Motivation

As agent ecosystems grow, static integrations do not scale. AX enables:

- Dynamic agent federation
- Safe capability comparison
- Protocol negotiation without tight coupling
- Policy-aware arbitration decisions

## Design Goals (Updated)

AX is designed to:

1. Enable deterministic capability comparison
2. Support policy-driven agent selection
3. Avoid semantic overlap with execution protocols
4. Support incremental evolution without breaking consumers

## Discovery Mechanism (Unchanged)

Agent Discovery Exchange (AX) defines a stable, internet-native discovery mechanism based on HTTPS retrieval of declarative agent metadata from a well-known location.

All requirements in Draft-00 remain applicable.

### Well-Known AX Resource

An AX document MUST be retrievable via HTTPS at:

`https://<domain>/.well-known/agent-exchange`

The resource MUST return a valid AX document encoded as UTF-8 JSON and MUST conform to the AX schema defined in this specification.

### Discovery Independence

Discovery location and discovery semantics are independent of:

 - agent execution protocols
 - trust or governance frameworks
 - registration or onboarding workflows
 - marketplaces or exchanges

AX discovery MUST remain usable as a pre-registration signal for any downstream system.

### Optional Extensions

Future drafts MAY define optional mechanisms for:
 - delegation or indirection
 - federation between discovery consumers
 - trust signaling or attestation references

Such mechanisms MUST NOT be required for basic AX compliance and MUST NOT modify the required .well-known HTTPS discovery path.

### Summary
AX defines a discovery process in which a consumer:

1. Resolves a domain using DNS.
2. Retrieves an AX document from a well-known HTTPS location.
3. Evaluates advertised capabilities and supported interaction
   protocols.
4. Selects an appropriate interaction mechanism.
5. Proceeds to execution using a protocol outside the scope of AX.

AX operates strictly prior to execution and does not participate in
message exchange, workflow orchestration, or task execution.

## Media Type Definition

AX documents MUST be served using the following media type: `application/agent-exchange+json`

### Media Type Parameters

 - version (OPTIONAL): AX document version (e.g., 1.0)

### Encoding Considerations

AX documents MUST be encoded using UTF-8.

### Security Considerations

See Section: Security Considerations.

## Agent Exchange (AX) Document (Revised)
### Required Fields

An AX document MUST include:

 - `record_type`
 - `version`
 - `agent`
 - `endpoints`
 - `capability_hash`

### Capability Hash

The `capability_hash` field provides a cryptographic summary of the agent’s declared capabilities.

## Capability Hashing
### Purpose

Capability hashing enables consumers to efficiently detect changes to an agent’s functional surface. It is intended to support caching, comparison, indexing, and change detection.

Capability hashing is NOT intended to provide:

 - Integrity guarantees
 - Authenticity verification
 - Authorization decisions
 - Trust establishment

Those concerns are explicitly out of scope for this document.

### Capability Hash Stability

Draft-01 introduces capability hashing to enable consumers to detect changes in advertised capabilities without altering discovery semantics.

The AX document MUST include a capability hash computed over the capability representation as defined in Section: Capability Surface.

The presence or change of a capability hash:

 - MUST NOT affect discovery location
 - MUST NOT alter retrieval semantics
 - MUST NOT imply trust, verification, or availability

### Capability Surface

The capability surface consists of AX document fields that materially affect interaction semantics. Only this subset MUST be included when computing a capability hash.

The capability surface SHOULD include:
- Stable agent identifiers
- Supported interaction protocols
- Endpoint definitions
- Declared capabilities
- Schema identifiers and versions

The capability surface MUST NOT include:
- Human-readable descriptions
- Documentation links
- Contact information
- Trust, reputation, or attestation metadata
- Federation or SLA metadata
- Any field that does not affect interaction behavior

The precise definition of the capability surface is normative and MUST be defined by this specification, not inferred from implementation details.

### Canonicalization Rules

Before hashing, the capability surface MUST be canonicalized to ensure deterministic results across implementations.

Canonicalization MUST include:
- Removal of fields outside the capability surface
- Stable key ordering
- Deterministic serialization
- UTF-8 encoding

JSON serialization MUST:
- Use lexicographically sorted object keys
- Omit insignificant whitespace
- Preserve numeric and boolean values exactly

Implementations MUST NOT rely on default language-specific JSON
serialization behavior without enforcing these rules.

### Hash Algorithm

The capability hash MUST be computed using a deterministic cryptographic hash algorithm.

SHA-256 is RECOMMENDED.

The output MUST be represented as a lowercase hexadecimal string.

Future documents MAY define alternative algorithms, but consumers MUST treat differing algorithms as producing non-comparable hashes.

### Change Detection Semantics

A change in the capability hash indicates that the agent’s functional surface has changed in a way that MAY affect interaction.

A change in the AX document that does not affect the capability surface MUST NOT change the capability hash.

Consumers MAY cache capability hashes and use them to:

 - Detect changes efficiently
 - Avoid unnecessary re-evaluation
 - Support indexing and comparison

Consumers MUST NOT treat a matching capability hash as evidence of trust, integrity, or authorization.

## Forward Compatibility Considerations

AX is explicitly designed to evolve.

Consumers MUST ignore unknown fields in AX documents.

Producers MAY add new optional fields without affecting the capability
hash, provided those fields are outside the defined capability surface.

Capability hashing MUST remain stable across:

 - Editorial changes
 - Addition of optional metadata
 - Introduction of future AX extensions

This design allows older consumers to interoperate safely with newer AX documents.

## Security Considerations (Expanded)

AX discovery and capability hashing do not provide security guarantees on their own.

Specific considerations include:

 - Capability hashes do not prevent spoofing or tampering.
 - AX documents may be served over HTTPS but are not inherently trusted.
 - Authorization, authentication, and attestation are out of scope.

Consumers SHOULD apply appropriate policy, validation, and trust mechanisms before executing interactions discovered via AX.

Future documents are expected to address trust, signing, and attestation as separate concerns.

### Threat: Capability Drift

Mitigation:

 - Capability hashing
 - Consumer-side caching and verification

### Threat: Metadata Spoofing

Mitigation:

 - HTTPS transport
 - Optional JWS signatures
 - Issuer validation

### Threat: Protocol Downgrade

Mitigation:

 - Consumer-defined protocol preference ordering
 - Capability hash validation

### Threat: Unauthorized Invocation

Mitigation:

 - AX does not authorize execution
 - All endpoints MUST enforce independent authentication and authorization

## Privacy Considerations

AX documents are intentionally public. Operators SHOULD NOT expose:

 - Internal topology
 - Sensitive operational constraints
 - Tenant-specific entitlements

## Relationship to Execution Protocols

AX is explicitly non-competitive with execution protocols.

AX is complementary to existing interaction and execution protocols, including but not limited to:

 - Agent-to-Agent (A2A)
 - Model Context Protocol (MCP)
 - GraphQL
 - REST

AX enables discovery and protocol selection but does not replace or compete with these mechanisms.

AX MAY advertise support for multiple protocols simultaneously.

## Non-Normative Implementation Guidance

This document defines normative semantics but does not prescribe a specific implementation.

Non-normative examples illustrating canonicalization and capability hashing are provided in the project repository under:

examples/capability-hashing/

These examples are for illustration only and are not required for AX compliance.

## IANA Considerations

This document proposes the registration of the following media type for use with AX documents.

This registration is provisional and subject to change based on implementation experience and community feedback.

```pgsql
Type name: application
Subtype name: agent-exchange+json
Required parameters: none
Optional parameters: version
Encoding considerations: UTF-8
Security considerations: see RFC
```

## References

 - RFC 2119
 - RFC 6838 (Media Type Specifications)
 - RFC 8615 (Well-Known URIs)