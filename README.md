# Agent Discovery Exchange (AX)

Agent Discovery Exchange (AX) is an **open, internet-native discovery protocol** that enables AI agents to advertise their capabilities and supported interaction protocols in a standardized, machine-readable format using existing HTTPS infrastructure.

AX is intentionally scoped to **discovery only**. It does **not** define execution semantics, trust models, governance workflows, or economic mechanisms. Instead, AX provides a **shared discovery substrate** that registries, exchanges, marketplaces, and coordination layers can consume **prior to registration, onboarding, trust evaluation, or execution decisions**.

By decoupling discovery from coordination, AX enables agent ecosystems to scale openly while allowing downstream systems to differentiate on trust, governance, policy, and execution.

AX is being developed as an **open, vendor-neutral standard** and is developed as an **Internet-Draft** standard to maximize visiblity and global adoption.


## Table of Contents

* [Overview](#agent-discovery-exchange-ax)
* [Design Principles](#design-principles)
* [How AX Works](#how-ax-works)

  * [What AX Is](#what-ax-is)
  * [What AX Is Not](#what-ax-is-not)
  * [AX in the Agent Stack](#ax-in-the-agent-stack)
* [Specifications & Drafts](#specifications--drafts)
* [Conformance](#conformance)
* [Examples](#examples)

  * [Minimal AX Document](#minimal-ax-document)
  * [Agent Advertising Multiple Protocols](#agent-advertising-multiple-protocols)
  * [Capability Hashing Example](#capability-hashing-example)
  * [Publishing an AX Document](#publishing-an-ax-document)
  * [Consuming AX as a Registry or Indexer](#consuming-ax-as-a-registry-or-indexer)
* [Example Use Cases](#example-use-cases)
* [Related Resources](#related-resources)
* [Status](#status)
* [Getting Started](#getting-started)
* [Implementations](#implementations)
* [Contributing](#contributing)
* [License](#license)

## Design Principles

AX is guided by a small set of principles:

 - Discovery before execution
 - Decentralisation over registries
 - Declaration over assumption
 - Policy at the edge
 - Evolution over finality

These principles are reflected in both the specification and its release process.


## How AX Works

Agents publish a discovery document at a **well-known HTTPS location** under a domain they control:

```
https://<domain>/.well-known/agent-exchange
```

The AX document:

* describes the agent’s capabilities,
* lists supported interaction protocols,
* includes optional descriptive metadata,
* and may include capability hashes for change detection.

AX documents are:

* retrieved over HTTPS,
* accessible without authentication,
* suitable for crawling, indexing, and caching.

AX discovery is **non-authoritative**. Publishing an AX document does not imply trust, endorsement, availability, pricing, or authorization to invoke the agent.

### What AX Is

 - A discovery and metadata exchange mechanism
 - Protocol-agnostic
 - Execution-neutral
 - Built on existing internet standards (DNS, HTTPS, .well-known)
 - Designed for incremental adoption

At its core, AX allows an agent to publish a machine-readable document that answers:
```
Who am I?
What can I do?
How can you interact with me?
Under what constraints and trust assumptions?
```
### What AX Is Not

AX explicitly does not:

 - Define agent execution semantics
 - Define task or message formats
 - Replace existing protocols (MCP, A2A, GraphQL, REST, etc.)
 - Act as an identity provider or authorization framework
 - Require central registries or governance bodies
 - Impose a specific architecture or product model

AX is intentionally narrow in scope.

### AX in the Agent Stack

AX occupies a distinct layer in the agent ecosystem:
```
+-----------------------------+
|   Agent Reasoning & Tools   |
|   (LLMs, planners, tools)   |
+-----------------------------+ 
|   Execution Protocols       |
|   (MCP, A2A, GraphQL, REST) |
+-----------------------------+
|   AX — Discovery &          |
|   Capability Exchange       |
+-----------------------------+
|   Internet Infrastructure   |
|   (DNS, HTTPS, PKI)         |
+-----------------------------+
```

AX answers “how do I find and understand an agent?”

Execution protocols answer “how do I talk to it once I do?”

## Specifications & Drafts

AX is specified using Internet-Drafts and a JSON schema.

* [**Draft-00**](./draft-agent-discovery-00.md): Core discovery mechanism\
  Defines HTTPS `.well-known` discovery semantics and document structure.

* [**Draft-01**](./draft-agent-discovery-01.md): Capability hashing\
  Adds capability hashing to support efficient change detection without altering discovery semantics.

* [**AX JSON Schema**](./ax-schema.json)\
  Defines the structure of the AX document.


## Conformance

To be AX-compliant, an agent:

* **MUST** expose a valid AX document at the `.well-known` HTTPS location
* **MUST** serve the document over HTTPS using UTF-8 JSON
* **MUST NOT** imply trust, authorization, or endorsement through discovery
* **SHOULD** support standard HTTP caching semantics
* **MAY** include capability hashes as defined in Draft-01

AX deliberately avoids defining any registration, trust, or execution requirements.


## Examples

### Minimal AX Document

The smallest useful AX document an agent can publish:

```json
{
  "record_type": "AX",
  "version": "1.0",
  "agent": {
    "name": "Example Tax Filing Agent",
    "description": "Provides automated tax preparation and filing assistance.",
    "provider": "ExampleCo"
  },
  "endpoints": [
    {
      "protocol": "a2a",
      "url": "https://api.example.com/agents/tax-filing/a2a",
      "auth": ["OIDC"],
      "content_type": "application/json"
    }
  ]
}
```


### Agent Advertising Multiple Protocols

Agents may support multiple interaction protocols simultaneously.

```json
{
  "record_type": "AX",
  "version": "1.0",
  "agent": {
    "name": "Research Assistant Agent",
    "description": "Analyzes documents and answers research questions.",
    "provider": "ExampleCo"
  },
  "endpoints": [
    {
      "protocol": "graphql",
      "url": "https://api.example.com/graphql",
      "auth": ["OIDC", "JWT"],
      "content_type": "application/json"
    },
    {
      "protocol": "mcp",
      "url": "https://api.example.com/agents/research/mcp",
      "auth": ["mTLS"]
    },
    {
      "protocol": "a2a",
      "url": "https://api.example.com/agents/research/a2a",
      "auth": ["OIDC"]
    },
    {
      "protocol": "rest",
      "url": "https://api.example.com/agents/research",
      "auth": ["OAuth2"],
      "content_type": "application/json"
    }
  ],
  "schema": {
    "graphql_schema_url": "https://api.example.com/graphql/schema.graphql",
    "mcp_manifest_url": "https://api.example.com/agents/research/mcp/manifest.json",
    "rest_openapi_url": "https://api.example.com/agents/research/openapi.json",
    "introspection": true
  },
  "capabilities": {
    "intents": ["document.analysis", "research.qna"],
    "async": true,
    "supports_callbacks": true,
    "callback_modes": ["webhook", "poll"]
  }
}
```


### Capability Hashing Example

Draft-01 introduces capability hashing. Until the schema formally defines the hashing fields, implementations SHOULD carry hashes in extensions to remain forward-compatible.

```json
{
  "record_type": "AX",
  "version": "1.1",
  "agent": {
    "name": "Claims Processing Agent",
    "description": "Processes insurance claims and returns eligibility decisions.",
    "provider": "ExampleCo"
  },
  "endpoints": [
    {
      "protocol": "a2a",
      "url": "https://api.example.com/agents/claims/a2a",
      "auth": ["OIDC"]
    }
  ],
  "extensions": {
    "ax": {
      "capability_hash": "sha256:7f3c2e4c8b1f..."
    }
  },
  "capabilities": {
    "intents": ["claims.processing", "claims.eligibility"],
    "async": true,
    "supports_callbacks": true,
    "callback_modes": ["webhook"]
  }
}
```

Capability hashing:

* does not change discovery semantics,
* does not imply trust,
* enables consumers to detect meaningful changes efficiently.


### Publishing an AX Document

An agent operator publishes the AX document at:

```
https://example.com/.well-known/agent-exchange
```

The resource:

* **MUST** be accessible via HTTPS
* **MUST** return UTF-8 JSON
* **SHOULD** include appropriate cache headers

No authentication is required for discovery.


### Consuming AX as a Registry or Indexer

Registries, exchanges, and indexers typically:

1. Discover candidate domains
2. Retrieve the AX document
3. Validate it against the AX schema
4. Index advertised capabilities and protocols
5. Decide whether to onboard, register, or ignore the agent

AX provides the **input signal**; downstream systems make governance decisions.


## Example Use Cases

AX is applicable to many downstream systems, including:

* Enterprise agent registries
* Public or curated agent exchanges
* Marketplaces layered on top of discovery
* Partner-built vertical registries
* Brokerages and federated coordination systems
* Open search indexes for agents

Any system that needs to decide *which agents to trust, onboard, or coordinate* can use AX as a discovery substrate.


## Related Resources

* **Background Reading**\
  [Agent Discovery Exchange (AX): Defining the social contract by which agents introduce themselves to the internet](https://builder.aws.com/content/37BOy7XIq01OFx2w4PkHakVcw6v/agent-discovery-exchange-ax)

  [Discovery Is Infrastructure: Why Agents Need Open Signals Before Platforms](https://medium.com/agentic-ai-systems/discovery-is-infrastructure-why-agents-need-open-signals-before-platforms-723b18a6fe65)

  [From Web Discovery to Agent Tethering: Scaling a Global Network of Agents](https://medium.com/agentic-ai-systems/from-web-discovery-to-agent-tethering-scaling-a-global-network-of-agents-db8ebf764f5f)

* **GitHub Discussions**\
  Community feedback, design notes, and evolution of the specification.\
  [Discussion: Initial public draft of Agent Discovery Exchange (AX)](https://github.com/sempfa/agent-discovery-exchange/discussions/1)

  [Discussion: Capability hashing](https://github.com/sempfa/agent-discovery-exchange/discussions/2)

  [Design Note: AX as a Pre-Registration Discovery Layer for Registries](https://github.com/sempfa/agent-discovery-exchange/discussions/5)

* **Closed Issues**\
  [#4: Align Discovery Mechanism with RFC 8615: Make .well-known HTTPS the Required Path](https://github.com/sempfa/agent-discovery-exchange/issues/4)

* **Open Issues**\
  [#3: Trust Signaling & Attestation](https://github.com/sempfa/agent-discovery-exchange/issues/3)

## Status

AX is early but intentional.

 - It is not an IETF standard
 - It is not final
 - It is expected to evolve
 - Feedback and alternative viewpoints are welcome

AX is published as Internet-Draft–style documents to encourage discussion, experimentation, and independent implementation.


## Getting Started

1. Publish an AX document at the `.well-known` path
2. Validate it against `ax-schema.json`
3. Consume AX documents using a crawler or indexer
4. Use capability hashes to detect changes over time

Example templates and utilities are available in the `examples/` directory.


## Implementations

AX is implementation-agnostic.

Any system that:

 - Publishes an AX document
 - Consumes AX documents
 - Uses them to inform agent interaction decisions

can claim AX compatibility.

Reference and example implementations may be published separately.


## Contributing

Feedback, issues, and pull requests are welcome.
Please use GitHub Discussions for design topics and Issues for concrete proposals.


## License

This project is licensed under MIT-0 license.
Specification contributions follow Internet-Draft conventions.


### Summary

AX defines a missing layer in the agent ecosystem: **open, standardized discovery prior to registration**.

By decoupling discovery from coordination, AX enables agent ecosystems to scale globally without fragmenting around proprietary registries.