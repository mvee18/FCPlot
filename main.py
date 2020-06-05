import numpy as np
import os
import matplotlib.pyplot as plt

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


f1 = 0.45961573569854314
f2 = 0.40010514709525397
f3 = -1.839080919045915

def plot_from_tuples(data):
    y_val = [x[0] for x in data]
    x_val = [x[1] for x in data]

    print(x_val)
    plt.plot(x_val, y_val)
    plt.plot(x_val, y_val, 'or')
    plt.show()

# F'(a)/1
def summation_of_terms(z):
    points = []

    for x in range(z):
        print(x)
        points.append((0 + (f1/1)*x + (f2/2)*(x**2) + (f3/6)*(x**3), x))

    plot_from_tuples(points)

summation_of_terms(8)

