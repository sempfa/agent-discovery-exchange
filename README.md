# Agent Discovery Exchange (AX)

Agent Discovery Exchange (AX) defines a lightweight, internet-native mechanism for discovering autonomous AI agents, understanding their capabilities, and negotiating how to interact with them — without standardising execution semantics or centralising control.

AX is designed to fill a missing layer in the agent ecosystem: discovery and capability exchange across organisational boundaries.

## Why AX Exists

As agentic systems move beyond isolated deployments, a new class of problems emerges:

- How does an agent discover other agents on the public internet?
- How does it understand what they can do?
- How does it know how to talk to them?
- How can this happen securely, dynamically, and without pre-arranged integration?

Today, these questions are solved with:

- Hard-coded endpoints
- Proprietary registries
- Out-of-band documentation
- Manual configuration

These approaches do not scale.

**AX exists to provide a common, internet-aligned discovery layer for agents**, analogous to what DNS + HTTPS already provide for services.

## What AX Is

AX is:

- A discovery and metadata exchange mechanism
- Protocol-agnostic
- Execution-neutral
- Built on existing internet standards (DNS, HTTPS, .well-known)
- Designed for incremental adoption

At its core, AX allows an agent to publish a machine-readable document that answers:

    Who am I?
    What can I do?
    How can you interact with me?
    Under what constraints and trust assumptions?

## What AX Is Not

AX explicitly does not:

- Define agent execution semantics
- Define task or message formats
- Replace existing protocols (MCP, A2A, GraphQL, REST, etc.)
- Act as an identity provider or authorization framework
- Require central registries or governance bodies
- Impose a specific architecture or product model

AX is intentionally narrow in scope.

## AX in the Agent Stack

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

AX answers _“how do I find and understand an agent?”_

Execution protocols answer _“how do I talk to it once I do?”_

## Relationship to Existing Protocols

AX is complementary by design.

### MCP (Model Context Protocol)

- MCP defines how tools are invoked by models
- AX defines how MCP endpoints are discovered and described

## A2A (Agent-to-Agent protocols)

- A2A defines peer agent interaction semantics
- AX defines how A2A-capable agents find each other

## GraphQL / REST

- These define API invocation
- AX defines API discovery and capability metadata

AX does not compete with execution protocols, it enables them to be used **dynamically and interoperably**.

## Design Principles

AX is guided by a small set of principles:

- Discovery before execution
- Decentralisation over registries
- Declaration over assumption
- Policy at the edge
- Evolution over finality

These principles are reflected in both the specification and its release process.

## The Drafts

AX is being developed as a series of Internet-Drafts, each layering additional capability:

[Draft 00 — Core discovery mechanism](./draft-agent-discovery-00.md)

...

Each draft is intentionally scoped and independently useful.

## Status

AX is early but intentional.

- It is not an IETF standard
- It is not final
- It is expected to evolve
- Feedback and alternative viewpoints are welcome

AX is published as Internet-Draft–style documents to encourage discussion, experimentation, and independent implementation.

## Implementations

AX is implementation-agnostic.

Any system that:

- Publishes an AX document
- Consumes AX documents
- Uses them to inform agent interaction decisions

can claim AX compatibility.

Reference and example implementations may be published separately.

## Why This Matters

Agentic systems are becoming distributed systems of intelligence.

Without a common discovery layer:

- Interoperability will fragment
- Governance will be brittle
- Federation will remain bespoke

AX aims to provide a small, composable foundation that lets the agent ecosystem grow without central control and without reinvention.

## License and Contribution

This repository is intended for open discussion and collaboration.

Contributions, critiques, and alternative designs are encouraged.

## summary

AX defines how agents introduce themselves to the internet, not how they think, act, or execute.

# Getting Started (Implementers)

AX is intentionally lightweight. Implementing it does not require adopting a new runtime, framework, or protocol.

### Minimal AX Producer (Agent Publisher)

To expose an agent via AX, you need to:

1. Choose a discovery domain
    - Typically your primary domain (e.g. example.com)
    - Optionally use _agent.example.com

2. Host an AX document
   - Location: `https://_agent.example.com/.well-known/agent-exchange.json`
   - Content-Type: `application/agent-exchange+json`

3. Describe your agent
   - Provide a name and description
   - Advertise supported interaction protocols (GraphQL, MCP, A2A, REST, etc.)
   - Optionally include capability hints, constraints, or trust metadata

4. Keep it stable
   - Treat the AX document as a contract
   - Version changes intentionally
   - Expect consumers to cache and compare capability hashes

**That’s it**. No central registry. No approval process.

## Minimal AX Consumer (Agent Discoverer)

To consume AX:

1. Resolve the discovery endpoint
   - Attempt: `https://_agent.<domain>/.well-known/agent-exchange.json`

2. Validate the document
   - HTTPS transport
   - Media type
   - JSON structure
   - (Optional) signature or issuer

3. Evaluate compatibility
   - Supported protocols
   - Required authentication
   - Declared capabilities and constraints

4. Select an interaction protocol
   - Based on local policy and task requirements
   - AX does not mandate selection logic

5. Invoke using the chosen protocol
   - Enforce authentication, authorization, and rate limits at execution time

AX consumers should treat all metadata as declarative and advisory.

## Incremental Adoption

AX can be adopted incrementally:

- Start with discovery + protocol advertisement
- Add capability hashing when stability matters
- Add trust tiers, constraints, and federation logic only if needed

Partial adoption is expected and supported.

## Reference Status

AX drafts are informational and evolving.

Implementers are encouraged to:

- Experiment
- Provide feedback
- Propose extensions
- Publish independent implementations