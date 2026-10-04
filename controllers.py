import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Simulation.simulation import run_simulation_default
from sklearn.metrics import root_mean_squared_error

TARGET_APOGEE = 3048 # target apogee in meters

pControllerKP = 0 # the propotional gain for p_controller

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
    return pControllerKP*(TARGET_APOGEE-alt)

def tune_p_controller(inputFileLoc,tolerance):
    """
    Uses a set of initial conditions to find best average proportional gain for those conditions.
    Prints the file gain to the console.
    
    Args:
        inputFileLoc (string): The location of the initial condition data csv file. Include directory and .csv in string
        tolerance (float): The acceptable error above or below the target apogee in meters
    
    Returns:
        None
    """

    # load pControllerKP as a global variable so it can updated as we close in on a value
    global pControllerKP

    # initial guesses for use in the false position method
    lowerKP = 0
    lowerError = None
    upperKP = 0.01
    upperError = None

    initialConditions = pd.read_csv(inputFileLoc)

    # evaluate initial error for lower KP
    pControllerKP = lowerKP
    lowerMean,lowerSTD = eval_controller(initialConditions,p_controller)
    lowerError = TARGET_APOGEE - lowerMean
    print(f"lower KP is {lowerKP}")
    print(f"lower bound undershot by {lowerError} meters")

    # evaluate initial error for upper KP
    pControllerKP = upperKP
    upperMean,upperSTD = eval_controller(initialConditions,p_controller)
    upperError = TARGET_APOGEE - upperMean
    print(f"upper KP is {upperKP}")
    print(f"upper bound undershot by {upperError} meters")

    while abs(upperError) > tolerance:
        newKP = (upperError*lowerKP - lowerError*upperKP)/(upperError - lowerError)

        print(f"evaluating with new KP of {newKP}")

        pControllerKP = newKP
        newMean, newSTD = eval_controller(initialConditions,p_controller)

        newError = TARGET_APOGEE - newMean

        if newError < 0:
            lowerKP = newKP
            lowerError = newError
        else:
            upperKP = newKP
            upperError = newError

        print(f"Got error of {newError}")

    print(f"Final KP value of {upperKP} with error of {upperError}")


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

if __name__ == "__main__":
    print("Program Start")
    # show what happens for a single run of p controller
    """
    pControllerKP = 0.01
    simResults = run_simulation_default(
        seaTemp=20+273,
        seaPressure=100000,
        lapseRate=-0.005,
        initialVelocity=260,
        initialAltitude=1050,
        extension_function=p_controller
    )

    print(f"final apogee: {simResults['apogee']}")

    plt.plot(simResults["altHistory"],simResults["targetExtensionHistory"])
    plt.show()
    """
    tune_p_controller("data/testData_initialConditions.csv",0.1)

    
