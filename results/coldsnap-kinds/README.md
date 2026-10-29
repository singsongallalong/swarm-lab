# coldsnap-kinds: the first real kinds run (2026-10-29)

Six DeepSeek Flash generators, each inventing a new kind of area look for Cold Snap,
run from a cloud Claude session. 3 of 6 survived every check; the other 3 ran out of
the 40-turn cap (now 70 for this job). $1.23 in total. `report.md` has the numbers.

- **A, picked first:** frost forking across the circle like rime on glass (`ColdSnapRime`).
- **B, picked second:** a two-armed spiral vortex (`ColdSnapRimeSpiral`).
- **C, passed over:** clock-hand sweeps with rime crescents, too dark to read (`ColdSnapRimeSweep`).

`selection.json` has the reasons, the first fix for each and a code review. Each
`candidate-<letter>.patch` is the whole candidate: its module, its registry line, its
rows and Cold Snap pointed at it. They apply on top of the drafted-kinds platform
(`docs/kind-drafting/0001-drafted-area-kinds.patch`), which must go in first:

    git am   <swarm-lab>/docs/kind-drafting/0001-drafted-area-kinds.patch
    git apply <swarm-lab>/results/coldsnap-kinds/candidate-A.patch

Base: arpg-game `8c0931592b` (main `41c9339` plus the platform commit). `key.json` maps
letters to generators; all three were DeepSeek here, so it hides nothing.

All three survivors asked for a painted frost-crystal particle texture.
