# Design: Governance Proposal Attestor

## Problem

Public governance proposals often collect discussion and votes in issue comments, but a later reviewer cannot easily reproduce which proposal text and vote markers supported a quorum decision.

## Evidence model

Each record is limited to a GitHub owner, repository, proposal issue, quorum, and policy. The contract constructs the API endpoints itself. It counts only explicit `[FOR]` and `[AGAINST]` markers and stores digests for the proposal text and normalized comments.

## Consensus model

The leader and validators independently fetch the issue and comments. They run the same constrained assessment and compare the decision, vote counts, proposal digest, and votes digest. Rationale is not compared because explanations can differ while the stable evidence gates remain equal.

## Limitations

This prototype does not authenticate voters, prevent duplicate accounts, or perform token-weighted voting. It is evidence attestation for a narrow public workflow, not a production governance framework.
