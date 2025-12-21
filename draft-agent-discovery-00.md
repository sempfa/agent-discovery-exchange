Internet-Draft                                              A. Sempf
Intended status: Informational                          December 2025
Expires: June 2026

# Agent Discovery Exchange (AX)

## Status of This Memo

This Internet-Draft is submitted as an informational document. It represents work in progress and may be updated, replaced, or obsoleted at any time. Distribution of this memo is unlimited.

## Abstract

Autonomous AI agents increasingly operate across organizational and administrative boundaries. However, there is no standardized, internet-native mechanism for discovering agent endpoints, understanding their capabilities, or negotiating supported interaction protocols.

This document defines Agent Discovery Exchange (AX), a lightweight, protocol-agnostic discovery mechanism that enables agents to advertise their capabilities and supported interaction protocols using existing DNS and HTTPS infrastructure. AX is designed to complement — not replace — existing agent execution and communication protocols such as GraphQL, MCP, A2A, and REST.

## Terminology

The key words MUST, MUST NOT, REQUIRED, SHALL, SHOULD, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119.

**Agent**: An autonomous or semi-autonomous software entity capable of executing tasks or workflows.

**AX Document**: A machine-readable JSON document describing an agent’s capabilities and supported interaction protocols.

**Discovery Domain**: A DNS domain used to locate an AX document.

**Protocol Descriptor**: A structured description of how an agent may be invoked using a specific protocol.

## Motivation

Current agent interoperability relies on out-of-band configuration, proprietary registries, or hard-coded integrations. These approaches do not scale across organizations and prevent dynamic federation of agents.

AX addresses the following needs:

- Public discovery of agent capabilities
- Protocol negotiation without prior coordination
- Decoupling discovery from execution
- Internet-native operation without new DNS record types

## Problem Statement

There is no standardized way for an agent to answer:

- Where are you reachable?
- What can you do?
- How should I talk to you?
- What security model do you require?

Without such a mechanism, agent ecosystems fragment and interoperability remains manual.

## Design Goals

AX is designed to be:

1. Protocol-agnostic
2. Standards-aligned
3. Incrementally deployable
4. Secure by declaration
5. Extensible without coordination
6. Non-invasive to DNS

## Non-Goals

- This specification does NOT:
- Define agent execution semantics
- Mandate a single communication protocol
- Define authentication or authorization mechanisms
- Require centralized registries
- Replace existing API specifications

## Architecture Overview

AX separates concerns as follows:
- **DNS**: Used only for locating an AX document
- **HTTPS**: Used for retrieving structured metadata
- **Execution Protocols**: Used independently for task invocation

## Discovery Mechanism

Agents publish Agent Exchange (AX) documents using existing DNS and HTTPS infrastructure.

To prevent namespace collisions and ensure consistent discovery semantics, AX documents SHOULD be published using the well-known URI mechanism defined in RFC 8615.

The default discovery location is:

`https://_agent.<domain>/.well-known/agent-exchange.json`


The .well-known URI path provides a standardized, server-wide location for machine-readable metadata and site-wide services, and avoids conflicts with application-specific URL namespaces.

Agents MAY additionally expose AX documents at other HTTPS locations; however, AX consumers SHOULD attempt discovery via the .well-known location first.

AX explicitly does not define discovery via custom DNS resource record types.

## Agent Exchange (AX) Document

An AX document is a JSON object that describes an agent and the protocols by which it may be invoked. AX documents are discovery metadata and MUST NOT be interpreted as authorization grants.

### Required Fields

AX documents MUST include:

- `record_type`: MUST be "AX"
- `version`: AX document version identifier (e.g., "1.0")
- `agent`: object describing the agent identity
- `endpoints`: array of protocol descriptors (see Section X)

The agent object MUST include:
- `name`: human-readable name
- `description`: short capability description

### Optional Fields

AX documents MAY include:

- `capabilities`: structured, machine-readable capability hints (e.g., intents)
- `schema`: references to machine-readable schemas/manifests (GraphQL schema URL, MCP manifest URL, etc.)
- `limits`: operational constraints (rate limits, max concurrency), if the operator is willing to disclose
- `security`: issuer, signature reference, and/or key discovery pointers
- `extensions`: namespaced vendor-specific extensions

