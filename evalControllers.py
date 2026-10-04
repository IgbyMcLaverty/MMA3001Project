import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Simulation.simulation import run_simulation_default

from controllers import p_controller

def eval_controller(inputFileLoc,controller):
    """
    Uses a set of initial conditions and a provided controller and calculates evaluation criteria.
    Plots residuals for the controller against initial conditons.
    Plots histogram of achieved apogees.
    
    Args:
        inputFileLoc (string): The location of the initial condition data csv file. Include directory and .csv in string
        controller (function): A function which contains the control algorithm being evaluated
    
    Returns:
        None
    """

    initialConditions = pd.read_csv(inputFileLoc)

    numConditions = len(initialConditions)
    apogees = []

    for i in range(numConditions):
        seaLevelTemp = initialConditions["seaTemp"][i]
        seaLevelPressure = initialConditions["groundPressure"][i]
        lapseRate = initialConditions["lapserate"][i]
        initialVelocity = initialConditions["initialVelocity"][i]
        initialAltitude = initialConditions["initialAltitude"][i]

        simResults = run_simulation_default(
            seaTemp=seaLevelTemp,
            seaPressure=seaLevelPressure,
            lapseRate=lapseRate,
            initialAltitude=initialAltitude,
            initialVelocity=initialVelocity,
            extension_function=controller
        )

        apogees.append(simResults["apogee"])

    plt.hist(apogees)
    plt.show()

if __name__ == "__main__":
    eval_controller("data/validationData_initialConditions",p_controller)