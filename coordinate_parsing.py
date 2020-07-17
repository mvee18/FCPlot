import numpy as np
from generatecoordinates import read_first_line

# We are looking for the format [x1, y1, z1 ... xn, yn, zn] for each energy point.

num_atoms = int(read_first_line("fort_files/fort.15")[0])

def parse_coordinates(coordinate, sign):  # 1 means positive, -1 means negative.
    # We can use a numpy array with zero to represent the string of coordinates without any displacement.
    xyz = np.zeros((num_atoms, 3))

    coordinate = np.asarray(coordinate)
    if coordinate.size == 4:
        coordinate = np.reshape(coordinate, (2, 2))

        for entry in coordinate:
            xyz[entry[1]][entry[0]] += 1

    # This is necessary since the second derivatives are backwards... (i.e., a1, c1, a2, c2 instead of c1, a1, c2, a2).
    else:
        for entry in coordinate:
            xyz[entry[0]][entry[1]] += 1

    if sign == 1:
        return xyz.flatten()
    elif sign == -1:
        return np.negative(xyz.flatten())


test1 = [0, 0, 0, 0]  # Outputs [2, 0, 0, 0, 0, 0, 0, 0, 0]
test2 = [1, 1, 1, 1]  # Outputs [0, 0, 0, 0, 2, 0, 0, 0, 0]
test3 = [2, 1, 2, 0]

test4 = [[0, 0], [0, 0], [0, 0]]
test5 = [[2, 0], [1, 0], [0, 0]]

print(parse_coordinates(test5, 1))
