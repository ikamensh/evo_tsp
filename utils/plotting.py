import matplotlib.pyplot as plt
import os

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