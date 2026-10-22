# Portal submission draft

## Suggested category

Developer → Intelligent Contracts

## Suggested title

Governance Proposal Attestor — Public Quorum Evidence Primitive

## Description

Governance Proposal Attestor is a standalone GenLayer Intelligent Contract for a bounded public governance workflow. A requester records one GitHub proposal issue, a quorum, and an explicit policy. The contract constructs GitHub API endpoints from validated identifiers, fetches the proposal and public comments, counts explicit FOR and AGAINST markers, and runs a constrained semantic assessment. GenLayer validators independently repeat the fetch and compare the decision, vote counts, and SHA-256 digests of the proposal and normalized vote evidence. The repository includes AST lint, local state tests, mocked GenLayer Direct Mode tests, and a successful CI workflow. This is a prototype and does not authenticate voter identity or replace a production governance system.
