"""
TP2 - Exercise 1 - Tests for moves.py (GIVEN)

Run:  python3 test_moves.py
Each line says OK or FAIL. A function that is not written yet is reported as
TODO. Do not modify this file: modify moves.py until every line is OK.
"""

import moves

results = {"OK": 0, "FAIL": 0, "TODO": 0}


def check(description, function, args, expected):
    """Call function(*args) and compare the result with expected."""
    try:
        got = function(*args)
    except NotImplementedError:
        status, detail = "TODO", "not written yet"
    except Exception as err:
        status, detail = "FAIL", f"raised {type(err).__name__}: {err}"
    else:
        if got == expected:
            status, detail = "OK", ""
        else:
            status, detail = "FAIL", f"expected {expected!r}, got {got!r}"
    results[status] += 1
    print(f"[{status:4}] {description:55} {detail}")


W = frozenset({(1, 0), (2, 2)})

print("--- Part A: from a click to a cell")
check("pixel_to_cell(250, 30, 100)", moves.pixel_to_cell, (250, 30, 100), (0, 2))
check("pixel_to_cell(0, 0, 110)", moves.pixel_to_cell, (0, 0, 110), (0, 0))
check("pixel_to_cell(439, 439, 110) - last pixel", moves.pixel_to_cell, (439, 439, 110), (3, 3))
check("pixel_to_cell(110, 219, 110) - on a border", moves.pixel_to_cell, (110, 219, 110), (1, 1))
check("is_inside((0, 0))", moves.is_inside, ((0, 0),), True)
check("is_inside((3, 3))", moves.is_inside, ((3, 3),), True)
check("is_inside((4, 0))", moves.is_inside, ((4, 0),), False)
check("is_inside((0, -1))", moves.is_inside, ((0, -1),), False)

print("--- Part B: distances and neighbours")
check("manhattan((0, 0), (2, 3))", moves.manhattan, ((0, 0), (2, 3)), 5)
check("manhattan((3, 1), (1, 2))", moves.manhattan, ((3, 1), (1, 2)), 3)
check("manhattan((2, 2), (2, 2))", moves.manhattan, ((2, 2), (2, 2)), 0)
check("is_neighbour((1, 1), (0, 1)) - above", moves.is_neighbour, ((1, 1), (0, 1)), True)
check("is_neighbour((1, 1), (1, 2)) - right", moves.is_neighbour, ((1, 1), (1, 2)), True)
check("is_neighbour((1, 1), (2, 2)) - diagonal", moves.is_neighbour, ((1, 1), (2, 2)), False)
check("is_neighbour((1, 1), (1, 1)) - itself", moves.is_neighbour, ((1, 1), (1, 1)), False)
check("is_neighbour((0, 0), (0, 2)) - too far", moves.is_neighbour, ((0, 0), (0, 2)), False)

print("--- Part C: walking step by step")
check("next_step((0, 0), (2, 3))", moves.next_step, ((0, 0), (2, 3)), (1, 0))
check("next_step((2, 0), (2, 3))", moves.next_step, ((2, 0), (2, 3)), (2, 1))
check("next_step((3, 3), (0, 3))", moves.next_step, ((3, 3), (0, 3)), (2, 3))
check("next_step((1, 2), (1, 0))", moves.next_step, ((1, 2), (1, 0)), (1, 1))
check("next_step((1, 1), (1, 1))", moves.next_step, ((1, 1), (1, 1)), (1, 1))
check("build_path((0, 0), (1, 2))", moves.build_path, ((0, 0), (1, 2)), [(1, 0), (1, 1), (1, 2)])
check("build_path((3, 3), (2, 1))", moves.build_path, ((3, 3), (2, 1)), [(2, 3), (2, 2), (2, 1)])
check("build_path((2, 2), (2, 2))", moves.build_path, ((2, 2), (2, 2)), [])

print("--- Part D: walls")
check("path_is_free([(0, 1), (1, 1)], W)", moves.path_is_free, ([(0, 1), (1, 1)], W), True)
check("path_is_free([(0, 0), (1, 0)], W)", moves.path_is_free, ([(0, 0), (1, 0)], W), False)
check("path_is_free([], W)", moves.path_is_free, ([], W), True)
check("build_path_columns_first((0, 0), (1, 2))", moves.build_path_columns_first,
      ((0, 0), (1, 2)), [(0, 1), (0, 2), (1, 2)])
check("build_path_columns_first((3, 3), (1, 3))", moves.build_path_columns_first,
      ((3, 3), (1, 3)), [(2, 3), (1, 3)])

print("--- Part E: move")
check("move jump (0,0) -> (3,2)", moves.move, ((0, 0), (3, 2), "jump"), [(3, 2)])
check("move jump outside the grid", moves.move, ((0, 0), (4, 2), "jump"), [])
check("move jump on itself", moves.move, ((1, 1), (1, 1), "jump"), [])
check("move neighbour (0,0) -> (0,1)", moves.move, ((0, 0), (0, 1), "neighbour"), [(0, 1)])
check("move neighbour (0,0) -> (1,1) refused", moves.move, ((0, 0), (1, 1), "neighbour"), [])
check("move walk (0,0) -> (2,1)", moves.move, ((0, 0), (2, 1), "walk"), [(1, 0), (2, 0), (2, 1)])
check("move walls (0,0) -> (3,1): columns first", moves.move, ((0, 0), (3, 1), "walls", W),
      [(0, 1), (1, 1), (2, 1), (3, 1)])
check("move walls (0,0) -> (0,3): rows first works", moves.move, ((0, 0), (0, 3), "walls", W),
      [(0, 1), (0, 2), (0, 3)])
check("move walls (0,0) -> (2,0): both paths blocked", moves.move, ((0, 0), (2, 0), "walls", W), [])
check("move walls target is a wall", moves.move, ((0, 0), (2, 2), "walls", W), [])

print()
print(f"{results['OK']} OK, {results['FAIL']} FAIL, {results['TODO']} TODO")
