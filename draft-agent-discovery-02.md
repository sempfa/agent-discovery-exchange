```
Internet-Draft                                              A. Sempf
Intended status: Informational                          January 2026
Expires: July 2026
```

# Agent Discovery Exchange (AX)

## Status of This Memo

This Internet-Draft is submitted in full conformance with the provisions of BCP 78 and BCP 79.

This Internet-Draft is submitted as an informational document. It represents work in progress and may be updated, replaced, or obsoleted at any time. Distribution of this memo is unlimited.

## Abstract

As autonomous and semi-autonomous AI agents increasingly operate across organizational, administrative, and trust boundaries, consumers of agent discovery metadata require signals that help assess provenance, integrity, and trustworthiness prior to engagement.

This document extends the Agent Discovery Exchange (AX) specification by defining optional trust and attestation mechanisms. These mechanisms enable agents, registries, brokers, and other intermediaries to publish and consume non-authoritative trust signals without coupling discovery to authorization, governance, or execution semantics.

This draft deliberately limits scope to pre-execution trust signaling. It does not define approval workflows, enforcement mechanisms, or execution-time policy. Those concerns remain the responsibility of registries, brokers, arbiters, and runtime systems.

## Terminology

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119.

## 1. Introduction

Agent Discovery Exchange (AX) defines a lightweight, internet-native mechanism for discovering autonomous agents and understanding their advertised capabilities and supported interaction protocols.

Discovery alone, however, is insufficient for safe and scalable adoption. Consumers of discovery metadata often require additional signals to assess:

whether an agent’s claims are authentic,

who is asserting those claims,

and whether the agent meets baseline trust expectations.

This document introduces trust and attestation signals as optional extensions to AX discovery metadata. These signals are intended to inform downstream decision-making without constraining how that decision-making is implemented.

## 2. Design Principles

This draft is guided by the following principles:

Layer separation: Discovery, trust signaling, and execution governance are distinct concerns.

Non-authoritativeness: Trust signals inform decisions; they do not make decisions.

Plurality of trust: No single trust authority is assumed or required.

Registry neutrality: AX remains independent of registries, brokers, or marketplaces.

Incremental adoption: Trust signals are optional and backward-compatible.

## 3. Scope and Non-Goals
### 3.1 In Scope

This draft defines:

 - Optional trust metadata associated with an AX document
 - Attestation structures and provenance signals
 - Trust tier declarations
 - Guidance for consumers on interpreting trust signals

### 3.2 Explicit Non-Goals

This draft does not define:

 - Authorization or access control decisions
 - Approval, onboarding, or registration workflows
 - Execution-time policy enforcement
 - Economic settlement, pricing, or billing
 - Agent-to-agent relationship graphs or reputation propagation

Trust signals defined here are *pre-execution inputs* only.

## 4. Layering Clarification

AX discovery operates at a different architectural layer than governance and execution systems.

**Discovery**  
_answers_: What exists? What does it claim to do?

**Trust signaling**  
_answers_: Who asserts this information, and under what basis?

**Execution governance**   
_answers_: Is this agent allowed to act, under which policy, and with what controls?

Trust and attestation metadata defined in this draft **MUST NOT** be interpreted as authorization or endorsement. Consumers **MUST** apply their own policy, governance, and risk evaluation before interacting with an agent.

## 5. Trust Model Overview

AX supports a _signal-based trust model_:

 - Trust is expressed as metadata assertions.
 - Assertions are made by one or more attestation authorities.
 - Consumers decide which authorities they trust and how to weight signals.

AX does not mandate any trust authority, scoring algorithm, or evaluation policy.

## 6. Trust Tiers

An AX document **MAY** declare one or more trust tiers. Trust tiers are coarse-grained indicators intended to support filtering and prioritization.

Example trust tiers include, but are not limited to:

 - `self-asserted`
 - `operator-attested`
 - `enterprise-attested`
 - `third-party-attested`

Trust tiers:

 - **MUST NOT** imply authorization
 - **MUST NOT** imply endorsement
 - **SHOULD** be interpreted as descriptive, not prescriptive

## 7. Attestation Statements

An AX document **MAY** include one or more attestation statements.

Each attestation statement **SHOULD** include:

 - Identifier of the attestation authority
 - Scope of the attestation (identity, ownership, capability claims)
 - Optional validity period
 - Optional cryptographic signature or reference

Attestations **MAY** be:

 - self-issued
 - enterprise-issued
 - vendor-issued
 - ecosystem-issued

AX places no restrictions on the attestation mechanism, signature format, or verification process.

### 7.1 Illustrative Example (Non-Normative)

The following example illustrates how an AX document MAY include optional trust tier declarations and attestation statements. This example is non-normative and provided for illustrative purposes only. Trust signals shown below are informational and MUST NOT be interpreted as authorization or endorsement.

```json
{
  "record_type": "AX",
  "version": "1.0",
  "agent": {
    "name": "Invoice Processing Agent",
    "description": "Processes and reconciles enterprise invoices."
  },
  "endpoints": [
    {
      "protocol": "a2a",
      "url": "https://api.example.com/agents/invoice/a2a"
    }
  ],
  "extensions": {
    "ax": {
      "trust": {
        "trust_tiers": ["enterprise-attested"],
        "attestations": [
          {
            "type": "ownership",
            "issuer": {
              "name": "ExampleCorp Security",
              "uri": "https://security.example.com"
            },
            "issued_at": "2026-01-15T00:00:00Z",
            "expires_at": "2027-01-15T00:00:00Z"
          }
        ]
      }
    }
  }
}
```

## 8. Multiple Attestation Authorities

AX explicitly supports multiple, independent attestation authorities.

Consumers:

 - **MUST NOT** assume a single authoritative source of trust
 - **SHOULD** evaluate attestations according to local policy
 - **MAY** require one or more trusted authorities before engagement

This model aligns with established internet trust systems such as PKI, SBOM signing, and software supply-chain attestations.

## 9. Consumer Guidance

Consumers of AX trust metadata:

 - **MUST** treat trust signals as advisory
 - **MUST** apply local governance and policy
 - **SHOULD** consider freshness, provenance, and scope
 - **SHOULD NOT** infer endorsement from presence alone

Registries, brokers, and arbiters are expected to layer additional evaluation, scoring, and enforcement mechanisms on top of AX trust signals.

## 10. Security Considerations

Trust metadata introduces new attack surfaces, including:

 - False self-assertion
 - Stale or revoked attestations
 - Implicit trust escalation

Consumers **SHOULD** implement:

 - Signature verification where applicable
 - Expiration handling
 - Authority allowlists
 - Defense-in-depth validation

AX does not attempt to solve these problems centrally.

## 11. Privacy Considerations

Attestation metadata may expose organizational relationships or operational details.

Publishers SHOULD:

 - Minimize sensitive disclosures
 - Avoid embedding personal data
 - Prefer references over inline details

 ## 12. Relationship to Future Work

This draft intentionally defers:

 - Agent-to-agent relationship semantics
 - Endorsement graphs
 - Reputation propagation
 - Federation scoring models

These topics may be addressed in future drafts once trust signaling primitives are established and validated.

## 13. IANA Considerations

This document introduces no new IANA registrations.

## 14. References

 - RFC 2119 – Key words for use in RFCs to Indicate Requirement Levels
 - RFC 8615 – Well-Known URIs
 - Agent Discovery Exchange (AX) Draft-00
 - Agent Discovery Exchange (AX) Draft-01