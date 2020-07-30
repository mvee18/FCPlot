import numpy as np
from generatecoordinates import read_first_line
import copy

# We are looking for the format [x1, y1, z1 ... xn, yn, zn] for each energy point.

num_atoms = int(read_first_line("fort_files/fort.15")[0])

def sign_change(array, sign):
    return_coordinates = []
    a = np.argsort(-array, axis=None)
    xyz = copy.deepcopy(array)

    for s in sign:
        for c, value in enumerate(s):
            xyz[a[c]] = xyz[a[c]] * value

        return_coordinates.append(xyz)
        xyz = copy.deepcopy(array)

    return np.asarray(return_coordinates)


def parse_coordinates(coordinate, sign):  # 1 means positive, -1 means negative.
    # We can use a numpy array with zero to represent the string of coordinates without any displacement.
    xyz = np.zeros((num_atoms, 3))

    coordinate = np.asarray(coordinate)
    if coordinate.size == 4:
        coordinate = np.reshape(coordinate, (2, 2))

        for entry in coordinate:
            xyz[entry[0]][entry[1]] += 1

    # This is necessary since the second derivatives are backwards... (i.e., a1, c1, a2, c2 instead of c1, a1, c2, a2).
    # Actually, they're not. So who's right here...?
    else:
        for entry in coordinate:
            xyz[entry[0]][entry[1]] += 1

    xyz = xyz.flatten()
    coordinates_list = sign_change(xyz, sign)

    return coordinates_list

# Test Data
# test1 = [0, 0, 0, 0]  # Outputs [2, 0, 0, 0, 0, 0, 0, 0, 0]
# test2 = [1, 1, 1, 1]  # Outputs [0, 0, 0, 0, 2, 0, 0, 0, 0]
# test3 = [2, 1, 2, 0]
# test3_signs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

# test4 = [[0, 0], [0, 0], [0, 0]]
# test4_signs = [(1,), (1/2,), (0,), (-1/2,), (-1,)]
# test5 = [[2, 0], [1, 0], [0, 0]]

# test6 = [[2, 0], [2, 0], [0, 0]]
# triple_double_signs = [(1, 1), (0, 1), (-1, 1), (1, -1), (0, -1), (-1, -1)]

# test_sign4 = [(1,), (1 / 3,), (-1 / 3,), (-1,)]

# fourth1 = [[2, 0], [2, 0], [2, 0], [0, 0]]
# fourth_triple_signs = [(1, 1), (1/3, 1), (-1/3, 1), (-1, 1), (1, -1), (1/3, -1), (-1/3, -1), (-1, -1)]
