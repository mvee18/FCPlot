import numpy as np
import os
from generatecoordinates import second_coordinates, third_geometry, fourth_geometry


np.set_printoptions(precision=10, floatmode="fixed", suppress=True)


def generate_array(file):
    path = os.path.join(file)
    return np.asarray(np.genfromtxt(path, skip_header=1))

"""
def flatten_array(array):
    array = array.flatten()
    return array


# Okay, this seems to work well. Let's try the other arrays and then put it all together.
def second_array_matching():
    fort15 = generate_array("fort_files/fort.15")
    fort15shape = fort15.shape

    second_coords = second_coordinates("fort_files/fort.15")
    stacked = np.reshape(second_coords, (fort15shape[0], fort15shape[1], 4))

#   for rows in range(fort15shape[0]):
#       for cols in range(fort15shape[1]):
#           print(fort15[rows][cols], stacked[rows][cols])


def third_array_matching():
    fort30 = generate_array("fort_files/fort.30")
    fort30shape = fort30.shape

    third_coords = third_geometry()
    reshape_third = np.reshape(third_coords, (fort30shape[0], fort30shape[1], 3, 2))
    reshape_third_shape = reshape_third.shape

#   for rows in range(reshape_third_shape[0]):
#       for cols in range(reshape_third_shape[1]):
#           print(reshape_third[rows][cols], fort30[rows][cols])


def fourth_array_matching():
    fort40 = generate_array("fort_files/fort.40")
    fort40shape = fort40.shape

    fourth_coords = fourth_geometry()
    reshape_fourth = np.reshape(fourth_coords, (165, 3, 4, 2))

#   for rows in range(fort40shape[0]):
#       for cols in range(fort40shape[1]):
#           print(reshape_fourth[rows][cols], fort40[rows][cols])
"""

# Put it all together in one beautiful function. DONE!
def array_matching(filename):
    fort_file = os.path.join("fort_files/" + filename)
    fort = generate_array(fort_file)
    fort_shape = fort.shape

    if filename == "fort.15":
        coords = second_coordinates(fort_file)
        reshaped_coords = np.reshape(coords, (fort_shape[0], fort_shape[1], 4))

    elif filename == "fort.30":
        coords = third_geometry()
        reshaped_coords = np.reshape(coords, (fort_shape[0], fort_shape[1], 3, 2))

    elif filename == "fort.40":
        coords = fourth_geometry()
        reshaped_coords = np.reshape(coords, (fort_shape[0], fort_shape[1], 4, 2))

    else:
        raise Exception("Could not match force constants with coordinates.")

    return fort, reshaped_coords, fort_shape


def iterate_arrays():
    second_array, second_coords, second_shape = array_matching("fort.15")
    third_array, third_coords, third_shape = array_matching("fort.30")
    fourth_array, fourth_coords, fourth_shape = array_matching("fort.40")

    for rows in range(second_shape[0]):
        for cols in range(second_shape[1]):
            for thr_rows in range(third_shape[0]):
                for thr_cols in range(third_shape[1]):
                    for for_rows in range(fourth_shape[0]):
                        for for_cols in range(fourth_shape[1]):
                            print(rows, cols, thr_rows, thr_cols, for_rows, for_cols)
                            f1, c2 = second_array[rows][cols], second_coords[rows][cols]
                            f2, c3 = third_array[thr_rows][thr_cols], third_coords[thr_rows][thr_cols]
                            f3, c4 = fourth_array[for_rows][for_cols], fourth_coords[for_rows][for_cols]
                            summation_of_terms(f1, f2, f3, c2, c3, c4)


def summation_of_terms(f1, f2, f3, c2, c3, c4):
    points = []
    c = 0.00944863
    referenceE = -76.369839621528
    for x in range(5):
        x = x * c
        y = (referenceE + 0 + (f1 / 2) * (x ** 2) + (f2 / 6) * (x ** 3) + (f3 / 24) * (x ** 4))
        # points.append((x, relative_energy(y)))
        #        print(x, y)
        points.append((x, y))
    #    print(points)
    #    plot_from_tuples(points)
    yield_coefficients(points, c2, c3, c4)


def yield_coefficients(data, c2, c3, c4):
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    x_new, y_new, coeffs = poly_fit(x_val, y_val)
    function_list.append((c2, c3, c4, coeffs))


def poly_fit(x, y):
    z = np.polyfit(x, y, 4)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    return x_new, y_new, z


function_list = []
iterate_arrays()

function_list = np.asarray(function_list)
print(function_list)

"""
This is why the arrays do not line up. The reciprocal points are used.
array[a1, c1, a2, c2] = energy
array[a2, c2, a1, c1] = energy

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
"""