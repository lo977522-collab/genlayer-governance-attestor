# GenLayer Governance Proposal Attestor

An experimental GenLayer Intelligent Contract for consensus-based verification of public governance proposal evidence.

## What it does

The contract records one GitHub issue as a proposal, a quorum, and a short policy. Public comments with explicit `[FOR]` or `[AGAINST]` markers are counted as votes. The leader and validators independently fetch the proposal and comments, then assess whether the evidence reaches the stated quorum.

This is a bounded governance evidence primitive, not a general-purpose voting system. It does not accept arbitrary URLs or treat an LLM response as proof by itself.

## Equivalence Principle

Validators repeat the public evidence fetch and constrained semantic assessment. They compare the decision, vote counts, proposal digest, and votes digest. A changed proposal or changed vote comments therefore cannot silently produce an equivalent result.

## Lifecycle

`OPEN` → `ASSESSED` → `CHALLENGED` → `FINAL`

The creator can finalize an assessed proposal. A separate challenge issue is recorded as counter-evidence.

## Verification and limits

The repository includes AST lint, local state tests, mocked GenLayer Direct Mode tests, and a GitHub Actions workflow. External GitHub and LLM calls are mocked in tests. The prototype does not prove voter identity, prevent duplicate commenters, or replace a production governance framework.

## Status

Pre-deployment prototype unless a deployment Explorer link is explicitly added by the maintainer. Not suitable for legal, financial, employment, or other high-stakes decisions.

## License

MIT. See [LICENSE](LICENSE).
