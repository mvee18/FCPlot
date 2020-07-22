import numpy as np
from coordinate_parsing import parse_coordinates
from generatecoordinates import read_first_line

# DONE! Create a function that iterates over the dimensions of the coordinate array.
# At each call to create a function, the current coordinates of each coordinate array should be submitted.
# Then, one large table can be created. I.E.:
# [[(0, 0), (0, 0), (0, 0)], [function coeffs]]
# ... and so on.

"""
Now we have all possible combinations of the force constants. We need to parse the function array to determine 
which ones we need...
"""

# Here is a function that can take all the values of a certain derivative and then give it's absolute errors
# in descending order.

# I can probably find a way to easily interface this with the massive point array that is still in memory...

"""
import numpy as np

c = 0.00944863
test_list = []

for value in function_list:
    if np.all([value[0]==[0,1,0,1]]):
        p = np.poly1d(value[3])
        e1 = p(2*c) - exact1
        e2 = p(-(2*c)) - exact2
        test_list.append((e1, e2))
print(sorted(test_list))
"""

num_atoms = int(read_first_line("fort_files/fort.15")[0])

# We also need to apply the scanning implemented in the original method to determine which displacements we need.
fort15array = []
fort30array = []
fort40array = []

c = 0.00944863


def function_list_iteration(array):
    global fort15array, fort30array, fort40array
    for entry in range(array.shape[0]):
        for coordinates in range(array.shape[1]):
            function = array[entry][3]

            if coordinates == 0:
                second_matching(array[entry][0], function)

            elif coordinates == 1:
                third_matching(array[entry][1], function)

            elif coordinates == 2:
                fourth_matching(array[entry][2], function)

    return np.asarray(fort15array), np.asarray(fort30array), np.asarray(fort40array)


def energy_output(function):
    return np.poly1d(function)


def second_matching(coordinate, function):
    a1 = coordinate[0]
    c1 = coordinate[1]
    a2 = coordinate[2]
    c2 = coordinate[3]

    # This will convert the coordinate from [0,0,0,0] --> [1, 0, 0, 0, 0, 0, 0, 0, 0]

    if a1 == a2 and c1 == c2:
        p = energy_output(function)
        e1, e2 = p(2 * c), p(-(2 * c))
        fort15array.append((parse_coordinates(coordinate, [(1,)]), e1))
        fort15array.append((parse_coordinates(coordinate, [(-1,)]), e2))

    elif len(coordinate) == 4:
        p = energy_output(function)
        second_list = [(p(2 * c)), p(c), p(-c), p(-(2 * c))]
        # The below input represents (+x,+y),(+x,-y),(-x,+y),(-x,-y) displacements.
        coordinate_list = parse_coordinates(coordinate, [(1, 1), (1, -1), (-1, 1), (-1, -1)])
        [fort15array.append((x, second_list[count])) for count, x in enumerate(coordinate_list)]

    else:
        raise Exception("Incorrect length for the second coordinates. Check the input.")


def third_matching(coordinate, function):
    coordinate = coordinate.tolist()
    if np.all([coordinate[0] == coordinate[1], coordinate[1] == coordinate[2]]):
        p = energy_output(function)
        third_list = [p(3 * c), p(c), p(-c), p(-(3 * c))]
        coordinate_list = parse_coordinates(coordinate, [(+1,), (+1/3,), (-1/3,), (-1,)])
        [fort30array.append((x, third_list[count])) for count, x in enumerate(coordinate_list)]

    elif np.all([coordinate[0] == coordinate[1]]):
        third_doubles(coordinate, function)

    elif np.all([coordinate[1] == coordinate[2]]):
        third_doubles(coordinate, function)

    elif np.all([coordinate[0] == coordinate[2]]):
        third_doubles(coordinate, function)

    elif np.all([coordinate[0] is not coordinate[1], coordinate[1] is not coordinate[2]]):
        p = energy_output(function)

        else_third = [p(3 * c), p(2 * c), p(2 * c), p(-(2 * c)), p(2 * c), p(-(2 * c)), p(-(2 * c)), p(-(2 * c)),
                      p(-(3 * c))]

        do_parsing_and_append(coordinate, else_third, 3,
                              [(1, 1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1), (1, 1, -1), (1, -1, -1), (-1, 1, -1),
                               (-1, -1, -1)])

    else:
        raise Exception("Unable to iterate over all coordinates. Check the geometry.")


def third_doubles(coordinate, function):
    p = energy_output(function)
    third_list = [p(3 * c), p(c), p(-c), p(c), p(-c), p(-(3 * c))]
    coordinate_list = parse_coordinates(coordinate, [(1, 1), (0, 1), (-1, 1), (1, -1), (0, -1), (-1, -1)])
    [fort30array.append((x, third_list[count])) for count, x in enumerate(coordinate_list)]


