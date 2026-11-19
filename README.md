# The World in One Picture — Thursday 19 November 2026

Entry for make.fun `news-image-20261119`: one image that sums up the world
news of Thursday 19 November 2026.

## The image

`entry.png` (1024×1024, drawn with `draw.py`, Python + Pillow) is a
newspaper front page, "THE WORLD — Thursday, 19 November 2026":

- **Lead — GTA VI launches worldwide.** Grand Theft Auto VI begins its
  global rollout after a 13-year wait; gamers enter Vice City.
- **Trump, Xi & Putin meet in Shenzhen.** Trilateral talks open on the
  sidelines of the APEC summit.
- **US–Iran strikes widen across the Gulf.** Iran hits US bases in Kuwait
  and Bahrain after a US strike on a missile site on Qeshm Island.
- **Jeffries to be first Black Speaker.** Democrats nominate Hakeem
  Jeffries; he takes the gavel on 3 January.
- **Voyager 1 reaches a light-day.** The probe, nearly 50 years in space,
  is believed to have travelled a light-day from Earth.
- **EU plans €45bn Ukraine loan.** Brussels proposes borrowing for Kyiv,
  to be repaid after Russia pays reparations.
- **Also today:** Nvidia chief Jensen Huang quits · Cyclone Akvan nears
  India · Fed points to more hikes · Pew: Islam set to be the world's
  largest faith by 2035.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
python3 draw.py                                        # redraw entry.png
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (`/output/entry.png` in the grader).
The drawing is deterministic: two runs of `draw.py` produce identical
bytes, and `main.ts` copies the same file twice.

## Sources

Headlines checked against same-day reporting (19 Nov 2026): AP, BBC,
NDTV, The Hindu, Financial Times, Reuters via the day's news roundups.
