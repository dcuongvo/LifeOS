# LifeOS Architecture v1.0

## Vision
LifeOS is a personal AI operating system for goals, career planning, memory, knowledge retrieval, and future autonomous planning.

## MVP Scope
LifeOS v0.1 starts as a Career Planning Assistant.

It can:
- Store goals, projects, tasks, documents, and memories
- Upload and index resume/job descriptions
- Use RAG to retrieve relevant knowledge
- Use a Career Agent to analyze gaps
- Use a Planner to suggest next actions

## Architecture Choice
Domain-oriented modular monolith.

Why:
- Easier to build than microservices
- Keeps code organized by domain
- Can scale later by splitting domains into services
- Works well with agents, RAG, and future digital twin features

## Core Modules
- apps/api: FastAPI backend
- apps/web: future frontend
- domains/career: career goals, resumes, applications, skills
- domains/planning: goals, projects, tasks
- domains/knowledge: documents, chunking, embeddings, retrieval
- domains/memory: long-term facts and user memory
- orchestration: LangGraph workflows and agent routing
- platform: database, LLM providers, tools, events, observability

## Initial Stack
- Python
- FastAPI
- PostgreSQL
- pgvector
- LangGraph
- Docker
- OpenAI or Gemini API