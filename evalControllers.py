import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Simulation.simulation import run_simulation_default

from controllers import p_controller
from controllers import linear_regression_controller
from controllers import linear_regression_2_controller
from controllers import svr_controller
from controllers import nn_controller
from controllers import constant_extension,set_constant_extension
from controllers import TARGET_APOGEE
from controllers import SVR_MODEL_FILE
from controllers import _svrModel

# Written manually then modified by Claude ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

def eval_controller(inputFileLoc,controller,controllerName):
    """
    Uses a set of initial conditions and a provided controller and calculates evaluation criteria.
    Rows where undershot or overshot equal 1 are excluded from the evaluation. The excluded rows are
    kept in separate dataframes (undershotRows and overshotRows) for later use.
    Plots residuals for the controller against initial conditons.
    Plots histogram of achieved apogees.
    
    Args:
        inputFileLoc (string): The location of the initial condition data csv file. Include directory and .csv in string
            Columns = ["initialAltitude","initialVelocity","seaTemp","groundPressure","lapserate","undershot","overshot"]
        controller (function): A function which contains the control algorithm being evaluated
        controllerName (straing): The name of the controller which will be put in title of plots
    
    Returns:
        None
    """

    allConditions = pd.read_csv(inputFileLoc)

    # split off the rows that undershot and the rows that overshot
    undershotRows = allConditions[allConditions["undershot"] == 1].copy()
    undershotRows = undershotRows.reset_index(drop=True)
    overshotRows = allConditions[allConditions["overshot"] == 1].copy()
    overshotRows = overshotRows.reset_index(drop=True)

    # only evaluate the runs that neither undershot nor overshot the target apogee,
    # and reset the index so the rows can be accessed as 0 to numConditions-1
    initialConditions = allConditions[(allConditions["undershot"] == 0) & (allConditions["overshot"] == 0)]
    initialConditions = initialConditions.reset_index(drop=True)
    print(f"Evaluating {len(initialConditions)} of {len(allConditions)} rows "
          f"({len(undershotRows)} undershot, {len(overshotRows)} overshot)")

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

    # evaluate on the undershot data
    numConditions = len(undershotRows)
    undershotApogees = []
    undershotBestApogees = []

    set_constant_extension(0)

    for i in range(numConditions):
        seaLevelTemp = undershotRows["seaTemp"][i]
        seaLevelPressure = undershotRows["groundPressure"][i]
        lapseRate = undershotRows["lapserate"][i]
        initialVelocity = undershotRows["initialVelocity"][i]
        initialAltitude = undershotRows["initialAltitude"][i]

        simResults = run_simulation_default(
            seaTemp=seaLevelTemp,
            seaPressure=seaLevelPressure,
            lapseRate=lapseRate,
            initialAltitude=initialAltitude,
            initialVelocity=initialVelocity,
            extension_function=controller
        )

        undershotApogees.append(simResults["apogee"])

        simResults = run_simulation_default(
            seaTemp=seaLevelTemp,
            seaPressure=seaLevelPressure,
            lapseRate=lapseRate,
            initialAltitude=initialAltitude,
            initialVelocity=initialVelocity,
            extension_function=constant_extension
        )

        undershotBestApogees.append(simResults["apogee"])

    # error of the controller relative to the best achievable apogee (arrays so they can be subtracted)
    undershotErrors = np.array(undershotApogees) - np.array(undershotBestApogees)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    axes[0].hist(apogees,bins=np.arange(2000,4000,100))
    axes[0].set_title(f"{controllerName} apogee histogram")
    axes[0].set_xlabel("Apogee")
    axes[0].set_ylabel("Occurances")

    axes[1].hist(undershotErrors,bins=np.arange(-100,5,5))
    axes[1].set_title(f"{controllerName} undershot error histogram")
    axes[1].set_xlabel("apogee with controller vs constant extension")
    axes[1].set_ylabel("Occurances")

    # third subplot is reserved for the overshot errors, hidden until it is filled in
    axes[2].axis("off")

    fig.tight_layout()
    plt.show()

# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

if __name__ == "__main__":
    #eval_controller("data/validationData_initialConditions.csv",p_controller,"P controller")
    #eval_controller("data/validationData_initialConditions.csv",linear_regression_controller,"Linear Regression controller")
    eval_controller("data/validationData_initialConditions.csv",linear_regression_2_controller,"Linear Regression 2 controller")
    #eval_controller("data/validationData_initialConditions.csv",svr_controller,"SVR controller")
    #eval_controller("data/validationData_initialConditions.csv",nn_controller,"NN controller")