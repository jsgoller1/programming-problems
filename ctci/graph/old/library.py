import random

"""
Creates a list of lists representing the grid. The grid is "size x size" (for the input size parameter),
so the returned list is of length size, as is each sublist within it.
"""
def generate_square_grid(size, maze_difficulty, end_cell):
    grid = [[] for i in range(size)]
    for row in grid:
        for column_index in range(size):  # NOTE: grid[0][0] is the uppermost, leftmost cell of the grid
            if(random.random() < maze_difficulty): # higher maze difficulty will correspond to more blocked cells
                row.append(1)
            else:
                row.append(0)
    grid[end_cell[0]][end_cell[1]] = 0
    grid[0][0] = 0
    return grid

"""
Takes a grid generated by generate_square_grid() and a list representing a shortest path,
and then replaces each entry in the grid contained in the path with a 2.
"""
def fill_grid_with_path(grid, path):
    for row_index, column_index in path:
        grid[row_index][column_index] = 2
    return grid


"""
Borrowed this function from some code I was given for a Udacity project.
I don't entirely understand lambda function syntax for Python yet, but all
show() does is nicely display a grid that is represented using lists of lists
(such as ones generated with generate_square_grid()).
"""
def show(p, text=""):
    rows = ['[' + ','.join(map(lambda x: '{0:d}'.format(x),r)) + ']' for r in p]
    print(text)
    print '[' + ',\n '.join(rows) + ']'
    print("\n")
