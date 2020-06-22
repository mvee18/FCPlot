import numpy as np
import os
import matplotlib.pyplot as plt
from generatecoordinates import second_coordinates

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


# This function calls from generatecoordinates.py to generate the list of coordinates in base 3 (0 0 0 0) ...
def coordinate_array():
    second_coords = second_coordinates("fort.15")
    return second_coords


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


def iterate_array(array1, array2, array3):
    size1 = array1.shape
    size2 = array2.shape
    size3 = array3.shape

    for rows in range(size1[0]):
        for cols in range(size1[1]):
            f1 = (array1[rows][cols])
            break
        for rows2 in range(size2[0]):
            for cols in range(size2[1]):
                f2 = (array2[rows2][cols])
                break
            for rows3 in range(size3[0]):
                for cols in range(size3[1]):
                    f3 = (array3[rows3][cols])
                    summation_of_terms(f1, f2, f3)

    test_plot(points)

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
points = []

# I just don't know what I'm supposed to use for x. Because if I use the original method,
# there would be a ton of unrelated graphs.

def summation_of_terms(f1, f2, f3):
    global c
#    for x in range(10):
    y = (referenceE + (f1/2)*(c**2) + (f2/6)*(c**3) + (f3/24)*(c**4))
    # print(y)
    points.append((c, relative_energy(y)))
#   print(points)
#   plot_from_tuples(points)

def relative_energy(energy):
    rel_energy = abs((energy - referenceE)) / abs(referenceE)
    return rel_energy

# TODO: Figure out the correct order to plot the points ... maybe sort by energy?
def test_plot(data):
    print(data)
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    plt.scatter(x_val, y_val)
    plt.show()
# This function plots the data which is generate from the functions below.
def plot_from_tuples(data):
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    x_new, y_new, coeffs = poly_fit(x_val, y_val)
    print(coeffs)

    plt.plot(x_val, y_val, 'o', x_new, y_new)
    plt.xlim([x_val[0]-1, x_val[-1] + 1])
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
