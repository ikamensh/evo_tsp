from Sasegasa import Sasegasa
from City import cities

if __name__ == '__main__':
    sgs = Sasegasa(cities, n_villages = 3, size_per_village=50, epochs_per_step=2)
    sgs.run()