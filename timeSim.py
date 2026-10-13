from Simulation.simulation import run_simulation_default
import timeit
import cProfile

from controllers import constant_extension, set_constant_extension

def timedFunc():
    run_simulation_default(    seaTemp=300,    seaPressure=100000,    lapseRate=-0.005,    initialVelocity=225,    initialAltitude=1100,    extension_function=constant_extension)

n = 100
set_constant_extension(0.5)
executionTime = timeit.timeit(timedFunc,number=n)
print(f"Average execution time: {executionTime/n}")

cProfile.run('timedFunc()')