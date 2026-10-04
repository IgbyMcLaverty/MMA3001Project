import pandas as pd
import numpy as np
from Simulation.simulation import run_simulation_default
from sklearn.metrics import root_mean_squared_error

TARGET_APOGEE = 3048 # target apogee in meters

pControllerKP = 0.01 # the propotional gain for p_controller

def p_controller(alt,vel,acc,extension,seaTemp,seaPressure):
    """
    Applies a proportional gain to the altitude error (target-altitude) in order to determine extension value.
    Uses the global variable "pControllerKP" defined controllers.py as it's gain
    
    Args:
        alt (float): The current altitude of the rocket in meters
        vel (float): The current vertical velocity of the rocket in m/s
        acc (float): The current acceleration of the rocket in m/s^2
        extension (float): The current extension of the Air Brakes between 0 and 1
        seaTemp (float): The temperature at sea level in kelvin
        seaPressure (float): The pressure at sea level in pascal
    
    Returns:
        targetExtension (float): The new requested target extension based on the current conditions
    """

    return pControllerKP(TARGET_APOGEE-alt)

def tune_p_controller(inputFileLoc):
    """
    Uses a set of initial conditions to find best average proportional gain for those conditions.
    Prints the file gain to the console.
    
    Args:
        inputFileLoc (string): The location of the initial condition data csv file. Include directory and .csv in string
    
    Returns:
        None
    """

    # initial guesses for use in the false position method
    lowerKP = 0
    lowerError = None
    upperKP = 0.01
    upperError = None

    initialConditions = pd.read_csv(inputFileLoc)
    numConditions = len(initialConditions)

    for i in range(numConditions):
        print("temp")

def eval_controller(initialConditions,controller):
    """
    Takes in a set of initial conditions and a controller and returns the average apogee achieved and RMSE
    
    Args:
        initialConditions (pandas dataframe): A pandas dataframe containing the initial conditions. Columns = ["initialAltitude","initialVelocity","seaTemp","groundPressure","lapserate"]
        controller (function): A function which contains the control algorithm being evaluated
    
    Returns:
        meanApogee (float): The mean apogee achieved across all initial conditions
        standardDeviation (float): The standard deviation in the achieved apogees
    """

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

    meanApogee = np.mean(apogees)
    standardDeviation = np.std(apogees)

    return meanApogee, standardDeviation
