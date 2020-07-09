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
    fort15data = generate_array("fort_files/fort.15")
    fort30data = generate_array("fort_files/fort.30")
    fort40data = generate_array("fort_files/fort.40")

    if level == 2:
        return fort15data
    elif level == 3:
        return fort15data, fort30data
    elif level == 4:
        return fort15data, fort30data, fort40data

# This function calls from generatecoordinates.py to generate the list of coordinates in base 3 (0 0 0 0) ...
def coordinate_array():
    second_coords = second_coordinates("fort_files/fort.15")
    return second_coords

# Taylor Series Calculations. Find a way to find each point...?
# TODO: Integrate this into the plotting functions.
def taylor_series(level):
    if level == 2:
        data = generate_data(2)
        print(data[0][16][2])
    elif level == 3:
        data = generate_data(3)
        print(data[0][16][2])
    elif level == 4:
        data = generate_data(4)
        print(data[0][16][2])
    else:
        raise Exception("Invalid Level. Must be 2,3,4.")


# These are the z2 displacements.
# f_constants = [0.45961573569854314, 0.40010514709525397, -1.839080919045915]

# These are the z3 displacements.
f_constants = [0.21817255812613368, -0.17041516191284814, -0.8302383821581545]

referenceE = -76.369839621528

# This list comprehension converts the f_constants given to their absolute values.
# TODO: Decide whether or not this is beneficial / harmful. Seems to make little difference for the z3 displacements.
# f_constants = [abs(x) for x in f_constants]

f1 = f_constants[0]
f2 = f_constants[1]
f3 = f_constants[2]

c = 0.00944863

# Check that the signs of the values are correct. I don't anticipate that the signs need to change.
# TODO: Implement a curve fitting method. DONE!
def summation_of_terms(z):
    points = []

    for x in range(z):
        x = x * c
        y = (referenceE + 0 + (f1/2)*(x**2) + (f2/6)*(x**3) + (f3/24)*(x**4))
        # print(y)
#        points.append((x, relative_energy(y)))
        print(x, y)
        points.append((x, y))
#    print(points)
    plot_from_tuples(points)


def relative_energy(energy):
    rel_energy = abs((energy - referenceE)) / abs(referenceE)
    return rel_energy


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


summation_of_terms(5)
# coordinate_array()
