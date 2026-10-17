import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Simulation.simulation import run_simulation_default
import os

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

def eval_controller(inputFileLoc,controller,controllerName,plotHistogram=True):
    """
    Uses a set of initial conditions and a provided controller and calculates evaluation criteria.
    Initial conditions which result in over and under shooting are plot on one histogram. The undershooting and overshooting conditions are plot seperately where instead 
    of plotting the achieved apogees directly, it plots the error between what the controller achieved and the apogee if the Air Brakes had be fully extended or retracted.
    
    Args:
        inputFileLoc (string): The location of the initial condition data csv file. Include directory and .csv in string
            Columns = ["initialAltitude","initialVelocity","seaTemp","groundPressure","lapserate","undershot","overshot"]
        controller (function): A function which contains the control algorithm being evaluated
        controllerName (straing): The name of the controller which will be put in title of plots
        plotHistogram (bool): Flag for whether or not to plot the histograms of the achieved apogees. Defaults to True
    
    Returns:
        apogees (list): A 1D list containing the achieved apogees for the non-over/under shooting data.
        overshotErrors (list): A 1D list containing the errors the controller achieved on the over shooting data.
        undershotErrors (list): A 1D list containing the errors the controller achieved on the under shooting data.
    """

    argumentTypes = {
            "inputFileLoc": [inputFileLoc,str],
            "controllerName": [controllerName,str],
            "plotHistogram": [plotHistogram,bool]
        }
    
    for name, a in argumentTypes.items():
        if not isinstance(a[0], a[1]):
            raise TypeError(
                f"'{name}' must be a {a[1]}, got {type(a[0]).__name__}"
            )

    if inputFileLoc[-4:] != ".csv":
        raise ValueError("'inputFileLoc' must end in '.csv'")
    if not os.path.isfile(inputFileLoc):
        raise ValueError(f"'inputFileLoc' does not exist: {inputFileLoc}")

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

    # evaluate on the overshot data
    numConditions = len(overshotRows)
    overshotApogees = []
    overshotBestApogees = []

    set_constant_extension(1)

    for i in range(numConditions):
        seaLevelTemp = overshotRows["seaTemp"][i]
        seaLevelPressure = overshotRows["groundPressure"][i]
        lapseRate = overshotRows["lapserate"][i]
        initialVelocity = overshotRows["initialVelocity"][i]
        initialAltitude = overshotRows["initialAltitude"][i]

        simResults = run_simulation_default(
            seaTemp=seaLevelTemp,
            seaPressure=seaLevelPressure,
            lapseRate=lapseRate,
            initialAltitude=initialAltitude,
            initialVelocity=initialVelocity,
            extension_function=controller
        )

        overshotApogees.append(simResults["apogee"])

        simResults = run_simulation_default(
            seaTemp=seaLevelTemp,
            seaPressure=seaLevelPressure,
            lapseRate=lapseRate,
            initialAltitude=initialAltitude,
            initialVelocity=initialVelocity,
            extension_function=constant_extension
        )

        overshotBestApogees.append(simResults["apogee"])

    # error of the controller relative to the best achievable apogee (arrays so they can be subtracted)
    overshotErrors = np.array(overshotApogees) - np.array(overshotBestApogees)

    if plotHistogram:
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # plot histogram for non shooting data
        axes[0].hist(apogees,bins=np.arange(2000,4000,100),color="grey")
        axes[0].set_title(f"{controllerName} apogee histogram")
        axes[0].set_xlabel("Apogee")
        axes[0].set_ylabel("Occurances")

        # plot histogram for error with undershooting data
        axes[1].hist(undershotErrors,bins=np.arange(np.min(undershotErrors),5,5),color="blue")
        axes[1].set_title(f"{controllerName} undershot error histogram")
        axes[1].set_xlabel("apogee with controller vs constant extension")
        axes[1].set_ylabel("Occurances")

        # plot histogram for error with overshooting data
        axes[2].hist(overshotErrors,bins=np.arange(0,np.max(overshotErrors),5),color="red")
        axes[2].set_title(f"{controllerName} overshot error histogram")
        axes[2].set_xlabel("apogee with controller vs constant extension")
        axes[2].set_ylabel("Occurances")

        fig.tight_layout()

    return apogees, overshotErrors, undershotErrors

# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

if __name__ == "__main__":
    print("Program Start...")

    inputData = "data/validationData_initialConditions.csv"

    print("Evaluating P controller...")
    dataP,dataOSP,dataUSP = eval_controller(inputData,p_controller,"P controller",False)
    print("Evaluating linear regression...")
    dataLR,dataOSLR,dataUSLR = eval_controller(inputData,linear_regression_controller,"Linear Regression controller",False)
    print("Evaluating linear regression 2...")
    dataLR2,dataOSLR2,dataUSLR2 = eval_controller(inputData,linear_regression_2_controller,"Linear Regression 2 controller",False)
    print("Evaluating evaluating SVR...")
    dataSVR,dataOSSVR,dataUSSVR = eval_controller(inputData,svr_controller,"SVR controller",False)
    print("Evaluating NN...")
    dataNN,dataOSNN,dataUSNN = eval_controller(inputData,nn_controller,"NN controller",False)

    dataAll = [dataP, dataLR, dataLR2, dataSVR, dataNN]
    dataOSAll = [dataOSP, dataOSLR, dataOSLR2, dataOSSVR, dataOSNN]
    dataUSAll = [dataUSP, dataUSLR, dataUSLR2, dataUSSVR, dataUSNN]

    boxLabels = ["P Controller", "Linear Regression", "Linear Regression 2", "SVR", "Neural Network"]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24,7))

    # --- Left subplot: box plot ---
    ax1.boxplot(dataAll, tick_labels=boxLabels)
    # horizontal line showing the target apogee
    ax1.axhline(y=3048, color="lightgray", linestyle="--", linewidth=2,label="Target: 3048", zorder=1)
    ax1.set_title("Controller Comparison in Normal Conditions")
    ax1.set_xlabel("CONTROLLER")
    ax1.set_ylabel("Apogee (m)")

    # --- Middle subplot: overshoot response ---
    rng = np.random.default_rng(0)  # fixed seed so the jitter is repeatable
    for i, d in enumerate(dataOSAll, start=1):
        d = np.asarray(d)
        x = i + rng.uniform(-0.2, 0.2, size=len(d))  # horizontal jitter
        ax2.scatter(x, d, s=25, alpha=0.6, edgecolors="none", zorder=3)
    
    ax2.set_xticks(range(1, len(dataOSAll) + 1))
    ax2.set_xticklabels(boxLabels)

    # horizontal line to show the optimal value
    ax2.axhline(y=0, color="lightgray", linestyle="--", linewidth=2,label="Optimal value (error = 0)", zorder=1)

    ax2.set_title("Apogee Error for Overshooting Conditions")
    ax2.set_xlabel("CONTROLLER")
    ax2.set_ylabel("Error (m)")

    # --- Right subplot: undershoot response ---
    rng = np.random.default_rng(0)  # fixed seed so the jitter is repeatable
    for i, d in enumerate(dataUSAll, start=1):
        d = np.asarray(d)
        x = i + rng.uniform(-0.2, 0.2, size=len(d))  # horizontal jitter
        ax3.scatter(x, d, s=25, alpha=0.6, edgecolors="none", zorder=3)
    
    ax3.set_xticks(range(1, len(dataOSAll) + 1))
    ax3.set_xticklabels(boxLabels)

    # horizontal line to show the optimal value
    ax3.axhline(y=0, color="lightgray", linestyle="--", linewidth=2,label="Optimal value (error = 0)", zorder=1)

    ax3.set_title("Apogee Error for undershooting Conditions")
    ax3.set_xlabel("CONTROLLER")
    ax3.set_ylabel("Error (m)")

    fig.tight_layout()
    plt.show()