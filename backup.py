import collections
import itertools

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [i+j for i in A for j in B]
def diag(A, B):
    "Cross product of elements in A and elements in B."
    return [i+j for (i,j) in zip(A, B)]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [diag(rows,cols)] + [diag(rows, cols[::-1])]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #values = find_naked_twins(values, column_units)    
    #values = find_naked_twins(values, row_units)    
    #values = find_naked_twins(values, square_units)    
    #values = find_naked_twins(values, diag_units)    
 
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    #this part of copied from the reviewer
    for unit in unitlist:   
      #Find all boxes with two digits remaining as possiblities 
      pairs = [box for box in unit if len(values[box]) == 2]
      #pairwise combinations
      poss_twins = [list(pair) for pair in itertools.combinations(pairs, 2)]
      #find the naked twins
      for pair in poss_twins:
        box1 = pair[0]
        box2 = pair[1]
        if values[box1] == values[box2]:
          for box in unit:
            #eliminate the naked twins as possibilities for peers
            if box != box1 and box != box2:
              for digit in values[box1]:
                values[box] == values[box].replace(digit,'')
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    EMPTY = '123456789'
    sudoku_grid = {}
    count = 0
    for row in row_units:
        for pos in row:
            val = grid[count]
            if val == '.':
                sudoku_grid[pos] = EMPTY
            else:
                sudoku_grid[pos] = val
            count += 1
 
    return sudoku_grid

def remove_val(grid, units, pos, val):
    for lists in units[pos]:
        for position in lists:
            if position == pos:
                continue
            else:
                grid[position] = grid[position].replace(val, '')
    return grid
                
def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    pass

def eliminate(values):
    for row in row_units:
        for pos in row:
            val = values[pos]
            if len(val) > 1:
                continue
            values = remove_val(values, units, pos, val)
    return values
   

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        #use naked twin
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False: 
        return False
        
    unsolved = [box for box in values.keys() if len(values[box]) > 1]    
    if len(unsolved) == 0: 
        return values


    # Choose one of the unfilled squares with the fewest possibilities
    
    possible = []
    for key, val in values.items():
        if len(val) == 1:
            continue
        possible.append([len(val), key])
    minsize, minunit = min(possible)

    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    
    for val in values[minunit]:
        values_copy = values.copy()
        values_copy[minunit] = val 
        tmp = search(values_copy)
        if tmp:
            return tmp
    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #convert string grid to dictionary grid
    values = grid_values(grid)
    solved = search(values)
    if solved:
      return solved
    else:
      return False
    

if __name__ == '__main__':
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    #diag_sudoku_grid =  '1.4.9..68956.18.34..84.695151.....868..6...1264..8..97781923645495.6.823.6.854179'
    #diag_sudoku_grid = '...8.1.........43.5............7.8........1...2..3....6......75..34........2..6..'
    #diag_sudoku_grid = '2..3..........6.....1...372.......8.....................67.......5...............'
    
    values = solve(diag_sudoku_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
