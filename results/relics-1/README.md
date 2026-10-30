# relics-1: Flash x4 against V4 Pro x4 on one contract (2026-10-30)

fafwa asked for experiments 3 and 4: a real gameplay system against a contract and tests Claude wrote, with V4 Pro beside Flash. The pure core of relics (docs/design/endgame-power.md, a proposal) and three rows; held-out tests (RelicsHeldOut.spec.luau, kept outside the tree during the run) scored, not gating; then a blind Claude review of the patches without the scores.

| Letter | Model | Held-out | Turns | Seconds | Cost (est.) | Review: correct / fit / relics / total |
|---|---|---|---|---|---|---|
| A | deepseek-pro | 14/14 | 14 | 321.8 | $0.1951 | 8 / 8 / 7 / 7.7 |
| B | deepseek-pro | 14/14 | 16 | 303.0 | $0.1965 | 8 / 8 / 7 / 7.7 |
| C | deepseek | 14/14 | 30 | 312.9 | $0.0874 | 10 / 9 / 6 / 8.5 |
| D | deepseek-pro | 14/14 | 13 | 382.4 | $0.2174 | 7 / 7 / 5 / 6.4 |
| E | deepseek-pro | 14/14 | 14 | 438.3 | $0.2472 | 9 / 7 / 8 / 8.1 |
| F | deepseek | 14/14 | 27 | 315.0 | $0.0895 | 10 / 6 / 6 / 7.6 |
| G | deepseek | 14/14 | 28 | 324.3 | $0.0893 | 10 / 9 / 5 / 8.2 |
| H | deepseek | 13/14 | 24 | 290.0 | $0.0817 | 6 / 8 / 5 / 6.3 |

Findings:

- 8 of 8 passed the visible specs, 7 of 8 every held-out test (H, Flash, miscounts copies to max with spares).
- The blind review ranked C, G (Flash) and E (Pro) top; it found a shared-conditions aliasing bug in three Pro builds (A, B, D) the tests didn't catch, and H's held-out bug again.
- Pro used half the turns and tokens and cost about 2.5x as much; on review, neither model was clearly better.
- Every build's EmberHeart named the status `Burning`, which doesn't exist (`Ignite` does). The brief was wrong (Claude's), and no check caught it: RelicRows now checks every status a condition names, and the brief says `Ignite`.
- Builders' requests found two more contract gaps: the pack's explain command (fixed) and an unspecified all-zero weights case in rollGrade.
- The reviewer suggests C's or G's core with E's rows, after the status fix, if relics leave the silo.
