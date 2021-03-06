#!/usr/bin/env python3

import numpy as np
import os
from generatecoordinates import second_coordinates, third_geometry, fourth_geometry
import multiprocessing as mp
import time
from interface import function_list_iteration
import pandas as pd
import getopt, sys

start_time = time.time()
np.set_printoptions(precision=10, floatmode="fixed", suppress=True)

function_list = []


def generate_array(file):
    path = os.path.join(file)
    try:
        fort = np.asarray(np.genfromtxt(path, skip_header=1))
        return fort

    except ValueError:
        with open(path, 'r') as fhand:
            file_lines = [line[:-1] for line in fhand if line.strip() != '']

        file_lines.pop(0)
        mat_raw = [[float(term) for term in line.split()] for line in file_lines]
        length = max(map(len, mat_raw))
        y = np.array([xi + [None] * (length-len(xi)) for xi in mat_raw])
        return y


# Put it all together in one beautiful function. DONE!
def array_matching(filename):
    fort_file = os.path.join("fort_files/" + filename)
    fort = generate_array(fort_file)    # This returns the padded out FC array if not an equal columns length.
    fort_shape = fort.shape
    print(fort_shape)

    if filename == "fort.15":
        coords = second_coordinates(fort_file)
        print(coords)
        reshaped_coords = np.reshape(coords, (fort_shape[0], fort_shape[1], 4))

    elif filename == "fort.30":
        coords = third_geometry()
        print(coords)
        try:
            reshaped_coords = np.reshape(coords, (fort_shape[0], fort_shape[1], 3, 2))

        except ValueError:
            coords = unequal_cols_coords(fort, coords)
            reshaped_coords = np.reshape(coords, (fort_shape[0], fort_shape[1], 3, 2))
            breakpoint()

    elif filename == "fort.40":
        coords = fourth_geometry()
        print(coords)
        breakpoint()
        reshaped_coords = np.reshape(coords, (fort_shape[0], fort_shape[1], 4, 2))

    else:
        raise Exception("Could not match force constants with coordinates.")

    return fort, reshaped_coords, fort_shape


def iterate_arrays():
    second_array, second_coords, second_shape = array_matching("fort.15")
    third_array, third_coords, third_shape = array_matching("fort.30")
    fourth_array, fourth_coords, fourth_shape = array_matching("fort.40")

    array = []
    num_of_points = (second_array.size * third_array.size * fourth_array.size)
    print("Currently generating data for {} points...".format(num_of_points))

    for rows in range(second_shape[0]):
        for cols in range(second_shape[1]):
            for thr_rows in range(third_shape[0]):
                for thr_cols in range(third_shape[1]):
                    for for_rows in range(fourth_shape[0]):
                        for for_cols in range(fourth_shape[1]):
                            if third_array[thr_rows][thr_cols] is not None:
                                f1, c2 = second_array[rows][cols], second_coords[rows][cols]
                                f2, c3 = third_array[thr_rows][thr_cols], third_coords[thr_rows][thr_cols]
                                f3, c4 = fourth_array[for_rows][for_cols], fourth_coords[for_rows][for_cols]
                                array.append([f1, f2, f3, c2, c3, c4])
                            else:
                                continue

    print("{} points generated. Proceeding to function creation.".format(len(array)))
    return np.asarray(array)


#                               coeffs = pool.map(summation_of_terms, [(f1, f2, f3)])
#                               function_list.append((c2, c3, c4, coeffs))


def summation_of_terms(f_constants):
    f1, f2, f3 = f_constants[0], f_constants[1], f_constants[2]
    c2, c3, c4 = f_constants[3], f_constants[4], f_constants[5]
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
    coeffs = yield_coefficients(points)
    return [c2, c3, c4, coeffs]


def yield_coefficients(data):
    x_val = [val[0] for val in data]
    y_val = [val[1] for val in data]

    x_new, y_new, coeffs = poly_fit(x_val, y_val)
    return coeffs


def poly_fit(x, y):
    z = np.polyfit(x, y, 4)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    return x_new, y_new, z


def command_line(argv):
    try:
        opts, args = getopt.getopt(argv, "t:", ["type="])
    except getopt.GetoptError:
        print('fcplot.py -t local')
        sys.exit(2)

    for opt, arg in opts:
        if opt in "-t":
            if arg == "local":
                return True

            else:
                return False

def unequal_cols_coords(forces, coordinates):
    force_shape = forces.shape
    needed_num_of_coords = force_shape[0] * force_shape[1]
    times_to_append = needed_num_of_coords - coordinates.shape[0]

    for i in range(times_to_append):
        coordinates = np.append(coordinates, [[[None, None], [None, None], [None, None]]])

    return coordinates


if __name__ == "__main__":
    # -t local or supercomputer by default
    local_bool = command_line(sys.argv[1:])

    mp_array = iterate_arrays()
    print("The array occupies %d bytes\n" % mp_array.nbytes)
    breakpoint()

    if local_bool:  # if True from command_line().
        with mp.Pool() as pool:
            for x in pool.imap(summation_of_terms, mp_array, 1000):
                function_list.append(x)

        del mp_array
        del pool, x

    else:
        for row in mp_array:
            x = summation_of_terms(row)
            function_list.append(x)

        del mp_array

    # Manual memory freeing; these no longer need to be in memory.

    function_list = np.asarray(function_list)
    print(function_list)
    print("The function_list occupies %d bytes\n" % function_list.nbytes)
    print("---- %s seconds ----" % (time.time() - start_time))
    #   breakpoint()

    sec, thr, fourth = function_list_iteration(function_list)

    del function_list

    print(sec)
    print("\n")
    print(thr)
    print("\n")
    print(fourth)

    secondDF = pd.DataFrame(data=sec)
    thirdDF = pd.DataFrame(data=thr)
    fourthDF = pd.DataFrame(data=fourth)

    secondDF.to_csv('second.out')
    thirdDF.to_csv('third.out')
    fourthDF.to_csv('fourth.out')

    #   breakpoint()
    print("---- %s seconds ----" % (time.time() - start_time))
