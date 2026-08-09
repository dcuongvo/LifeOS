# ADR 001: Initial Architecture

## Status
Accepted

## Context
LifeOS needs to support multiple domains, agents, memory, RAG, tools, and future expansion.

## Decision
Use a domain-oriented modular monolith for v1.0.

## Why
This gives us clean structure without microservice complexity.

## Alternatives Considered
- Simple layered app: easier, but weaker domain boundaries
- Microservices: scalable, but too complex too early
- Agent-first architecture: flexible, but can become messy
- Event-driven architecture: useful later, but not needed on day one

## Consequences
Good:
- Easier MVP
- Clear folders
- Easier testing
- Can split into services later

Bad:
- Requires discipline to keep domain boundaries clean
- Some architecture overhead compared to a simple script