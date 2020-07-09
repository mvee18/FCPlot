import numpy as np
import os
from generatecoordinates import second_coordinates
from generatecoordinates import third_geometry

np.set_printoptions(precision=10, floatmode="fixed", suppress=True)


def generate_array(file):
    path = os.path.join(file)
    return np.asarray(np.genfromtxt(path, skip_header=1))


def flatten_array(array):
    array = array.flatten()
    return array


# Okay, this seems to work well. Let's try the other arrays and then put it all together.
def second_array_matching():
    fort15 = generate_array("fort_files/fort.15")
    fort15shape = fort15.shape

    second_coords = second_coordinates("fort_files/fort.15")
    stacked = np.reshape(second_coords, (27, 3, 4))

    for rows in range(fort15shape[0]):
        for cols in range(fort15shape[1]):
            print(fort15[rows][cols], stacked[rows][cols])


def third_array_matching():
    fort30 = generate_array("fort_files/fort.30")
    fort30shape = fort30.shape

    third_coords = third_geometry()
    reshape_third = np.reshape(third_coords, (55, 3, 3, 2))
    reshape_third_shape = reshape_third.shape

    for rows in range(reshape_third_shape[0]):
        for cols in range(reshape_third_shape[1]):
            print(reshape_third[rows][cols], fort30[rows][cols])


#   print(fort30)
#   print(third_coords)
#   print(third_coords.shape)
#   print(fort30shape)


third_array_matching()

breakpoint()

"""
This is why the arrays do not line up. The reciprocal points are used.
array[a1, c1, a2, c2] = energy
array[a2, c2, a1, c1] = energy
"""

Reset_List = []
def iterate_array(array1):
    array1 = flatten_array(array1)
    size1 = array1.shape  # (3, 27)
    print(size1)

    global second_iter, Reset_List

    for rows in range(size1[0]):
        try:
            f1 = (array1[rows])
            c2 = next(second_iter)
            Reset_List.append(list(c2))
            print(rows, f1, c2)
            break

        except StopIteration:
            Reset_List = np.asarray(Reset_List)
            # print(Reset_List)
            # print("You must construct additional pylons.")
            second_iter = iter(second_coords)
            f1 = (array1[rows])
            c2 = next(second_iter)
            print(f1, c2)

            Reset_List = []
            continue

iterate_array(fort15)
