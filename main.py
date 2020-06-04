import numpy as np
import os

# This function will return a numpy array from the fort files.


def generatearray(file):
    path = os.path.join(file)
    return np.asarray(np.genfromtxt(path, skip_header=1))


fort15data = generatearray("fort.15")
fort30data = generatearray("fort.30")
fort40data = generatearray("fort.40")

print(fort15data[16][2])
