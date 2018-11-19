from Sasegasa import Sasegasa
from City import cities
from time import time

if __name__ == "__main__":
    t = time()

    sgs = Sasegasa(cities, n_villages=10, size_per_village=500, epochs_per_step=70)
    sgs.run()

    print("It took that many seconds: ",time() - t)