"""
The purpose of this file is to evaluate the time taken to run the simulation. It is not intended to be run on it's own.

evaluate using python -m timeit timeSim.py
"""

from Simulation.simulation import run_simulation_default

def const_extension(alt,vel,acc,extension,seaTemp,seaPressure):
    return 0.5

run_simulation_default(
    seaTemp=300,
    seaPressure=100000,
    lapseRate=-0.005,
    initialVelocity=225,
    initialAltitude=1100,
    extension_function=const_extension
)