Consumers MUST ignore unknown fields to preserve forward compatibility.

### Supported Protocol Advertisement

The endpoints field advertises the interaction protocols supported by the agent. It enables protocol negotiation without requiring prior out-of-band coordination. AX does not define the semantics of any advertised protocol.

Each endpoint entry in endpoints MUST include:

- `protocol`: identifier of the protocol (e.g., graphql, mcp, a2a, rest)
- `url`: invocation endpoint URL

Each endpoint entry SHOULD include:

- `auth`: supported authentication mechanisms (e.g., AWS_IAM, OIDC, OAuth2, mTLS)
- `content_type`: expected request content type where applicable

Consumer selection:

- AX consumers SHOULD select the “best available” protocol based on local policy, required interaction mode (sync/async), and security posture.
- If multiple endpoints match, consumers MAY prefer those with stronger authentication requirements or higher trust posture (if present).

Note: Advertising a protocol does not imply that all intents/capabilities are available via all protocols.

### Example AX document 

```json
{
  "record_type": "AX",
  "version": "1.0",
  "agent": {
    "name": "Example Arbiter",
    "description": "Intent-based workflow arbiter coordinating internal and external agents",
    "provider": "Example"
  },
  "endpoints": [
    {
      "protocol": "graphql",
      "url": "https://abc123.appsync-api.ap-southeast-2.amazonaws.com/graphql",
      "auth": ["AWS_IAM", "OIDC"]
    },
    {
      "protocol": "mcp",
      "url": "https://mcp.example.com",
      "auth": ["OIDC"]
    },
    {
      "protocol": "a2a",
      "url": "https://agents.example.com/a2a",
      "auth": ["JWT"]
    },
    {
      "protocol": "rest",
      "url": "https://api.example.com/agents/tasks",
      "auth": ["OAuth2"]
    }
],
  "capabilities": {
    "intents": [
      "multi_agent_planning",
      "document_analysis",
      "tool_execution"
    ],
    "async": true,
    "supports_callbacks": true
  },
  "schema": {
    "graphql_schema_url": "https://_agent.example.com/schema.graphql",
    "mcp_manifest_url": "https://_agent.example.com/mcp.json"
  },
  "security": {
    "issuer": "https://example.com",
    "metadata_signature": "jws"
  }
}
```

## Security Considerations

AX introduces the following threat surfaces:

**Metadata Spoofing**

- AX documents SHOULD be cryptographically signed (e.g., JWS).
- Consumers SHOULD validate issuer identity.

**Capability Forgery**

- AX documents describe intent; authorization MUST be enforced at execution time.

**Replay and Downgrade Attacks**

- AX documents SHOULD be versioned and cache-controlled.
- Protocol selection SHOULD prefer stronger security models.

**Callback Abuse**

- Callback mechanisms MUST require explicit opt-in.
- Payloads SHOULD be signed and replay-protected.

AX does not bypass authentication, authorization, or rate limiting enforced by execution endpoints.

## Privacy Considerations

AX documents are public by design.

Operators SHOULD avoid exposing:

- Sensitive internal topology
- Private agent identities
- Credentials or secrets

## Extensibility

AX documents MAY include an extensions object.

Extensions MUST:

- Be namespaced
- NOT alter base semantics

## Backward Compatibility

AX documents MUST be forward-compatible.

Unknown fields MUST be ignored by consumers.

## IANA Considerations

This specification does not require any IANA actions.

## References

- RFC 2119 (Key words for use in RFCs)
- RFC 8615 (Well-Known URIs)
- DNS RFCs

## Appendix A. Threat Modeling Summary (Non-Normative)

| Threat                | Mitigation                          |
| --------------------- | ----------------------------------- |
| Metadata spoofing     | HTTPS + signed AX documents         |
| Capability over-claim | Enforcement at execution layer      |
| Downgrade attacks     | Protocol preference rules           |
| Callback injection    | Signed callbacks + allowlists       |
| Enumeration abuse     | Rate limiting on discovery endpoint |
