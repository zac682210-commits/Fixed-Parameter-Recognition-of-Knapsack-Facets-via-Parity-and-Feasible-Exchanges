MOR 34: Fixed-Parameter Recognition of Knapsack Facets
Zhiyan Lin — research preprint v0.1 — 2026-10-13

Main files
  paper/mor34_fpt_proof.pdf        Complete 8-page analytic proof draft.
  paper/mor34_fpt_proof.tex        Compile twice with pdflatex.
  mor34_research_audit_20261013.txt Chinese result, provenance and limitations.
  CITATION.cff                   Citation metadata (no unverified URL/DOI).
  code/                          Exact reference implementation and checks.
  results/                       Recorded JSON outputs.
  provenance/                    Source and GitHub audit records.
  history/                       Previous screening/checkpoint archive.

Claim and scope
  For positive integer knapsack weights a, max(a)<=b, and nonnegative
  integer candidate c, let K be its number of distinct positive coefficients.
  Theorem 8 computes validity and supporting-face dimension in
  2^{O((K+1)log(K+2))} poly(n,L) bit operations. Facet recognition follows.
  Corollary 9, using standard Frank–Tardos compression, removes numerical
  magnitudes from the arithmetic-operation bound and matches the original
  unit-cost formulation. Zero coefficients are included as one extra class.

Reproduction (Python 3.12.14; standard library only)
  From the archive root:
    cd code
    python verify_reference.py
    python profile_parity_check.py
    python verify_pairing.py
  Each command writes a JSON result into code/. Compare the integer counts
  and PASS status with the corresponding results/ file. Runtime fields vary.
  Seeds are in each source and result. No network access is needed.

Expected meaningful checks
  verify_reference.py: 538 exact binary-enumeration comparisons; 20 facets,
    65 invalid candidates, 152 empty faces, 383 cases with zero coefficients.
  profile_parity_check.py: 460 count-profile instances, 2521 parity classes,
    12803 forced cuts, 16458 affine cells, exact rational rank comparisons.
  verify_pairing.py: 500 endpoint pairs, 5039 constructive cut repartitions;
    in 597 cases only one of the new points is feasible, as allowed by proof.

Limitations
  exact_reference.py deliberately ENUMERATES count vectors. It validates the
  combinatorial algorithm and exact ranks, not the claimed FPT runtime.
  The theoretical algorithm uses a cited fixed-dimensional ILP theorem;
  neither that ILP algorithm nor Frank–Tardos compression is implemented here.
  An initial broad random test, parity_span_check.py, had 1350 instances but
  no nontrivial parity pairs. Its output is retained as exploratory history,
  not as confirmation of the central pairing lemma.
  All checks were performed in the same research session. No independent
  referee review or machine-checked formal proof is claimed.

Source attribution
  Existing: Chen–Zhu's model and XP result; public progress note's swap
  completion and rank-counting approach; fixed-dimensional ILP, convex
  epigraphs, affine-hull separation, and Frank–Tardos weight compression.
  Proposed new: exchange-forcing equal-parity pairing, bounded affine-cell
  decomposition, their FPT recognition consequence, and the facet component
  bound. See the audit for precise checked prior-art scope.
  Substantial AI assistance was used for derivations, literature retrieval,
  implementation, proof drafting and checks. Author attribution is as supplied
  by Zhiyan Lin; it is not a claim of independent human verification.

The historical archive contains earlier partial claims and candidate screens.
The current paper supersedes the statement that FPT(K) is still missing in
that checkpoint. Public repository searches are read-only; nothing has been
uploaded publicly and no authors have been contacted.
