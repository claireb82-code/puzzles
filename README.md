# Daily Puzzles

A personal rotating daily logic puzzle — nonogram, word logic, sudoku — built as
self-contained HTML files (no build step, no dependencies).

Every puzzle is procedurally generated client-side, seeded from the current UTC date.
Same date → same puzzle for everyone; a new date → a fresh puzzle, even for a type you've
seen before. Nothing is stored server-side and there's no build step — open a file and the
puzzle for today generates itself in the page.

## Start here

Open [`index.html`](index.html) — it works out which puzzle type is up today and links to it,
plus lists all three so you can jump to any of them regardless of the rotation.

## Rotation

Day-of-epoch mod 3 (UTC), so it cycles continuously:

1. **Nonogram** (`nonogram.html`) — "Picture Logic". 15×15 grid-fill, three blob shapes
   stamped onto the grid, drag-to-fill, live hint/mistake button, auto-marks a line once
   it's fully solved.
2. **Word logic** (`wordlogic.html`) — "Desk Neighbors". 4 people × pet × drink, staircase
   elimination grid (confirm/eliminate cells, right-click to quick-eliminate), live
   hint/mistake button.
3. **Sudoku** (`numberlogic.html`) — "Nine". Classic 9×9, 32 givens, keyboard/keypad entry,
   live row/column/box conflict highlighting and peer highlighting, live hint/mistake button.

## How the generation is verified

Each file seeds a small deterministic PRNG (`xmur3` + `mulberry32`) from a puzzle-type salt
plus today's ISO date, so the puzzle is reproducible for a given day without a server. On top
of that, each generator proves its own output is soundly unique before showing it to you:

- **Sudoku** — builds a solved grid via the standard band/stack-shuffle method, then carves
  givens out one at a time, keeping a removal only if a backtracking solver (capped at 2
  solutions) still finds exactly one.
- **Word logic** — builds a pool of true statements about a randomized person/pet/drink
  assignment (deliberately excluding direct "X has Y" giveaways), then greedily drops clues
  while brute-force checking all 576 possible assignments still yield exactly one match.
- **Nonogram** — stamps 2–4 overlapping rectangles into 3 diagonally-spread bands to form a
  grid, then runs the clues through a line-propagation constraint solver to a fixpoint. If
  every cell ends up determined, that assignment was logically forced at every step — which
  proves both that it's solvable without guessing *and* that the solution is unique. If a
  generated grid doesn't converge (rare), it retries with a new one.

`scripts/sudoku_gen.py` is the original Python prototype used to validate the sudoku approach
before porting it to the in-browser JS generator — kept for reference, not used at runtime.

## Playing

Open `index.html` for the daily hub, or open any puzzle's `.html` file directly to play that
type regardless of what's "due" today — everything runs client-side.

## Testing

Open `tests.html` in a browser (needs to be served over HTTP, e.g. `python3 -m http.server`,
since it loads the puzzle pages in iframes). It runs ~40 tests against the live page code:
pure-function unit tests, determinism checks (including a guard that generators never touch
unseeded `Math.random`), generator invariants across dozens of seeds (uniqueness, solvability,
no blank lines, given counts), rotation math, and UI behavior (win/reset/hint flows, conflict
marking, cascade undo, keypad state). No build step or test framework — same philosophy as
the puzzles.

## Progress saving

Each puzzle saves its state to `localStorage` on every move (keyed by puzzle type + date),
so a reload or accidental tab close within the same day picks up exactly where you left off,
including the timer. Reset clears the save; old days' saves are purged automatically.

## Roadmap

- [x] Word logic puzzle
- [x] Sudoku puzzle
- [x] Procedural daily generation for all three types
- [x] Day-rotation hub page (`index.html`)
- [x] In-browser test harness (`tests.html`)
- [x] localStorage persistence (state + timer survive same-day reloads)
