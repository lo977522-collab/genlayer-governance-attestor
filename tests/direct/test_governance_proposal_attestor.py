"""Mocked Direct Mode tests for GovernanceProposalAttestor."""

import json
import pytest


ISSUE_URL = "https://api.github.com/repos/acme/governance-demo/issues/11"
COMMENTS_URL = ISSUE_URL + "/comments"
POLICY = "At least one explicit FOR vote is required for the proposal to pass."


@pytest.fixture
def attestor(direct_vm, direct_deploy):
    direct_vm.strict_mocks = True
    direct_vm.check_pickling = True
    return direct_deploy("contracts/governance_proposal_attestor.py", sdk_version="v0.2.16")


def mock_evidence(vm, comment_body="[FOR] support"):
    vm.mock_web(r"https://api\.github\.com/repos/acme/governance-demo/issues/11$", {"status": 200, "body": json.dumps({"number": 11, "title": "Adopt policy", "body": "A public governance proposal."})})
    vm.mock_web(r"https://api\.github\.com/repos/acme/governance-demo/issues/11/comments$", {"status": 200, "body": json.dumps([{ "user": {"login": "alice"}, "body": comment_body }])})
    vm.mock_llm(r"(?s).*assessing one public governance proposal.*", json.dumps({"decision": "QUORUM_REACHED", "rationale": "Mocked governance review."}))


def test_create_and_assess(attestor, direct_vm):
    proposal_id = attestor.create_proposal("acme", "governance-demo", 11, 1, POLICY)
    assert proposal_id == "0"
    assert attestor.get_evidence_urls(proposal_id)["proposal"] == ISSUE_URL
    mock_evidence(direct_vm)
    attestor.assess_proposal(proposal_id)
    proposal = attestor.get_proposal(proposal_id)
    assert (proposal.status, proposal.decision) == ("ASSESSED", "QUORUM_REACHED")
    assert (proposal.for_votes, proposal.against_votes) == (1, 0)


def test_validator_rejects_changed_vote_comments(attestor, direct_vm):
    proposal_id = attestor.create_proposal("acme", "governance-demo", 11, 1, POLICY)
    mock_evidence(direct_vm)
    attestor.assess_proposal(proposal_id)
    direct_vm.clear_mocks()
    mock_evidence(direct_vm, "[AGAINST] reject")
    assert direct_vm.run_validator(index=0) is False


def test_finalize_requires_assessment(attestor, direct_vm):
    proposal_id = attestor.create_proposal("acme", "governance-demo", 11, 1, POLICY)
    with direct_vm.expect_revert("cannot be finalized"):
        attestor.finalize_proposal(proposal_id)
