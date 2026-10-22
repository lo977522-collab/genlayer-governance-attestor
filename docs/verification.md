# Verification

Run these checks from the project root:

```bash
python3 -m py_compile contracts/governance_proposal_attestor.py
genvm-lint lint contracts/governance_proposal_attestor.py
python tests/unit/test_governance_logic.py
pytest tests/direct/test_governance_proposal_attestor.py -v
```

Direct Mode tests mock GitHub issue/comment responses and the LLM decision. They are not live network or testnet tests. A real deployment address must be documented separately if the contract is deployed.
