from Sasegasa import Sasegasa
from City import City
from time import time

if __name__ == "__main__":

    cities = [City(ndim=2) for _ in range(60)]

    t = time()

    sgs = Sasegasa(cities, n_villages=5, size_per_village=50, epochs_per_step=20)
    sgs.run()

    print("It took that many seconds: ",time() - t)