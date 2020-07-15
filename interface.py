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

def function_list_iteration(array):
    for entry in range(array.shape[0]):
        for coordinates in range(array.shape[1]):
            if coordinates == 0:
                print(array[entry][0])
                print(second_matching(array[entry][0]))

            elif coordinates == 1:
                print(array[entry][1])
                print(third_matching(array[entry][1]))

            elif coordinates == 2:
                print(array[entry][2])
                print(fourth_matching(array[entry][2]))


def second_matching(coordinate):
    a1 = coordinate[0]
    c1 = coordinate[1]
    a2 = coordinate[2]
    c2 = coordinate[3]
    if a1 == a2 and c1 == c2:
        return 1

    elif len(coordinate) == 4:
        return 0

    else:
        raise Exception("Incorrect length for the second coordinates. Check the input.")

def third_matching(coordinate):
    if np.all([coordinate[0] == coordinate[1], coordinate[1] == coordinate[2]]):
        return 3

    elif np.all([coordinate[0] == coordinate[1]]):
        return 0, 1

    elif np.all([coordinate[1] == coordinate[2]]):
        return 1, 2

    elif np.all([coordinate[0] == coordinate[2]]):
        return 0, 2

    elif np.all([coordinate[0] is not coordinate[1], coordinate[1] is not coordinate[2]]):
        return 0

    else:
        raise Exception("Unable to iterate over all coordinates. Check the geometry.")

def fourth_matching(coordinate):
    if np.all([coordinate[0] == coordinate[1], coordinate[1] == coordinate[2], coordinate[2] == coordinate[3]]):
        return 4

    elif np.all([coordinate[0] == coordinate[1], coordinate[0] == coordinate[2]]):
        return 0, 1, 2

    elif np.all([coordinate[0] == coordinate[1], coordinate[0] == coordinate[3]]):
        return 0, 1, 3

    elif np.all([coordinate[0] == coordinate[2], coordinate[0] == coordinate[3]]):
        return 0, 2, 3

    elif np.all([coordinate[1] == coordinate[2], coordinate[1] == coordinate[3]]):
        return 1, 2, 3

    elif np.all([coordinate[0] == coordinate[1], coordinate[2] == coordinate[3]]):
        return 0, 1, 2, 3

    elif np.all([coordinate[0] == coordinate[3], coordinate[1] == coordinate[2]]):
        return 0, 3, 1, 2

    elif np.all([coordinate[0] == coordinate[1]]):
        return 0, 1

    elif np.all([coordinate[0] == coordinate[2]]):
        return 0, 2

    elif np.all([coordinate[0] == coordinate[3]]):
        return 0, 3

    elif np.all([coordinate[1] == coordinate[2]]):
        return 1, 2

    elif np.all([coordinate[1] == coordinate[3]]):
        return 1, 3

    elif np.all([coordinate[2] == coordinate[3]]):
        return 1, 3

    else:
        return 0
