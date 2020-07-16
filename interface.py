import numpy as np

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
    if a1 == a2 and c1 == c2:
        p = energy_output(function)
        e1, e2 = p(2 * c), p(-(2 * c))
        fort15array.append((coordinate, e1, e2))

    elif len(coordinate) == 4:
        p = energy_output(function)
        e1, e2, e3, e4 = p((2 * c)), p(c), p(-c), p(-(2 * c))
        fort15array.append((coordinate, e1, e2, e3, e4))

    else:
        raise Exception("Incorrect length for the second coordinates. Check the input.")


def third_matching(coordinate, function):
    coordinate = coordinate.tolist()
    if np.all([coordinate[0] == coordinate[1], coordinate[1] == coordinate[2]]):
        p = energy_output(function)
        e1, e2, e3, e4 = p(3 * c), p(c), p(-c), p(-(3 * c))
        fort30array.append((coordinate, [e1, e2, e3, e4]))

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
        fort30array.append((coordinate, [else_third]))

    else:
        raise Exception("Unable to iterate over all coordinates. Check the geometry.")


def third_doubles(coordinate, function):
    p = energy_output(function)
    e1, e2, e3, e4, e5, e6 = p(3 * c), p(c), p(-c), p(c), p(-c), p(-(3 * c))
    fort30array.append((coordinate, [e1, e2, e3, e4, e5, e6]))


def fourth_matching(coordinate, function):
    coordinate = coordinate.tolist()
    if np.all([coordinate[0] == coordinate[1], coordinate[1] == coordinate[2], coordinate[2] == coordinate[3]]):
        p = energy_output(function)
        e1, e2, e3, e4 = p(4 * c), p(2 * c), p(-(2 * c)), p(-(4 * c))
        fort40array.append((coordinate, [e1, e2, e3, e4]))

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
        fort40array.append((coordinate, [fourth_single]))


def fourth_doubles(coordinate, function):
    p = np.poly1d(function)
    fourth_double = [p(4 * c), p(2 * c), p(0), p(2 * c), p(0), p(-(2 * c)), p(2 * c), p(0), p(-(2 * c)), p(0),
                     p(-(2 * c)),
                     p(-(4 * c))]
    fort40array.append((coordinate, [fourth_double]))


def fourth_triples(coordinate, function):
    p = np.poly1d(function)
    fourth_triple = [p(4 * c), p(2 * c), p(0), p(-(2 * c)), p(2 * c), p(0), p(-(2 * c)), p(-(4 * c))]
    fort40array.append((coordinate, [fourth_triple]))


def fourth_pair(coordinate, function):
    p = np.poly1d(function)
    fourth_pairs = [p(4 * c), p(-(4 * c)), p(0), p(0), p(2 * c), p(2 * c), p(-(2 * c)), p(-(2 * c)), p(0)]
    fort40array.append((coordinate, [fourth_pairs]))
