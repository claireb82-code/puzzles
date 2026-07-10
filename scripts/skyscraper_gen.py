import random
from itertools import permutations

N = 5

def view_count(seq):
    count = 0
    tallest = 0
    for v in seq:
        if v > tallest:
            count += 1
            tallest = v
    return count

def clues_from_grid(grid):
    n = len(grid)
    top = [view_count([grid[r][c] for r in range(n)]) for c in range(n)]
    bottom = [view_count([grid[r][c] for r in range(n-1,-1,-1)]) for c in range(n)]
    left = [view_count(grid[r]) for r in range(n)]
    right = [view_count(grid[r][::-1]) for r in range(n)]
    return top, bottom, left, right

def gen_latin_square(n, tries=2000):
    for _ in range(tries):
        rows = []
        cols_used = [set() for _ in range(n)]
        ok = True
        base = list(range(1, n+1))
        for r in range(n):
            random.shuffle(base)
            # try to find a permutation for this row consistent with columns used
            found = None
            perms = list(permutations(base))
            random.shuffle(perms)
            for p in perms:
                if all(p[c] not in cols_used[c] for c in range(n)):
                    found = p
                    break
            if found is None:
                ok = False
                break
            rows.append(list(found))
            for c in range(n):
                cols_used[c].add(found[c])
        if ok:
            return rows
    return None

def all_latin_squares(n):
    # backtracking generator for all n x n latin squares (rows are permutations, columns distinct)
    results = []
    rows = []
    cols_used = [set() for _ in range(n)]
    all_perms = list(permutations(range(1, n+1)))

    def backtrack(r):
        if r == n:
            results.append([row[:] for row in rows])
            return
        for p in all_perms:
            if all(p[c] not in cols_used[c] for c in range(n)):
                rows.append(list(p))
                for c in range(n):
                    cols_used[c].add(p[c])
                backtrack(r+1)
                rows.pop()
                for c in range(n):
                    cols_used[c].discard(p[c])
    backtrack(0)
    return results

random.seed(42)
grid = gen_latin_square(N)
print("Solution grid:")
for row in grid:
    print(row)

top, bottom, left, right = clues_from_grid(grid)
print("top", top)
print("bottom", bottom)
print("left", left)
print("right", right)

print("Enumerating all latin squares of order", N, "...")
all_squares = all_latin_squares(N)
print("total latin squares:", len(all_squares))

def matches(g, top, bottom, left, right):
    t, b, l, r = clues_from_grid(g)
    return t == top and b == bottom and l == left and r == right

matching = [g for g in all_squares if matches(g, top, bottom, left, right)]
print("matching count with FULL clue set:", len(matching))

print("\n--- Attempting clue reduction ---")

# Represent clues as dict: side -> list of Optional[int] (None = not given)
clue_state = {
    'top': top[:], 'bottom': bottom[:], 'left': left[:], 'right': right[:]
}

def matches_partial(g, state):
    t, b, l, r = clues_from_grid(g)
    for given, actual in [(state['top'], t), (state['bottom'], b), (state['left'], l), (state['right'], r)]:
        for gv, av in zip(given, actual):
            if gv is not None and gv != av:
                return False
    return True

def count_matching(state):
    cnt = 0
    for g in all_squares:
        if matches_partial(g, state):
            cnt += 1
            if cnt > 1:
                return cnt
    return cnt

# list all (side, index) positions
positions = [(side, i) for side in ['top','bottom','left','right'] for i in range(N)]
random.shuffle(positions)

removed = []
for side, i in positions:
    original = clue_state[side][i]
    clue_state[side][i] = None
    if count_matching(clue_state) == 1:
        removed.append((side, i, original))
    else:
        clue_state[side][i] = original  # put it back, still needed

print("Removed", len(removed), "of 20 clues, kept", 20 - len(removed))
print("Final clue state:")
for side in ['top','bottom','left','right']:
    print(side, clue_state[side])

# sanity re-check final uniqueness
print("final unique count:", count_matching(clue_state))
