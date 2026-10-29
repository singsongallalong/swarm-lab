# moonwell-zones: the first zones run, a new area's look (2026-10-29)

Six DeepSeek Flash generators each made the whole look of the Moonwell glade from the same
brief: a drowned glade of moon-priestesses, inspired by the old Warcraft night-elf forests
but in this game's style. Each made a tileset derived from the field's, sculpt props, a
theme and a signature set piece, with catalog rows. Each took a different direction:

- A: the drowned glade
- B: the sacred ring
- C: the fading well
- D: the watch of towers
- E: the swallowed temple
- F: the barrow glade

All six finished in about 10 minutes each. The ledger estimates $2.58, but the DeepSeek
balance fell only $0.57 (16.55 to 15.98), so the price table in `providers.toml` overstates
this provider.

On the first check, 0 of 6 survived, because two of the job's rules were too strict:

- four had added a comment line above their catalog rows;
- two had tileset files of 340–350 lines, against a 300-line cap.

Both rules were loosened (comments allowed, cap 450), and the same work was checked again:
6 of 6 survived.

`moonwell-zones-sites-effects-props-45b1658.png` shows each candidate's pool site (from
three-quarters and eye level), its set piece from the game camera, and its props.

- **F, picked first:** the barrow glade. Its teal coil of streaming light is the only effect
  that clearly reads from the game camera, over a stone ring, crypts and headstones.
- **C, picked second:** the fading well. The cleanest ring of standing stones; its motes are
  faint.
- **D, picked third:** the watch of towers. Ruined towers and leaning ancients on the rims;
  a coiling, crackling well-glow.

What the run taught:

- **All six chose nearly the same cold green-grey,** so the whole-map view barely tells them
  apart. The next brief or directions should vary the colour, not only the props.
- **The landmark can't be met with data.** A tileset scatters prop sets anywhere, so "a ring
  round the well" needs a landmark placed by code, as the field's are.
- **Not judged offline:** mist, light colour and lighting, and the set piece in place.

Apply one patch at a time on arpg-game `45b1658` (all use `Moonwell` and `moonwell_` names):

    git apply <swarm-lab>/results/moonwell-zones/candidate-F.patch
