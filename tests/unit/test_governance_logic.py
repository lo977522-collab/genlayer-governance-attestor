"""Fast local state checks for the governance proposal attestor."""

import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


class FakeAddress:
    as_hex = "0x" + "1" * 40


class FakeContract:
    def __new__(cls):
        instance = super().__new__(cls)
        instance.proposals = {}
        return instance


class FakeResponse:
    def __init__(self, payload):
        self.status_code = 200
        self.body = payload.encode("utf-8")


def load_contract():
    identity = lambda value: value
    public = types.SimpleNamespace(write=identity, view=identity)

    def get(url):
        import json
        if url.endswith("/comments"):
            return FakeResponse(json.dumps([{"user": {"login": "alice"}, "body": "[FOR] support"}]))
        return FakeResponse(json.dumps({"number": 11, "title": "Adopt policy", "body": "A public governance proposal."}))

    def prompt(_text, response_format=None):
        return {"decision": "QUORUM_REACHED", "rationale": "The explicit vote reaches quorum."}

    class Return:
        def __init__(self, calldata):
            self.calldata = calldata

    fake = types.ModuleType("genlayer")
    fake.allow_storage = identity
    fake.Address = FakeAddress
    fake.u256 = int
    fake.TreeMap = dict
    fake.gl = types.SimpleNamespace(
        Contract=FakeContract,
        public=public,
        nondet=types.SimpleNamespace(web=types.SimpleNamespace(get=get), exec_prompt=prompt),
        vm=types.SimpleNamespace(UserError=Exception, Return=Return, run_nondet_unsafe=lambda leader, validator: leader()),
        message=types.SimpleNamespace(sender_address=FakeAddress()),
    )
    path = Path(__file__).resolve().parents[2] / "contracts" / "governance_proposal_attestor.py"
    spec = importlib.util.spec_from_file_location("governance_attestor_local", path)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {"genlayer": fake, spec.name: module}):
        spec.loader.exec_module(module)
    return module


class GovernanceAttestorTests(unittest.TestCase):
    def setUp(self):
        self.module = load_contract()
        self.contract = self.module.GovernanceProposalAttestor()
        self.policy = "At least one explicit FOR vote is required for the proposal to pass."

    def create(self):
        return self.contract.create_proposal("acme", "governance-demo", 11, 1, self.policy)

    def test_create_and_restrict_identifiers(self):
        self.assertEqual(self.create(), "0")
        self.assertEqual(self.contract.get_proposal_count(), 1)
        self.assertIn("issues/11/comments", self.contract.get_evidence_urls("0")["votes"])
        with self.assertRaisesRegex(Exception, "unsupported character"):
            self.contract.create_proposal("acme", "governance/demo", 11, 1, self.policy)
        with self.assertRaisesRegex(Exception, "positive issue"):
            self.contract.create_proposal("acme", "governance-demo", 0, 1, self.policy)

    def test_assess_and_finalize(self):
        proposal_id = self.create()
        self.contract.assess_proposal(proposal_id)
        proposal = self.contract.get_proposal(proposal_id)
        self.assertEqual((proposal.status, proposal.decision), ("ASSESSED", "QUORUM_REACHED"))
        self.assertEqual((proposal.for_votes, proposal.against_votes), (1, 0))
        self.assertEqual(len(proposal.votes_digest), 64)
        self.contract.finalize_proposal(proposal_id)
        self.assertEqual(self.contract.get_proposal(proposal_id).status, "FINAL")

    def test_challenge_requires_different_issue(self):
        proposal_id = self.create()
        self.contract.assess_proposal(proposal_id)
        with self.assertRaisesRegex(Exception, "must differ"):
            self.contract.challenge_proposal(proposal_id, 11)
        self.contract.challenge_proposal(proposal_id, 12)
        self.assertEqual(self.contract.get_proposal(proposal_id).status, "CHALLENGED")


if __name__ == "__main__":
    unittest.main()
