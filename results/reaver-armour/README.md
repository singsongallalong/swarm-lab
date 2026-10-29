# reaver-armour: the first armour run (2026-10-29)

Six DeepSeek Flash generators each designed a full Reaver (barbarian) set, helm, chest,
gloves and boots, from a different silhouette, run from a cloud Claude session. All 6
survived every check, each within the 64-part set budget (59 to 63). $1.56 in total.

- **D, picked first:** two pale bone antlers over broad smoke-cured hide (`ReaverHelm` ...).
- **A, picked second:** a horned beast-skull helm, wolf-fur mantle, bone trophies.
- **E, picked third:** an asymmetric skull pauldron, the other arm bare.

`selection.json` has the reasons and the first fix for each. Every candidate's whole set
is `candidate-<letter>.patch` (four look files, their registry lines and catalog rows),
applicable on arpg-game main `41c9339`:

    git apply <swarm-lab>/results/reaver-armour/candidate-D.patch

The looks aren't worn by anything yet: a base (numbers, drop weight, bag picture) or a
hand-made item decides who wears them (arpg-game docs/guides/adding-items.md). Every
candidate names its files ReaverHelm, ReaverChest, ReaverGloves and ReaverBoots, so apply
one at a time. Bare arms show the preview dummy's blue; check real avatars in Studio.
