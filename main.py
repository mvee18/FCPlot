import numpy as np
import os
import matplotlib.pyplot as plt
from generatecoordinates import second_coordinates

# This function will return a numpy array from the fort files.
def generate_array(file):
    path = os.path.join(file)
    return np.asarray(np.genfromtxt(path, skip_header=1))

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

def coordinate_array():
    second_coords = second_coordinates("fort.15")
    return second_coords

# Taylor Series Calculations. Find a way to find each point...?
def taylor_series(level):
    if level == 2:
        data = generate_data(2)
        print(data[0][16][2])
    elif level == 3:
        data = generate_data(3)
        print(data[0][16][2])
    elif level == 4:
        data = generate_data(3)
        print(data[0][16][2])
    else:
        raise Exception("Invalid Level. Must be 2,3,4.")


# These are the z2 displacements.
# f_constants = [0.45961573569854314, 0.40010514709525397, -1.839080919045915]


# These are the z3 displacements.
f_constants = [0.21817255812613368, -0.17041516191284814, -0.8302383821581545]

referenceE = -76.369839621528

f1 = abs(f_constants[0])
f2 = abs(f_constants[1])
f3 = abs(f_constants[2])

def plot_from_tuples(data):
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    plt.plot(x_val, y_val, color="k", marker="o")
#    plt.autoscale(enable=True, axis="y", tight=False)
#    plt.plot(x_val, y_val, 'or')

# It is interesting to note that if the below code is added, then the plot is a linear graph...
#    plt.xscale('log')
#    plt.yscale('log')

    plt.show()

# Check that the signs of the values are correct. I don't anticipate that the signs need to change.
# TODO: Implement a curve fitting method.
def summation_of_terms(z):
    points = []

    for x in range(z):
        y = (referenceE + (f1/2)*(x**2) + (f2/6)*(x**3) + (f3/24)*(x**4))
        print(y)
        points.append((x, relative_energy(y)))

    print(points)
    plot_from_tuples(points)

def relative_energy(energy):
    rel_energy = abs((energy - referenceE)) / abs(referenceE)
    return rel_energy


summation_of_terms(10)
# coordinate_array()
