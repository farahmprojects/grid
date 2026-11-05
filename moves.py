"""
TP2 - Exercise 1 - Moving a character on a 4 x 4 grid
=======================================================

THIS IS THE ONLY FILE YOU HAVE TO EDIT.

The window (grid_gui.py) is given: it draws the grid and the character, and
every time you click on a cell it calls the functions below. Replace each
`raise NotImplementedError` with your own code, then run:

    python3 test_moves.py     # checks your functions, without any window
    python3 grid_gui.py       # opens the window

Conventions used everywhere in this file
----------------------------------------
* A cell is a tuple (row, col). Rows go from top to bottom, columns from
  left to right, both start at 0. The top-left cell is (0, 0) and the
  bottom-right cell is (3, 3).
* The character starts on (0, 0).
* `walls` is a set of cells the character is not allowed to enter.
"""


GRID_SIZE = 4


# ---------------------------------------------------------------------------
# Part A - From a click to a cell
# ---------------------------------------------------------------------------


"""
Réponses aux questions de la Partie A: 
    
    
Question 1:

// est la division entière. x donne la colonne et y la ligne,
car x est horizontal et y vertical.


Question 2:

(4, 0) et (0, -1) renvoient False car ces cellules sont hors grille.
"""


def pixel_to_cell(x, y, cell_size):
    
    """Convert the coordinates (x, y) of a mouse click, in pixels, into a cell.

    x is the horizontal position (it gives the column), y is the vertical one
    (it gives the row). Each cell is a square of cell_size pixels.
    Example with cell_size = 100: (250, 30) -> (0, 2).
    Returns the tuple (row, col).
    """
    
    col = x // cell_size
    row = y // cell_size
    return (row, col)


def is_inside(cell, size=GRID_SIZE):
    
    """Return True if cell = (row, col) lies on a grid of size x size cells."""
    
    row, col = cell 
    if 0 <= row < size and 0 <= col < size : 
        return True 
    else : 
        return False


# ---------------------------------------------------------------------------
# Part B - Distances and neighbours
# ---------------------------------------------------------------------------


"""
Réponses aux questions de la Partie B: 
    

Question 4:

La distance entre (0, 0) et (3, 3) est 3 + 3 = 6.


Question 5:

Deux cellules sont voisines si leur distance vaut 1.
Les diagonales valent 2 et une cellule elle-même vaut 0.


Question 6:

Il faut au minimum 6 clics : 3 vers le bas et 3 vers la droite.
"""


def manhattan(a, b):
    
    """Return the Manhattan distance between two cells:
    |row_a - row_b| + |col_a - col_b|. It is the number of single steps
    (up, down, left, right) needed to go from a to b.
    """
    
    row_a, col_a = a
    row_b, col_b = b
    return abs(row_a - row_b) + abs(col_a - col_b)
    

def is_neighbour(a, b):
    
    """Return True if b is directly above, below, left or right of a
    (diagonals do NOT count, and a cell is not its own neighbour)."""

    
    if manhattan(a,b) == 1 :
        return True
    else : 
        return False


# ---------------------------------------------------------------------------
# Part C - Walking step by step
# ---------------------------------------------------------------------------


"""
Réponses aux questions de la Partie C: 
    
Question 7:

next_step avance d'une case, d'abord en ligne puis en colonne.
Si la cible est atteinte, la fonction renvoie la cellule actuelle.


Question 8:

La boucle s'arrête car la distance diminue de 1 à chaque étape.
La longueur du chemin est égale à la distance de Manhattan.


Question 9:

Steps walked correspond à la longueur du chemin,
donc à la distance de Manhattan sans murs.
"""


