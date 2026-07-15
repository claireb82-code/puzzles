# Daily Puzzles

A personal rotating daily logic puzzle — nonogram, word logic, sudoku — built as
self-contained HTML files (no build step, no dependencies).

**Play it live: <https://claireb82-code.github.io/puzzles/>**

Every puzzle is procedurally generated client-side, seeded from the current UTC date.
Same date → same puzzle for everyone; a new date → a fresh puzzle, even for a type you've
seen before. Nothing is stored server-side and there's no build step — open a file and the
puzzle for today generates itself in the page.

## Start here

Open [`index.html`](index.html) (or the live link above) — it works out which puzzle type is
up today and links to it, lists all three so you can jump to any of them regardless of the
rotation, and shows the past two weeks' puzzles so you can play any you missed. Every puzzle
page has a ⌂ Home button back to the hub.

## Archive

Because puzzles are generated deterministically from their date, any past day's puzzle can be
replayed exactly: append `?date=YYYY-MM-DD` to a puzzle URL (the hub's "Past two weeks" list
does this for you). Future or malformed dates fall back to today. Archive plays get their own
progress save, and the page is labelled with the archive date.

## Rotation

Day-of-epoch mod 3 (UTC), so it cycles continuously:

1. **Nonogram** (`nonogram.html`) — "Picture Logic". 15×15 grid-fill, several shape clusters
   scattered across the grid, drag-to-fill, live hint/mistake button, auto-marks a line once
   it's fully solved (and retracts those marks if you undo a fill — your own ✕s are never
   touched). Every row and column has at least one filled cell.
2. **Word logic** (`wordlogic.html`) — "Desk Neighbors". 4 people × pet × drink, staircase
   elimination grid with the clue list alongside it (confirm/eliminate cells, right-click to
   quick-eliminate; un-confirming a cell also undoes the eliminations it auto-added), live
   hint/mistake button.
3. **Sudoku** (`numberlogic.html`) — "Nine". Classic 9×9, 32 givens, keyboard/keypad entry,
   live row/column/box conflict highlighting and peer highlighting, keypad digits grey out
   once fully placed, live hint/mistake button.

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
- **Nonogram** — stamps 3–5 small overlapping rectangles into each of 5 diagonally-spread
  bands to form a grid, then runs the clues through a line-propagation constraint solver to
  a fixpoint. If every cell ends up determined, that assignment was logically forced at every
  step — which proves both that it's solvable without guessing *and* that the solution is
  unique. Candidate grids are rejected if any row/column is completely blank (free auto-solved
  lines) or if the solver converges in fewer than 4 passes (too easy — no cross-referencing
  needed); it retries with a new grid until one qualifies.

`scripts/sudoku_gen.py` is the original Python prototype used to validate the sudoku approach
before porting it to the in-browser JS generator — kept for reference, not used at runtime.

## Playing

Open `index.html` for the daily hub, or open any puzzle's `.html` file directly to play that
type regardless of what's "due" today — everything runs client-side.

## Testing

Open `tests.html` in a browser (needs to be served over HTTP, e.g. `python3 -m http.server`,
since it loads the puzzle pages in iframes — it also runs on the live site). It runs 49 tests
against the live page code: pure-function unit tests, determinism checks (including a guard
that generators never touch unseeded `Math.random`), generator invariants across dozens of
seeds (uniqueness, solvability, no blank lines, given counts), rotation math, UI behavior
(win/reset/hint flows, conflict marking, cascade undo, keypad state), and persistence
round-trips (save/reload/restore, reset-clears-save). Persistence tests use a dedicated TEST
storage key via `?persisttest=1`, and all other UI tests load frames with `?nosave=1`, so a
test run never touches your real daily progress.

## Progress saving

Each puzzle saves its state to `localStorage` on every move (keyed by puzzle type + the date
being played, so archive games have their own saves too). A reload or accidental tab close
picks up exactly where you left off, including the timer. Reset clears the save; saves older
than ~35 days are purged automatically.

## Roadmap

- [x] Word logic puzzle
- [x] Sudoku puzzle
- [x] Procedural daily generation for all three types
- [x] Day-rotation hub page (`index.html`)
- [x] In-browser test harness (`tests.html`)
- [x] localStorage persistence (state + timer survive same-day reloads)
- [x] Home button on every puzzle page
- [x] Archive: replay any past day's puzzle via `?date=` + hub list of the past two weeks
