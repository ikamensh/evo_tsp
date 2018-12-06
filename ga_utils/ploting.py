import matplotlib.pyplot as plt
import os

problem_tag = lambda cities: f"cities_{len(cities)}_dim{len(cities[0].coordinates)}"

def maybe_make_dir(folder):
    try:
        os.makedirs(folder)
    except:
        pass

def my_plot(array, name, folder):
    maybe_make_dir(folder)
    plt.clf()
    plt.plot(array)
    plt.ylabel(name)
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, name+".png"))

def plot_many(name, folder, *args):
    maybe_make_dir(folder)
    plt.clf()
    for array in args:
        plt.plot(array)
    plt.ylabel(name)
    plt.xlabel('Generation')
    plt.grid()
    plt.savefig(os.path.join(folder, name + ".png"))


def plot_histogram(array, name, folder):
    maybe_make_dir(folder)
    plt.clf()
    plt.hist(array)
    plt.savefig(os.path.join(folder, name+".png"))