def fourth_matching(coordinate, function):
    coordinate = coordinate.tolist()
    if np.all([coordinate[0] == coordinate[1], coordinate[1] == coordinate[2], coordinate[2] == coordinate[3]]):
        p = np.poly1d(function)
        fourth_list = [p(4 * c), p(2 * c), p(0), p(-(2 * c)), p(-(4 * c))]
        do_parsing_and_append(coordinate, fourth_list, 4, [(1,), (1/2,), (0,), (-1/2,), (-1,)])

    elif np.all([coordinate[0] == coordinate[1], coordinate[0] == coordinate[2]]):
        fourth_triples(coordinate, function)

    elif np.all([coordinate[0] == coordinate[1], coordinate[0] == coordinate[3]]):
        fourth_triples(coordinate, function)

    elif np.all([coordinate[0] == coordinate[2], coordinate[0] == coordinate[3]]):
        fourth_triples(coordinate, function)

    elif np.all([coordinate[1] == coordinate[2], coordinate[1] == coordinate[3]]):
        fourth_triples(coordinate, function)

    elif np.all([coordinate[0] == coordinate[1], coordinate[2] == coordinate[3]]):
        fourth_pair(coordinate, function)

    elif np.all([coordinate[0] == coordinate[3], coordinate[1] == coordinate[2]]):
        fourth_pair(coordinate, function)

    elif np.all([coordinate[0] == coordinate[1]]):
        fourth_doubles(coordinate, function)

    elif np.all([coordinate[0] == coordinate[2]]):
        fourth_doubles(coordinate, function)

    elif np.all([coordinate[0] == coordinate[3]]):
        fourth_doubles(coordinate, function)

    elif np.all([coordinate[1] == coordinate[2]]):
        fourth_doubles(coordinate, function)

    elif np.all([coordinate[1] == coordinate[3]]):
        fourth_doubles(coordinate, function)

    elif np.all([coordinate[2] == coordinate[3]]):
        fourth_doubles(coordinate, function)

    else:
        p = np.poly1d(function)
        fourth_single = [p(4 * c), p(2 * c), p(2 * c), p(0), p(2 * c), p(0), p(0), p(-(2 * c)), p(2 * c), p(0), p(0),
                         p(-2), p(0), p(-2), p(-2), p(-4)]
        do_parsing_and_append(coordinate, fourth_single, 4,
                              [(1, 1, 1, 1), (-1, 1, 1, 1), (1, -1, 1, 1), (-1, -1, 1, 1), (1, 1, -1, 1),
                               (-1, 1, -1, 1), (1, -1, -1, 1), (-1, -1, -1, 1), (1, 1, 1, -1), (-1, 1, 1, -1),
                               (1, -1, 1, -1), (-1, -1, 1, -1), (1, 1, -1, -1), (-1, 1, -1, -1), (1, -1, -1, -1),
                               (-1, -1, -1, -1)])


def fourth_doubles(coordinate, function):
    p = np.poly1d(function)
    fourth_double = [p(4 * c), p(2 * c), p(0), p(2 * c), p(0), p(-(2 * c)), p(2 * c), p(0), p(-(2 * c)), p(0),
                     p(-(2 * c)), p(-(4 * c))]

    do_parsing_and_append(coordinate, fourth_double, 4,
                          [(1, 1, 1), (0, 1, 1), (-1, 1, 1), (1, -1, 1), (0, -1, 1), (-1, -1, 1), (1, 1, -1),
                           (0, 1, -1), (-1, 1, -1), (1, -1, -1), (0, -1, -1), (-1, -1, -1)])

# TODO: Make the multiplication map to the larger value.
def fourth_triples(coordinate, function):
    p = np.poly1d(function)
    fourth_triple = [p(4 * c), p(2 * c), p(0), p(-(2 * c)), p(2 * c), p(0), p(-(2 * c)), p(-(4 * c))]
    do_parsing_and_append(coordinate, fourth_triple, 4,
                          [(1, 1), (1/3, 1), (-1/3, 1), (-1, 1), (1, -1), (1/3, -1), (-1/3, -1), (-1, -1)])


def fourth_pair(coordinate, function):
    p = np.poly1d(function)
    fourth_pairs = [p(4 * c), p(-(4 * c)), p(0), p(0), p(2 * c), p(2 * c), p(-(2 * c)), p(-(2 * c)), p(0)]
    do_parsing_and_append(coordinate, fourth_pairs, 4,
                          [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)])


def do_parsing_and_append(coordinate, energies, derivative, signs):
    coordinate_list = parse_coordinates(coordinate, signs)

    if derivative == 2:
        [fort15array.append((x, energies[count])) for count, x in enumerate(coordinate_list)]

    elif derivative == 3:
        [fort30array.append((x, energies[count])) for count, x in enumerate(coordinate_list)]

    elif derivative == 4:
        [fort40array.append((x, energies[count])) for count, x in enumerate(coordinate_list)]
