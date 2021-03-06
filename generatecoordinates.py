import numpy as np
import os

# This works. Or we could just use the array.size from the main file.
def read_first_line(fort_file):
    file = os.path.join(fort_file)
    f = open(file, "r")
    lines = f.readlines()
    first_line = lines[0].split()
    size_of_line = (int(first_line[0]), int(first_line[1]))
    return size_of_line


def generate_second_coordinates(size):
    array = []
    for atom1 in range(size[0]):
        coordinate_list1 = []
        for coordinate1 in range(3):
            atom_list1 = []
            for atom2 in range(size[0]):
                coordinate_list2 = []
                for coordinate2 in range(3):
                    coordinate_list2.append(coordinate2)
                atom_list1.append(coordinate_list2)
            coordinate_list1.append(atom_list1)
        array.append(coordinate_list1)

    array = np.asarray(array)
    array = array.astype(float)
    shape_four = array.shape

    return shape_four


def convert(coordinates):
    s = [str(i) for i in coordinates]
    res = int("".join(s))
    return res


def yield_coordinates(shape_four):
    for i in range(shape_four[0]):
        for j in range(shape_four[1]):
            found = False
            for k in range(shape_four[2]):
                for L in range(shape_four[3]):
                    yield i, j, k, L
                    """
                    if i == k and j == L:
                        value = (i, j, k, L)
                        res = convert(value)
                        found = True
                        yield i, j, k, L
                    # manipulate_geometry_second(i, j, k, l)
                    elif found:
                        comparison_list = (i, j, k, L)
                        compare_value = convert(comparison_list)
                        yield i, j, k, L
                        if compare_value > res:
                            # print(compare_value, res)
                            yield i, j, k, L
                            # manipulate_geometry_second(i, j, k, l)
                    """
# This function generates the array with all of the coordinates for the second derivatives using a generator expression.
def second_coordinates(fort_file):
    second_coords = []
    for value in yield_coordinates(generate_second_coordinates(read_first_line(fort_file))):
        second_coords.append(value)

    second_coords = np.asarray(second_coords)
    return second_coords


generate_second_coordinates((3, 0))

second_coordinates("fort_files/fort.15")

third_list = []

def determine_atom(row, atom_number, item, array):
    array[row, atom_number, item] = int(array[row, atom_number, item]) // 3

def determine_coordinate(row, coordinate_number, item, array):
    array[row, coordinate_number, item] = int(array[row, coordinate_number, item]) % 3

def third_geometry():
    third_size = read_first_line("fort_files/fort.30")
    num_of_jobs = third_size[0] * 3
    for i in range(num_of_jobs):
        for j in range(num_of_jobs):
            for k in range(num_of_jobs):
                if j <= i and k <= j:
                    third_list.append(((i, i), (j, j), (k, k)))

    third_array = np.asarray(third_list)

    third_array_shape = third_array.shape

    for row in range(third_array_shape[0]):
        for col in range(third_array_shape[1]):
            pair = 0
            if pair == 0:
                determine_atom(row, col, pair, third_array)
        for col in range(third_array_shape[1]):
            pair = 1
            if pair == 1:
                third_array[row, col, 1] = int(third_array[row, col, 1])
                determine_coordinate(row, col, 1, third_array)
    #    print(third_array.shape)
    return third_array


"""
    zipped_array = []
    for i in range(third_array_shape[0]):
        for j in range(third_array_shape[1]):
            row_list.append(third_array[i, j, 0])
            col_list.append(third_array[i, j, 1])
        zipped = zip(row_list, col_list)
        zipped = list(zipped)
        zipped_array.append(zipped)
        row_list.clear()
        col_list.clear()

    print(zipped_array)
    zipped_array = np.asarray(zipped_array)
    print(zipped_array)
#    print(third_array.shape)
"""

row_list = []
col_list = []

third_energy_array = []

def determine_fourth_atom(row, atom_number, item, fourth_array):
    fourth_array[row, atom_number, item] = int(fourth_array[row, atom_number, item]) // 3


def determine_fourth_coordinate(row, coordinate_number, item, fourth_array):
    fourth_array[row, coordinate_number, item] = int(fourth_array[row, coordinate_number, item]) % 3


fourth_list = []

# DONE: Fix generation of fourth points. It seems to create two arrays together...
# FIXED: Second col loop was not correctly indented.
def fourth_geometry():
    fourth_size = read_first_line("fort_files/fort.40")
    num_of_jobs = fourth_size[0] * 3
    for w in range(num_of_jobs):
        for x in range(num_of_jobs):
            for y in range(num_of_jobs):
                for z in range(num_of_jobs):
                    if x <= w and y <= x and z <= y:
                        fourth_list.append(((w, w), (x, x), (y, y), (z, z)))

    fourth_array = np.asarray(fourth_list)

    fourth_array_shape = fourth_array.shape

    for row in range(fourth_array_shape[0]):
        for col in range(fourth_array_shape[1]):
            pair = 0
            if pair == 0:
                determine_fourth_atom(row, col, 0, fourth_array)

        for col in range(fourth_array_shape[1]):
            pair = 1
            if pair == 1:
                fourth_array[row, col, 1] = int(fourth_array[row, col, 1])
                determine_fourth_coordinate(row, col, 1, fourth_array)

    new_fourth = []
    for value in fourth_array:
        new_fourth.append(value)

    return np.asarray(new_fourth)
