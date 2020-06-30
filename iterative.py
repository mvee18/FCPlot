import numpy as np
import os
import matplotlib.pyplot as plt
from generatecoordinates import second_coordinates
from generatecoordinates import third_geometry
from generatecoordinates import fourth_geometry

# This function will return a numpy array from the fort files.
def generate_array(file):
    path = os.path.join(file)
    return np.asarray(np.genfromtxt(path, skip_header=1))

# This function will return the array specific to each given der. level, using the above function.
def generate_data(level):
    fort15data = generate_array("fort.15")
    fort30data = generate_array("fort.30")
    fort40data = generate_array("fort.40")

    if level == 2:
        return fort15data
    elif level == 3:
        return fort15data, fort30data
    elif level == 4:
        return fort15data, fort30data, fort40data


def reset_iter(iterator):
    global Reset_List
    while True:
        try:
            value = next(iterator)
            Reset_List.append(list(value))
            print(value)
        except StopIteration:
            Reset_List = np.asarray(Reset_List)
            print(Reset_List)
            print("You must construct additional pylons.")
            iterator = iter(Reset_List)
            Reset_List = []
            continue

# These functions yield the iterators necessary in the next step.
# TODO: Refactor this to use one function.
second_coords = second_coordinates("fort.15")
second_iter = iter(second_coords)

third_coords = third_geometry()
third_iter = iter(third_coords)

fourth_coords = fourth_geometry()
fourth_iter = iter(fourth_coords)

# Taylor Series Calculations. Find a way to find each point...?
# TODO: Integrate this into the plotting functions.
def taylor_series(level):
    if level == 2:
        data = generate_data(2)
        iterate_array(data, np.empty((0, 0)), np.empty((0, 0)))
    elif level == 3:
        data = generate_data(3)
        iterate_array(data[0], data[1], np.empty((0, 0)))
    elif level == 4:
        data = generate_data(4)
        iterate_array(data[0], data[1], data[2])

    else:
        raise Exception("Invalid Level. Must be 2,3,4.")


Reset_List = []
def iterate_array(array1, array2, array3):
    size1 = array1.shape
    size2 = array2.shape
    size3 = array3.shape
    global Reset_List, second_iter, third_iter, fourth_iter

    for rows in range(size1[0]):
        for cols in range(size1[1]):
            try:
                f1 = (array1[rows][cols])
                c2 = next(second_iter)
                Reset_List.append(list(c2))
                break

            except StopIteration:
                Reset_List = np.asarray(Reset_List)
                print(Reset_List)
                print("You must construct additional pylons.")
                second_iter = iter(Reset_List)
                Reset_List = []
                continue

        for rows2 in range(size2[0]):
            for cols in range(size2[1]):
                try:
                    f2 = (array2[rows2][cols])
                    c3 = next(third_iter)
                    Reset_List.append((list(c3)))
                    break

                except StopIteration:
                    Reset_List = np.asarray(Reset_List)
                    print(Reset_List)
                    print("You must construct additional pylons.")
                    third_iter = iter(Reset_List)
                    Reset_List = []
                    continue

            for rows3 in range(size3[0]):
                for cols in range(size3[1]):
                    try:
                        f3 = (array3[rows3][cols])
                        c4 = next(fourth_iter)
                        Reset_List.append((list(c4)))
                        summation_of_terms(f1, f2, f3, c2, c3, c4)
                        
                    except StopIteration:
                        Reset_List = np.asarray(Reset_List)
                        print(Reset_List)
                        print("You must construct additional pylons.")
                        fourth_iter = iter(Reset_List)
                        Reset_List = []
                        continue

#    test_plot(points)

# These are the z2 displacements.
# f_constants = [0.45961573569854314, 0.40010514709525397, -1.839080919045915]

# These are the z3 displacements.
# f_constants = [0.21817255812613368, -0.17041516191284814, -0.8302383821581545]


referenceE = -76.369839621528


# This list comprehension converts the f_constants given to their absolute values.
# TODO: Decide whether or not this is beneficial / harmful. Seems to make little difference for the z3 displacements.
"""
f_constants = [abs(x) for x in f_constants]

f1 = f_constants[0]
f2 = f_constants[1]
f3 = f_constants[2]
"""

# Check that the signs of the values are correct. I don't anticipate that the signs need to change.
# TODO: Implement a curve fitting method. DONE!
c = 0.00944863
energy_list = []
function_list = []

# I just don't know what I'm supposed to use for x. Because if I use the original method,
# there would be a ton of unrelated graphs.

def summation_of_terms(f1, f2, f3, c2, c3, c4):
    points = []
    for x in range(5):
        x = x * c
        y = (referenceE + 0 + (f1 / 2) * (x ** 2) + (f2 / 6) * (x ** 3) + (f3 / 24) * (x ** 4))
        # points.append((x, relative_energy(y)))
#        print(x, y)
        points.append((x, y))
    #    print(points)
#    plot_from_tuples(points)
    yield_coefficients(points, c2, c3, c4)


def relative_energy(energy):
    rel_energy = abs((energy - referenceE)) / abs(referenceE)
    return rel_energy


# TODO: Figure out the correct order to plot the points ... maybe sort by energy?
def test_plot(data):
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    plt.scatter(x_val, y_val)
    plt.show()


# This function is similar to plot_from_tuples, but instead appends the coordinates used and the function.
def yield_coefficients(data, c2, c3, c4):
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    x_new, y_new, coeffs = poly_fit(x_val, y_val)
    function_list.append((c2, c3, c4, coeffs))
    print(c2, c3, c4, coeffs)

# This function plots the data which is generate from the functions below.
def plot_from_tuples(data):
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    x_new, y_new, coeffs = poly_fit(x_val, y_val)
    print(coeffs)

    plt.rcParams['axes.formatter.useoffset'] = False
    plt.plot(x_val, y_val, 'o', x_new, y_new)
    plt.xlim([x_val[0]-0.005, x_val[-1] + 0.005])
    plt.grid(True)
    plt.show()


def poly_fit(x, y):
    z = np.polyfit(x, y, 4)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    return x_new, y_new, z


taylor_series(4)
# summation_of_terms(10)
# coordinate_array()

print(function_list)
