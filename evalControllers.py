import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Simulation.simulation import run_simulation_default

from controllers import p_controller
from controllers import linear_regression_controller
from controllers import TARGET_APOGEE

def eval_controller(inputFileLoc,controller,controllerName):
    """
    Uses a set of initial conditions and a provided controller and calculates evaluation criteria.
    Plots residuals for the controller against initial conditons.
    Plots histogram of achieved apogees.
    
    Args:
        inputFileLoc (string): The location of the initial condition data csv file. Include directory and .csv in string
        controller (function): A function which contains the control algorithm being evaluated
        controllerName (straing): The name of the controller which will be put in title of plots
    
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

    standardDeviation = np.std(apogees)
    mean = np.mean(apogees)
    print(f"Mean apogee of {controllerName} is {mean} meters, which is an error of {mean - TARGET_APOGEE}")
    print(f"Standard deviation of {controllerName} is {standardDeviation} meters")

    plt.hist(apogees,bins=np.arange(2000,4000,100))
    plt.title(f"{controllerName} apogee Histogram")
    plt.xlabel("Apogee")
    plt.ylabel("Occurances")
    plt.show()

if __name__ == "__main__":
    #eval_controller("data/validationData_initialConditions.csv",p_controller,"P controller")
    eval_controller("data/validationData_initialConditions.csv",linear_regression_controller,"Linear Regression controller")