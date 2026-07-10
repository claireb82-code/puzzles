# Daily Puzzles

A personal rotating daily logic puzzle — nonogram, word logic, number logic — built as
self-contained HTML files (no build step, no dependencies).

## Rotation

1. **Nonogram** — picture logic, clue-driven grid fill
2. **Word logic** — logic-grid deduction (people/items/attributes, cross-elimination clues)
3. **Sudoku** — classic 9×9 number placement

Repeats weekly.

## Files

- `nonogram.html` — Day 1. 15×15, medium-hard, drag-to-fill, live hint/mistake button,
  auto-marks a line once it's fully solved.
- `wordlogic.html` — Day 2. "Desk Neighbors": 4 people × pet × drink, staircase elimination
  grid (confirm/eliminate cells, right-click to quick-eliminate), live hint/mistake button.
  Clue set is hand-verified to be uniquely solvable by pure elimination, no guessing.
- `numberlogic.html` — Day 3. "Nine": classic 9×9 sudoku, keyboard/keypad number entry, live
  row/column/box conflict highlighting and peer highlighting, live hint/mistake button.
  Solution and 34-given puzzle were generated with a script and verified unique via a
  backtracking solution counter (see `scripts/sudoku_gen.py`).

## Playing

Open the `.html` file directly in a browser — everything runs client-side.

## Roadmap

- [x] Word logic puzzle (Day 2)
- [x] Number logic puzzle (Day 3)
- [ ] Optional: scheduled generation so a new puzzle is ready each morning
