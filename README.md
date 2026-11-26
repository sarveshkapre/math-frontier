# Math Frontier

An independent, open research project investigating unsolved mathematical problems through mathematical reasoning, computation, and AI-assisted exploration.

The goal is meaningful, original mathematics per unit of research effort—not a leaderboard of claimed solutions. We aim to develop new proofs, counterexamples, structural insights, and reusable computational methods, while documenting failures and uncertainty.

## Research tracks

| Problem | Area | Status |
|---|---|---|
| [Lužar–Soták conjecture](problems/luzar-sotak-conjecture/) | Graph theory | General conjecture open; partial results with checkable certificates; novelty unconfirmed |

See [PROBLEMS.md](PROBLEMS.md) for the research index and [CONTRIBUTING.md](CONTRIBUTING.md) for research standards.

## Verify the current results

From the repository root, with Python 3.10 or newer:

```sh
python3 problems/luzar-sotak-conjecture/verify_theorems.py
```

This runs the included standard-library certificate checks and construction checks. It is not a proof-assistant formalization or peer review.

## Research approach

- Look for tractable questions where a new result would matter; review the literature before committing resources.
- Formulate testable hypotheses, seek counterexamples, and use computation to guide mathematical proofs.
- Report the scope, limitations, reproducibility, and originality status of each result. Distinguish exhaustive search, bounded experiments, certificate-checked results, and formally verified theorems.
- Preserve unsuccessful approaches and negative findings. Invite scrutiny and credit prior work and contributors.

## Attribution and AI assistance

This is an independent AI-assisted research initiative. AI systems contributed to the formulation, computation, proof drafting, and verification of the initial research. AI-generated arguments may contain errors and must be evaluated on their mathematical merits. No affiliation with the authors of the conjectures or endorsement by their institutions is implied. Novelty is not established merely by deriving a result independently or failing to find it in a literature search.

Licensing is to be established before inviting redistribution or code reuse. No third-party material is intentionally relicensed here.
