import numpy as np
from generatecoordinates import read_first_line
import copy

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

    xyz = xyz.flatten()
    coordinates_list = change_signs(xyz, sign)

    return coordinates_list


test1 = [0, 0, 0, 0]  # Outputs [2, 0, 0, 0, 0, 0, 0, 0, 0]
test2 = [1, 1, 1, 1]  # Outputs [0, 0, 0, 0, 2, 0, 0, 0, 0]
test3 = [2, 1, 2, 0]

test4 = [[0, 0], [0, 0], [0, 0]]
test5 = [[2, 0], [1, 0], [0, 0]]
test6 = [[2, 0], [2, 0], [0, 0]]

# Input like [1,1], [1,-1], [-1,1], [-1,-1]

def change_signs(xyz, sign):
    index_list = []
    return_coordinates = []
    xyz_working = copy.deepcopy(xyz)

    for index, number in enumerate(xyz):
        if number != 0:
            index_list.append(index)

    for sign_chart in sign:
        for count, value in enumerate(sign_chart):
            xyz_working[index_list[count]] = value * xyz_working[index_list[count]]

        return_coordinates.append(xyz_working)
        xyz_working = xyz

    return return_coordinates


