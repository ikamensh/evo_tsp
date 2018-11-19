from Sasegasa import Sasegasa
from City import cities

sgs = Sasegasa(cities, size_per_village=50, epochs_per_step=2)
sgs.run()