### What particles are for in this game

A look is made of two things: **drawn parts** (the kinds above: stones, rings, cracks,
cones) and **particle bursts** (an `Emitters` row, fired by the look). They do
different jobs, and the best looks use both:

- **Parts give shape.** They carry the silhouette that reads from the high camera: where
  the area is, how far it reaches, its edge. But every part counts against the phone
  budget (SE3), and parts alone tend to read as hard, plastic and flat (SE6).
- **Particles give volume, haze and life, for free.** A burst costs no parts and no
  script time (skill-effects.md, "Particles before parts"). It's how a look gets depth
  in the side view (SE6), a soft body around a hard core, matter that tells the truth
  (SE9: frost or rime where cold lands, dust only where something meets the ground), and
  an after-beat that lingers once the parts have faded.
- **The failure to avoid is particles nobody sees.** The art passes learned this the
  hard way: worn effects' first pass was "mostly invisible from the game camera"
  (A28-D10), and "a loose cloud of small soft things is read by brightness" (A31). Few,
  big, half-lit puffs beat many small dim ones. The opposite failure is real too:
  puffs so big they cover the fight (A34: at twice the size "the motes cover the husk";
  SE10).

### Sizes that read (measured)

Measured in this game's own preview on Cold Snap's 8-stud circle at power 0, one look
with the same frost emitter at several sizes (`docs/measurements/` in swarm-lab):

| A puff's size at the end of its life, after the kind's scale (below) | At the game camera |
|---|---|
| 0.6 studs | gone |
| 1.2 studs (what `SlamDust` gives a Wave or Rocks look today) | specks |
| 2.4 studs | reads as distinct puffs |
| 2.4 studs with `lightEmission = 0.5` | reads clearly at night: the biggest single gain |

So: **aim for about 2 to 3 studs at end of life after the kind's scale, half-lit**
(`lightEmission` about 0.5, `lightInfluence` about 0.5; Cave-in's dust is "half lit so
it shows at night", A33). Keep `transparency` starting near 0.25 to 0.35 and fading to 1.
Remember the preview flatters faint particles (A31-D9): if a burst is only just visible
in your render, it will be invisible in the game, so aim above the minimum.

### Where your particles fire depends on the kind

You don't place particles: the look's kind does, by the game's own rule (quoted below).
Choose the kind for where you want the particles, not only for its parts:

- **Wave:** only at every other point of its **outer edge**, at the moment the front
  arrives, at half scale. Measured: even good puffs here make a dotted ring at the edge
  late in the look, never a haze or a cloud.
- **Rocks:** a puff at every `every`th stone, at half scale, as it heaves; **plus its own
  `burst` field: one full-scale burst at the middle at the very start**
  (`burstScale` sizes it; it can grow with power through `perPower.burstScale`). This is
  the strongest particle lever in the system. Measured: a burst sitting among the
  stones is hidden by them from the game camera; one that **rises** (speed about 10 to
  16, upward acceleration, a narrow spread) shows as a column above them from 0.3 s and
  lingers after they sink. At power 8 the stones grow and swallow a burst that doesn't
  grow too, so give `burstScale` its own `perPower` share (Cave-in, A33).
- **Fissures:** at each crack's far end, at 0.4 scale.
- **Bolt, Arc:** once where it strikes, at once.
- **Gust:** once, part way along, as it nears the edge, sized to the area.
- **Flames:** six puffs round the edge as the fire reaches it.
- **Fan:** at each ray's far end.

### How to check your particles worked

- The preview's last line says `<n> parts, <m> particles`. **`0 particles` means your
  emitter never fired:** a missing or misnamed row, or a kind that has no `emitter`.
- Look at the frames after the hit (0.2 s and later): that's when most bursts are alive.
  Check the side view for height and volume.
- Compare against your own look without the particles in your head: if you couldn't tell
  the difference at the game camera, they aren't doing their job yet.
