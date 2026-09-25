from Simulation.simulation import run_simulation_default
import timeit

def const_extension(alt,vel,acc,extension,seaTemp,seaPressure):
    return 0.5

def timedFunc():
    run_simulation_default(    seaTemp=300,    seaPressure=100000,    lapseRate=-0.005,    initialVelocity=225,    initialAltitude=1100,    extension_function=const_extension)

n = 100
executionTime = timeit.timeit(timedFunc,number=n)
print(f"Average execution time: {executionTime/n}")