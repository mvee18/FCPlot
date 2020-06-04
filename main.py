import numpy as np
import os

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


# Taylor Series Calculations.
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

