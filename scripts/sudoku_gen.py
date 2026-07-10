import random

def pattern(r, c, base=3):
    side = base * base
    return (base * (r % base) + r // base + c) % side

def shuffled(seed_rng, s):
    s = list(s)
    seed_rng.shuffle(s)
    return s

def make_solution(rng, base=3):
    side = base * base
    r_base = range(base)
    rows = [g * base + r for g in shuffled(rng, r_base) for r in shuffled(rng, r_base)]
    cols = [g * base + c for g in shuffled(rng, r_base) for c in shuffled(rng, r_base)]
    nums = shuffled(rng, range(1, side + 1))
    grid = [[nums[pattern(r, c, base)] for c in cols] for r in rows]
    return grid

def count_solutions(grid, limit=2):
    n = 9
    grid = [row[:] for row in grid]
    count = 0

    def find_empty():
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    return r, c
        return None

    def valid(r, c, v):
        for i in range(n):
            if grid[r][i] == v or grid[i][c] == v:
                return False
        br, bc = 3*(r//3), 3*(c//3)
        for rr in range(br, br+3):
            for cc in range(bc, bc+3):
                if grid[rr][cc] == v:
                    return False
        return True

    def backtrack():
        nonlocal count
        if count >= limit:
            return
        pos = find_empty()
        if pos is None:
            count += 1
            return
        r, c = pos
        for v in range(1, 10):
            if valid(r, c, v):
                grid[r][c] = v
                backtrack()
                grid[r][c] = 0
                if count >= limit:
                    return

    backtrack()
    return count

def make_puzzle(rng, solution, target_givens=34, min_per_line=2):
    n = 9
    puzzle = [row[:] for row in solution]
    cells = [(r, c) for r in range(n) for c in range(n)]
    rng.shuffle(cells)
    givens = 81

    def row_count(g, r): return sum(1 for c in range(9) if g[r][c] != 0)
    def col_count(g, c): return sum(1 for r in range(9) if g[r][c] != 0)

    for r, c in cells:
        if givens <= target_givens:
            break
        if row_count(puzzle, r) <= min_per_line or col_count(puzzle, c) <= min_per_line:
            continue
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        if count_solutions(puzzle, limit=2) == 1:
            givens -= 1
        else:
            puzzle[r][c] = backup
    return puzzle, givens

best = None
for seed in range(200):
    rng = random.Random(seed)
    solution = make_solution(rng)
    puzzle, givens = make_puzzle(rng, solution, target_givens=34, min_per_line=2)
    rows_ok = all(sum(1 for c in range(9) if puzzle[r][c]!=0) >= 2 for r in range(9))
    cols_ok = all(sum(1 for r in range(9) if puzzle[r][c]!=0) >= 2 for c in range(9))
    if givens <= 36 and rows_ok and cols_ok:
        best = (seed, solution, puzzle, givens)
        break

if best:
    seed, solution, puzzle, givens = best
    print("seed", seed, "givens", givens)
    print("Solution:")
    for row in solution: print(row)
    print("Puzzle:")
    for row in puzzle: print(row)
    print("row counts:", [sum(1 for c in range(9) if puzzle[r][c]!=0) for r in range(9)])
    print("col counts:", [sum(1 for r in range(9) if puzzle[r][c]!=0) for c in range(9)])
else:
    print("none found")
