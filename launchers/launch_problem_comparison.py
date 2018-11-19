from City import City

from launchers.launch_classical import run_all
from Sasegasa import Sasegasa

if __name__ == "__main__":
    amounts = [60, 100, 300, 1000]
    n_dims = [2, 3, 5, 90]

    for amt in amounts:
        for d in n_dims:
            cities = [City(ndim=d) for _ in range(amt)]
            run_all(cities, 1)

            sgs = Sasegasa(cities, n_villages=2, size_per_village=10, epochs_per_step=2)
            sgs.run()
