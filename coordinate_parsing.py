import numpy as np
from generatecoordinates import read_first_line

# We are looking for the format [x1, y1, z1 ... xn, yn, zn] for each energy point.

def parse_coordinates(coordinate):
    num_atoms = int(read_first_line("fort_files/fort.15")[0])
    # We can use a numpy array with zero to represent the string of coordinates without any displacement.
    xyz = np.zeros((num_atoms, 3))

    if len(coordinate) == 4:
        coordinate = np.asarray(coordinate)
        coordinate = np.reshape(coordinate, (2, 2))

        for entry in coordinate:
            xyz[entry[1]][entry[0]] += 1

    # This is necessary since the second derivatives are backwards... (i.e., a1, c1, a2, c2 instead of c1, a1, c2, a2).
    else:
        for entry in coordinate:
            xyz[entry[0]][entry[1]] += 1

    return xyz.flatten()


test1 = [0, 0, 0, 0]
test2 = [1, 1, 1, 1]
test3 = [2, 1, 2, 0]

test4 = [[0, 0], [0, 0], [0, 0]]
test5 = [[2, 0], [1, 0], [0, 0]]

xyz_new = parse_coordinates(test3)
print(xyz_new)