# Research and contribution standards

Each research track lives in `problems/<slug>/` and contains a self-contained README, a precise problem statement with primary sources, hypotheses and results, reproducible proof and experiment artifacts, limitations, and next steps. Prefer preserving an existing track's internally consistent layout rather than moving its files unnecessarily.

Before starting a new track or making a substantial claim, review the relevant literature and existing work in this repository. Prioritize independent, nonredundant contributions. Record failed attempts and distinguish empirical evidence from a general argument. Include graph encodings, solver assumptions, random seeds, dependency versions, and exact verification instructions where relevant. Use independent verifiers and formal proof assistants when practical; never conflate solver status or a successful script run with peer review.

Every substantial result should include a claim, proof or certificate, reproducibility instructions, limitations, prior-work references, and a novelty status. Report AI assistance and attribute human and published contributions. No personal information, credentials, confidential materials, or unauthorized third-party content belongs in the repository. Do not claim affiliation or endorsement. Respect applicable licenses. Correct errors publicly without rewriting the historical research record.

Add a new research track to `PROBLEMS.md` and the root README. Share genuinely reusable utilities in `tools/`, with documentation and tests. Keep research-specific scripts with their problem. Avoid giant generated outputs unless needed to reproduce the evidence.
