from Simulation.simulation import run_simulation_default
import random
import os
import pandas as pd

from controllers import constant_extension, set_constant_extension

MIN_VEL = 200 # m/s
"""float: The minimum initial velocity to be present in the generated data in meters per second"""
MAX_VEL = 260 # m/s
"""float: The maximum initial velocity to be present in the generated data in meters per second"""

MIN_ALT = 1100 # m
"""float: The minimum initial altitude to be present in the generated data in meters"""
MAX_ALT = 1500 # m
"""float: The maximum initial altitude to be present in the generated data in meters"""

MIN_TEMP = 250 # Kelvin
"""float: The minimum ground temperature to be present in the generated data in kelvin"""
MAX_TEMP = 310 # Kelvin
"""float: The maximum ground temperature to be present in the generated data in kelvin"""

MIN_PRES = 98500 # Pascal
"""float: The minimum ground pressure to be present in the generated data in pascal"""
MAX_PRES = 100000 # Pascal
"""float: The maximum ground pressure to be present in the generated data in pascal"""

MIN_LAPSE = -0.015 # Kelvin/m
"""float: The minimum lapse rate to be present in the generated data in kelvin per meter"""
MAX_LAPSE = 0.015 # Kelvin/m
"""float: The maximum lapse rate to be present in the generated data in kelvin per meter"""

NUM_TRIALS_TRAIN = 150
"""int: The number of initial conditions to generate for the training data"""
NUM_TRIALS_VAL = 150
"""int: The number of initial conditions to generate for the validation data"""
NUM_TRIALS_TEST = 150
"""int: The number of initial conditions to generate for the testing data"""

SAMPLES_PER_TRAIL = 100
"""int: The number of timesteps to save per initial condition"""

RAND_SEED = 1234
"""int: The seed for the random number generator"""

TARGET_ALT = 3048 # m, 10,000 feet in meters
"""float: The target apogee which extension wil be optimised for in meters"""
TARGET_TOLERANCE = 0.1 # m, altitude above or below which is considered close enough
"""float: The distance above or below the target apogee which is considered acceptable in meters"""

