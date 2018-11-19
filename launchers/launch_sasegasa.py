from Sasegasa import Sasegasa
from City import cities

sgs = Sasegasa(cities, size_per_village=500, epochs_per_step=70)
sgs.run()