from Simulation.simulation import run_simulation
import pandas as pd

# values obtained manually from saturn frame 0
seaLevelTemp = 280.8126697952598 # kelvin
seaLevelPressure = 98851.6944512164 # pascal
lapseRate = 0.00118 # kelvin per meter
initialVelocity = 239.15 # m/s
initialAltitude = 1137.745636727661 # meters
coefficientOfDrag = 0.39146244 # taken from meridian_final.csv under mach 0.6, no pitch, no roll, no extension
crossectionalArea = 0.0754767635 # m^2

apogee = run_simulation(1,seaLevelTemp,seaLevelPressure,lapseRate,initialVelocity,initialAltitude,coefficientOfDrag,crossectionalArea)