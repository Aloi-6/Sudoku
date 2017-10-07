rows = 'ABCDEFGHI'
cols = '123456789'
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [i+j for i in A for j in B]
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def find_naked_twins(values, ls):
  """
    given a list of units, find naked twins
    args:
      values(dict): a dictionary of the form {'box_name': '123456789', ...}
      ls: a list of lists of units (rows or columns or squares)
  """

  for sub_list in ls:
    unit_values = [x for x in values[unit] for unit in sub_list]
    print(sub_list)
    print("hi")
    exit(0)

 
d = ['4', '5', '8', '2379', '379', '23', '1', '5', '23']
