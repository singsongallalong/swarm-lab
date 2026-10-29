## The figure: feminine

This set is worn as a feminine figure. Its outline from the high camera must read as a woman's
before any detail does. The game stays part-built and blocky: that retro look is the point,
so don't try to round anything off. Blocky is fine. **Broad is not.**

What makes a part-built outline read as feminine:

- **A narrow shoulder line.** Nothing on `UpperTorso` or `UpperArm` stands out past the
  shoulders, and nothing out at the shoulders rises above them. No pauldrons, puffed shoulder
  caps, epaulettes or capes draped over the shoulder tops. Square, wide shoulders are what
  make a dress read as armour or as a man's coat.
- **A defined waist.** The bodice is fitted and the waist is the narrowest point: a belt,
  sash, corset lacing or bodice point at the `LowerTorso` draws the eye in.
- **Width low, not high.** The silhouette widens below the waist: a skirt that flares from
  the thighs and keeps widening to the hem, hips, a bustle behind. Read top to bottom, it's
  a narrow top over a wide base: an A, a bell or an hourglass, never a V.
- **Height at the head.** Headdresses, bonnets, veils and hair ornaments may go up and back.
  They may not go wide at ear level, which reads as a helmet.
- **Volume at the forearm.** A sleeve that should feel full flares at the elbow and cuff
  (the Gloves slot, `LowerArm`), not at the shoulder. The upper arm stays close to the arm.
- **Capes and trains hang from the back.** Attach them to the back of `UpperTorso` (+Z),
  below the shoulder top, and let them fall, not over the shoulders' outer edges.

### The shoulder check (a failure means the run is discarded)

This command measures your Chest look on the reference body and fails when it's too broad:

```
$figure_cmd
```

- **Out** is how far a piece reaches sideways past the side of the torso or the outside of
  the upper arm. It must stay at or under **$max_out studs**. A sleeve centred on the
  1-stud arm may be up to 1.3 studs wide.
- **Rise** is how far a piece out at the shoulders stands above the top of the torso or the
  arm. It must stay at or under **$max_rise studs**. A collar inside the neck's width may
  rise freely.

It names the piece that's over. Narrow it, lower it, or move its volume down to the waist,
hips or hem. Run it with the other checks, after every revision.

### Bodies

Players wear their own avatars, from the blocky classic body to slim ones. Look at the
`fit` render's slimmer avatar as closely as at the main one: the set must still read as
feminine there, with no gaps at the waist and nothing poking out at the shoulders.
