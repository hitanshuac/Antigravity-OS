# 1. Record architecture decisions

Date: 2026-06-07

## Status

Accepted

## Context

We need to record the architectural decisions made on this project. Historically, major decisions (like adopting DuckDB over SQLite, or Context Compaction over simple truncation) were made without an immutable, contextual history. This leads to cyclical debates and lack of context for new agents or engineers joining the environment.

## Decision

We will use Architecture Decision Records (ADRs), following the markdown format proposed by Michael Nygard. We will store these inside `.agents/architecture/adrs/` so that automated agents and humans can parse the historical context of the system before proposing changes.

## Consequences

* See [Michael Nygard's article](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) on Architecture Decision Records.
* Agents analyzing the codebase MUST read the ADRs to understand why certain tools (e.g. Semgrep, Ruff, DuckDB) are strictly enforced.
