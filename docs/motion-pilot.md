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
- 2026-10-30, round 1: arm A, 6 of 6 passed the checks ($1.12). Arm B's blocking pass: 5 of 6, plus 1 after a resume ($1.70).
- Arm A's critic passes 1 and 2: the top three were A (g04), C (g02) and F (g05), at 7.0, 6.8 and 5.5.
- Arm B's block critic: E (g03) at 7.2 was the best block, then B at 6.5.
- **DeepSeek's balance ran out** during the polish pass. 4 of 6 polish builders stopped with "402 Insufficient Balance", and only g00 and g05 finished.

## Result (blind final, one fresh critic, 2026-10-30)

| Rank | Candidate | Total | Lab `!` faults |
| --- | --- | --- | --- |
| 1 | B, the best block, unpolished (smash-block-1 g03) | 7.2 | 5 |
| 2 | B, polished from it (smash-polish-1 g05) | 6.9 | 8 |
| 3 | A, the whole motion, reworked (smash-whole-1 g04) | 6.6 | 6 |
| 4 | A (g02) | 6.3 | 6 |
| 5 | B, polished (g00) | 5.9 | 7 |
| 6 | A (g05) | 4.7 | 6 |

For comparison, Ground Slam has 6 lab faults and the hand-keyed Chop draft has 7. The critic's verdict: the winner is worth a look in Studio. It flagged the mace passing level at chest height around 0.52 s, and a fold that reads weakly from the game camera.

What it suggests (guessed, from one critic and small numbers):

- **The narrow task won.** Five named poses on a fixed timeline, judged as poses, beat the free brief at the same cost.
- **Polish didn't help.** The polished versions scored at or below the block they started from, and both added lab faults. This matches the features runs, where reworks rarely improved the result. Flash seems better at making one well-specified thing than at improving something already made.
- **The arms were uneven at the end:** two polish finishers against six. A rerun with balance would settle the polish question.

Files: `results/motion-pilot/` holds the winner's and the runner-up's patches and renders, the blind critique, and the key.

## fafwa's verdict in Studio (C393, 2026-10-30)

"The animation looked pretty good actually ... wow! I am pleasantly surprised with the
animation. Excellent!" It was SmashBlock, the winning block, on arpg-game branch
`claude/smash-draft`.

The one fault was the effects. Ground Slam's effects fired out of time with the mace landing.

- **Likely cause (measured):** the draft plays over its own 0.6 s, but the skill's hit and its
  looks keep Ground Slam's `use.time` of 0.15 s. So they land about 0.45 s before the mace.
- **Why the lab missed it:** the lab draws no effects for a draft without its own, so its
  `EffectTiming` check had nothing to compare.

## Next time

fafwa: draft with the effects turned on, or have a Claude repair the disconnect later.

1. **Draft with effects on.** A motions brief names the skill the motion is for, and the job
   renders it with that skill's effects on its cues. Then `EffectTiming` warns builders and
   critics when an `Impact` fires off the blow. This needs the lab to give a draft the effects
   of the skill it plays, as `CastPick.swing` does for moveset swings, and the brief's cast
   time to be the one the skill will have.
2. **Or repair afterwards:** a Claude session promotes the swing at its own cast time, keys
   the effects to its cues, and checks it in the lab, then in Studio.
3. **Brief as a blocking pass.** Named poses on a fixed timeline won here. Skip polish
   passes; spend the budget on more blocks.
4. **Rerun when the account has balance,** if the polish question still matters.
