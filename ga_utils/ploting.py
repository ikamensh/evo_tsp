import matplotlib.pyplot as plt
import os

problem_tag = lambda cities: f"cities_{len(cities)}_dim{len(cities[0].coordinates)}"

def my_plot(array, name, folder):
    plt.clf()
    plt.plot(array)
    plt.ylabel(name)
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, name+".png"))

def plot_many(name, folder, *args):
    plt.clf()
    for array in args:
        plt.plot(array)
    plt.ylabel(name)
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, name + ".png"))