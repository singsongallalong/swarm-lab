# glade-maps: the first maps run, whole layouts written by generators (2026-10-29)

Six DeepSeek Flash generators each wrote a whole outdoor map as one pure, seeded Luau layout
generator (a drafted map, 578 to 652 lines). It covers the walkable ground, the road, the
rims and the sites, and places the Moonwell's ring of standing stones where its road leads.
The game's own MapDress dresses it in the barrow-glade look from moonwell-zones.

Each took one form:

- A: a spiral
- B: a pale avenue
- C: a drowned causeway
- D: a hub of glades
- E: a broken ring
- F: two hollows

Three finished within 100 turns; the other three were resumed for 30 more. One was first
rejected for adding a sculpt in the file's own after-the-table style (`Sculpts.x = {`);
the row reader now accepts it. In the end, 6 of 6 passed:

- every seed a sound map;
- the same map for the same seed, and a different one for each seed;
- inside the phone budget once dressed;
- purity, catalog, lint and format.

The ledger estimates $3.93; the DeepSeek balance fell $0.90 (15.98 to 15.08).

`glade-maps-top-seeds1-3-landmark-166b53d.png` shows each map from above on seeds 1, 2 and 3,
and its landmark up close.

- **A, picked first:** the spiral, a road coiling in to the well at the heart.
- **D, picked second:** the hub of glades. A star of glades round the well, and the most
  varied from seed to seed.
- **B, picked third:** the pale avenue. A processional road into a round glade whose ring
  holds a pool of teal light: the most beautiful landmark.
- **Passed over:**
  - C, the causeway: a fine chain of islands, but little variety.
  - E, the ring round a dark wood: strong, but the same on every seed.
  - F, the two hollows: closest to a band.

What the run taught:

- **Variety between seeds is the weak point.** Most maps vary in detail more than in shape.
- **100 turns is short** for a whole layout generator.
- **Not yet judged:** play at eye level (room to fight between the spiral's turns), monster
  pack sites and mist. Making a draft a real map is a design question first (arpg-game
  docs/guides/adding-areas.md).

Each patch is the draft alone, on arpg-game `166b53d` plus `docs/map-drafting/0001-drafted-maps.patch`:

    git apply <swarm-lab>/docs/map-drafting/0001-drafted-maps.patch
    git apply <swarm-lab>/results/glade-maps/candidate-A.patch
    lune run scripts/dresspreview whole out.png 3 1 layout=<its name>