def next_step(current, target):
    """Return the cell reached after ONE step from current towards target.

    Rule: first fix the row (move up or down by one), and only when the row
    is right, fix the column (move left or right by one).
    If current == target, return current unchanged.
    Example: next_step((0, 0), (2, 3)) -> (1, 0)
             next_step((2, 0), (2, 3)) -> (2, 1)
    """
    
    row_c, col_c = current
    row_t, col_t = target
        
    if row_c < row_t:
        return (row_c + 1, col_c)
    elif row_c > row_t: 
        return (row_c - 1, col_c)
    elif col_c < col_t: 
        return (row_c, col_c + 1) 
    elif col_c > col_t: 
        return (row_c, col_c -1)
    else : 
        return current 
    

def build_path(start, target):
    """Return the list of the cells visited to go from start to target,
    WITHOUT start and WITH target. Use next_step in a while loop.
    Example: build_path((0, 0), (1, 2)) -> [(1, 0), (1, 1), (1, 2)]
    build_path(c, c) -> []
    """
    
    path = []
    while start != target:
        start = next_step(start, target)
        path.append(start)

    return path


# ---------------------------------------------------------------------------
# Part D - Walls
# ---------------------------------------------------------------------------


"""
Réponses aux questions de la Partie D: 
    
Question 10:

Un set est plus rapide qu'une liste pour rechercher une cellule
avec in : O(1) en moyenne contre O(n).


Question 11:

La fonction modifie d'abord la colonne, puis la ligne.


Question 12:

Le programme essaie le chemin ligne d'abord, puis colonne.
Si les deux traversent un mur, le déplacement est refusé.


Question 13:

Les deux chemins passent par le mur (1, 0).
Pourtant, on peut le contourner par (0, 1), (1, 1), (2, 1),
puis (2, 0). La stratégie teste seulement deux chemins et peut
donc refuser un déplacement pourtant possible.
"""


def path_is_free(path, walls):
    """Return True if no cell of the list path belongs to the set walls."""
    
    for cell in path:
        if cell in walls:
            return False
    return True


def build_path_columns_first(start, target):
    """Same as build_path, but fix the COLUMN first, then the row.
    Example: build_path_columns_first((0, 0), (1, 2)) -> [(0, 1), (0, 2), (1, 2)]
    """
    row_s, col_s = start
    row_t, col_t = target
    path = []
    while col_s != col_t:
        if col_s < col_t:
            col_s += 1
        else:
            col_s -= 1
        path.append((row_s, col_s))

    while row_s != row_t:
        if row_s < row_t:
            row_s += 1
        else:
            row_s -= 1
        path.append((row_s, col_s))

    return path


# ---------------------------------------------------------------------------
# Part E - The function called by the window
# ---------------------------------------------------------------------------


def move(current, target, mode, walls=frozenset()):
    """Decide where the character goes when the user clicks on target.

    Returns the list of cells the window must animate, one after the other
    (without current). An EMPTY list means "the move is refused".

    mode is one of the strings chosen with the radio buttons of the window:
      "jump"      : the character jumps directly to target -> [target]
      "neighbour" : allowed only if target is a neighbour of current
      "walk"      : the character walks with build_path
      "walls"     : like "walk", but the path must avoid walls: try
                    build_path, then build_path_columns_first; if both
                    cross a wall, refuse the move.

    In every mode, refuse a target that is outside the grid, that is a wall,
    or that is the current cell.
    """
    
# ---------------------------------------------------------------------------
#tous les modes
# ---------------------------------------------------------------------------

    if not is_inside(target,size=GRID_SIZE) or target == current or target in walls: 
        return []
    
#mode "jump" ------------------------------------------------------------
    if mode == "jump": 
        return [target]
    
#mode "neighbour" -------------------------------------------------------
    if mode == "neighbour": 
        if is_neighbour(current, target):
            return [target] 
        else : 
            return []
    
#mode "walk" ------------------------------------------------------------
    if mode == "walk": 
        return build_path(current, target)

#mode "walls" -----------------------------------------------------------
    if mode == "walls": 
        path = build_path(current, target)

        if path_is_free(path, walls):
            return path

        path = build_path_columns_first(current, target)

        if path_is_free(path, walls):
            return path

        return []