def generate_data(outputDirectory,outputFileName,numberTrails):
    """
    Generates optimal Air Brakes values for a range of initial conditions.
    Initial conditions are generated randomly using the bounds specified in genDataSet.py
    Uses the false position method to find optimal extensions.
    From each set of initial conditions, a specified number of points in time are saved to the output csv file.

    Args:
        outputDirectory (string): The folder to which the data should be saved
        outputFileName (string): The name of the file which will be created in the supplied directory. Do not include .csv
        numberTrails (integer): The number ofinitial conditions to generate.
    Returns:
    - **None**
    """
    # type checks for input arguments
    if not isinstance(outputDirectory,str):
        raise TypeError(f"outputDirectory must be a string: got {type(outputDirectory).__name__}")
    if not isinstance(outputFileName,str):
        raise TypeError(f"outputFileName must be a string: got {type(outputFileName).__name__}")
    if isinstance(numberTrails, bool) or not isinstance(numberTrails, int):
        raise TypeError(f"numberTrails must be an integer: got {type(numberTrails).__name__}")

    if numberTrails <= 0:
        raise ValueError(f"numberTrails must be greater than 1: got {numberTrails}")

    # if the directory does not exist create it
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    # dataframe for the data at a given timestep which will be saved
    columnNames = ["altitude","velocity","acceleration","seaTemp","groundPressure","lapserate","extension","undershot","overshot"]
    dataFrame = pd.DataFrame(columns = columnNames)
    dataFrameIndex = 0

    # dataframe for the initial conditions used for each set of data
    initialConditionColumnNames = ["initialAltitude","initialVelocity","seaTemp","groundPressure","lapserate","undershot","overshot"]
    initialConditions = pd.DataFrame(columns = initialConditionColumnNames)
    initialConditionsIndex = 0

    undershots = 0
    overshots = 0

    for i in range(numberTrails):
        vel = random.uniform(MIN_VEL,MAX_VEL)
        alt = random.uniform(MIN_ALT,MAX_ALT)
        temp = random.uniform(MIN_TEMP,MAX_TEMP)
        pres = random.uniform(MIN_PRES,MAX_PRES)
        lapse = random.uniform(MIN_LAPSE,MAX_LAPSE)

        extLower = 0.0
        extUpper = 1.0

        extFinal = None
        undershot = 0
        overshot = 0

        # run the simulation with the minimum possible extension

        set_constant_extension(extLower)

        lowerSimResults = run_simulation_default(
            seaTemp=temp,
            seaPressure=pres,
            lapseRate=lapse,
            initialVelocity=vel,
            initialAltitude=alt,
            extension_function=constant_extension
        )

        apogeeLower = lowerSimResults["apogee"]

        # if the even with the minimum possible extension we don't reach apogee,
        # we should at least get as close as possible. Hence we save 0 as our correct extension.
        if apogeeLower < TARGET_ALT:
            undershots += 1
            extFinal = extLower
            undershot = 1
        else:
            set_constant_extension(extUpper)

            upperSimResults = run_simulation_default(
                seaTemp=temp,
                seaPressure=pres,
                lapseRate=lapse,
                initialVelocity=vel,
                initialAltitude=alt,
                extension_function=constant_extension
            )

            apogeeUpper = upperSimResults["apogee"]

            if apogeeUpper > TARGET_ALT:
                overshots += 1
                extFinal = extUpper
                overshot = 1
            else:
                # using the false position method to find narrow in on value

                apogeeBest = 0
                while(abs(apogeeBest-TARGET_ALT) > TARGET_TOLERANCE):
                    errorLower = apogeeLower - TARGET_ALT
                    errorUpper = apogeeUpper - TARGET_ALT
                    extFinal = (errorUpper*extLower - errorLower*extUpper)/(errorUpper - errorLower)

                    set_constant_extension(extFinal)

                    newSimResults = run_simulation_default(
                        seaTemp=temp,
                        seaPressure=pres,
                        lapseRate=lapse,
                        initialVelocity=vel,
                        initialAltitude=alt,
                        extension_function=constant_extension
                    )

                    apogeeBest = newSimResults["apogee"]

                    if apogeeBest - TARGET_ALT > 0:
                        extLower = extFinal
                        apogeeLower = apogeeBest
                    else:
                        extUpper = extFinal
                        apogeeUpper = apogeeBest

        
        # save result into the dataframe
        if undershot == 1:
            timeHistory = lowerSimResults["timeHistory"]
            altHistory = lowerSimResults["altHistory"]
            velHistory = lowerSimResults["velHistory"]
            accHistory = lowerSimResults["accHistory"]
        elif overshot == 1:
            timeHistory = upperSimResults["timeHistory"]
            altHistory = upperSimResults["altHistory"]
            velHistory = upperSimResults["velHistory"]
            accHistory = upperSimResults["accHistory"]
        else:
            timeHistory = newSimResults["timeHistory"]
            altHistory = newSimResults["altHistory"]
            velHistory = newSimResults["velHistory"]
            accHistory = newSimResults["accHistory"]

        samples = random.sample(range(len(timeHistory)), SAMPLES_PER_TRAIL)
        for j in samples:
            dataFrame.loc[dataFrameIndex] = [altHistory[j], velHistory[j], accHistory[j], temp, pres, lapse, extFinal, undershot, overshot]
            dataFrameIndex += 1

        # save the initial condition for this set of points
        initialConditions.loc[initialConditionsIndex] = [alt, vel, temp, pres, lapse, undershot, overshot]
        initialConditionsIndex += 1

        print(f"progess: {(i/numberTrails)*100:.0f}%",end='\r')

    # save the data to a csv
    dataFrame.to_csv(f"{outputDirectory}/{outputFileName}.csv", index=False)
    print(f"Finished generating for file {outputFileName}.csv")
    print(f"undershots: {undershots}, overshots: {overshots}")

    # save the initial conditions to a seperate csv
    initialConditions.to_csv(f"{outputDirectory}/{outputFileName}_initialConditions.csv", index=False)
    print(f"Saved initial condtions to {outputFileName}_initialConditions.csv")

if __name__ == "__main__":
    random.seed(RAND_SEED)
    print("Begin dataset generation...")
    # generate training dataset
    print("Begin generating training data")
    generate_data("data","trainingData",NUM_TRIALS_TRAIN)

    # generatre validation dataset
    print("Begin generating validation data")
    generate_data("data","validationData",NUM_TRIALS_VAL)

    # generatre test dataset
    print("Begin generating test data")
    generate_data("data","testData",NUM_TRIALS_TEST)