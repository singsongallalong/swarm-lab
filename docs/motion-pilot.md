# Motion pilot: cast motions from words, whole versus pose-to-pose

Started 2026-10-30. fafwa: "what do you think about having an animation described in words in
keyframes ... and then deepseek agents work on generating keyframes using prior ones as an
input?" Then: "The animation pilot sounds good."

## What's already true

arpg-game keys cast motions as **end effectors**, not joint angles (`CastDrafts.luau`,
`docs/guides/cast-motions.md`):

- each pose places the weapon's grip from the right shoulder (`weapon`) and the way its head
  points (`point`);
- it sets the chest's `twist` and `lean` and the hips' `drop`;
- the rig solves the arms and legs, and plays the keys through muscles.

So builders write effector poses, and the motion lab renders them offline on the R15 body
and prints its rule pass (`!` lines). The lab's run takes about 2 s.

## The question

Does splitting the work the way animators do (blocking, then timing and polish) beat one
builder doing the whole motion, at the same number of builder sessions?

| Arm | Job, brief | Sessions |
| --- | --- | --- |
| A, whole | `motions`, `Smash`: the five keys in words, the timeline a guide, free to add in-betweens | 6 builders, then 1 rework with critic notes (12) |
| B, pose-to-pose | `motions`, `SmashBlock`: the same words, exactly five poses on a fixed timeline; then `motions-polish` on the best block: timing, in-betweens, holds, kicks | 6 blocking + 6 polish (12) |

Both use the same six directions and the same critic rubric, weighted:

| Criterion | Weight |
| --- | --- |
| Reads as the brief | 3 |
| Weight and snap | 2.5 |
| Clean body | 2 |
| Arc | 1.5 |
| Recovery | 1 |

The motion is a one-handed overhead mace smash at a 0.6 s cast, a draft that plays as
Ground Slam. The reference is Ground Slam's one-handed swing.

## How it's judged

1. Each arm runs its own critic passes.
2. The final round puts the best three of each arm on one blind sheet: same renders, letters
   shuffled. A fresh critic ranks all six.
3. Beside it, the lab's `!` count on each final.
4. fafwa's eye decides whether either is worth a Studio lane.

## Log

- 2026-10-30: the `motion` family in `swarm/pack.py`, and the job in
  `targets/arpg-game/motions/`. Dry-ran with hand keys: the renders, specs and row check pass,
  and the lab flags the hand keys' faults. Launched A and B1.
