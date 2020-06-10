import numpy as np

# This works. Or we could just use the array.size from the main file.
def read_first_line(fort_file):
    f = open(fort_file, "r")
    lines = f.readlines()
    first_line = lines[0].split()
    size_of_line = (int(first_line[0]), int(first_line[1]))
    return size_of_line


def generate_second_coordinates(size):
    array = []
    for atom1 in range(size[0]):
        coordinate_list1 = []
        for coordinate1 in range(size[0]):
            atom_list1 = []
            for atom2 in range(size[0]):
                coordinate_list2 = []
                for coordinate2 in range(size[0]):
                    coordinate_list2.append(coordinate2)
                atom_list1.append(coordinate_list2)
            coordinate_list1.append(atom_list1)
        array.append(coordinate_list1)

    array = np.asarray(array)
    array = array.astype(float)
    shape_four = array.shape
    compare_coordinates(shape_four)


def convert(coordinates):
    s = [str(i) for i in coordinates]
    res = int("".join(s))
    return res


def compare_coordinates(shape_array):
    for i in range(shape_array[0]):
        for j in range(shape_array[1]):
            found = False
            for k in range(shape_array[2]):
                for L in range(shape_array[3]):
                    if i == k and j == L:
                        value = (i, j, k, L)
                        res = convert(value)
                        found = True
                        print(i, j, k, L)
                    # manipulate_geometry_second(i, j, k, l)
                    elif found:
                        comparison_list = (i, j, k, L)
                        compare_value = convert(comparison_list)
                        if compare_value > res:
                            # print(compare_value, res)
                            print(i, j, k, L)
                            # manipulate_geometry_second(i, j, k, l)


def second_coordinates(fort_file):
    generate_second_coordinates(read_first_line(fort_file))
