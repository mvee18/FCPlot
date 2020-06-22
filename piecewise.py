import matplotlib.pyplot as plt
import numpy as np

referenceE = -76.369839621528

points = []
energy_list = []
c = 0.00944863

f1 = 0.21817255812613368
f2 = -0.17041516191284814
f3 = -0.8302383821581545

def relative_energy(energy):
    rel_energy = abs((energy - referenceE)) / abs(referenceE)
    return rel_energy


def poly_fit(x, y):
    z = np.polyfit(x, y, 4)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    return x_new, y_new, z


def summation_of_terms(f1, f2, f3):
    global c
    y0 = referenceE
    y1 = referenceE + 0
    y2 = referenceE + 0 + (f1/2)*(c**2)
    y3 = (referenceE + 0 + (f1/2)*(c**2) + (f2/6)*(c**3))
    y4 = (referenceE + (f1/2)*(c**2) + (f2/6)*(c**3) + (f3/24)*(c**4))
    energy_list.extend([y0, y1, y2, y3, y4])
    print(energy_list)
    plot_from_tuples(create_points(energy_list))


def create_points(e_list):
    global c
    [points.append(((count*c), x)) for count, x in enumerate(e_list)]
    print(points)
    return points


def plot_from_tuples(data):
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    x_new, y_new, coeffs = poly_fit(x_val, y_val)
    print(coeffs)

    plt.rcParams['axes.formatter.useoffset'] = False
    plt.plot(x_val, y_val, 'o', x_new, y_new)
    plt.xlim([x_new[0]-0.005, x_new[-1]+0.005])
    plt.grid(True)
    plt.show()


summation_of_terms(f1, f2, f3)
