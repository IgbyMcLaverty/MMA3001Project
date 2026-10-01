from Simulation.simulation import run_simulation_default
import random
import os
import pandas as pd

MIN_VEL = 200 # m/s
MAX_VEL = 260 # m/s

MIN_ALT = 1100 # m
MAX_ALT = 1500 # m

MIN_TEMP = 250 # Kelvin
MAX_TEMP = 310 # Kelvin

MIN_PRES = 98500 # Pascal
MAX_PRES = 100000 # Pascal

MIN_LAPSE = -0.015 # Kelvin/m
MAX_LAPSE = 0.015 # Kelvin/m

NUM_TRIALS_TRAIN = 150
NUM_TRIALS_VAL = 50
NUM_TRIALS_TEST = 100

SAMPLES_PER_TRAIL = 100

RAND_SEED = 1234

TARGET_ALT = 3048 # m, 10,000 feet in meters
TARGET_TOLERANCE = 0.1 # m, altitude above or below which is considered close enough

random.seed(RAND_SEED)

def generate_data(outputDirectory,outputFileName,numberTrails):
    """
    Generates optimal Air Brakes values for a range of initial conditions.
    Initial conditions are generated randomly using the bounds specified in genDataSet.py
    Uses the false position method to find optimal extensions.
    From each set of initial conditions, a specified number of points in time are saved to the output csv file.

    Args:
        outputDirectory (string): The folder to which the data should be saved
        outputFileName (string): The name of the file which will be created in the supplied directory. Do not include .csv
        numberTrails (integer): The number of sets of initial conditions to generate.
    """
    # if the directory does not exist create it
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    # dataframe for the initial conditions which will be saved to a csv
    columnNames = ["altitude","velocity","acceleration1","seaTemp","groundPressure","lapserate","extension","undershot","overshot"]
    dataFrame = pd.DataFrame(columns = columnNames)
    dataFrameIndex = 0

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

        def const_extLower(alt,vel,acc,extension,seaTemp,seaPressure):
            return extLower

        apogeeLower,timeHistory,altHistory,velHistory,accHistory,densityHistory,pressureHistory,tempHistory = run_simulation_default(
            seaTemp=temp,
            seaPressure=pres,
            lapseRate=lapse,
            initialVelocity=vel,
            initialAltitude=alt,
            extension_function=const_extLower
        )

        # if the even with the minimum possible extension we don't reach apogee,
        # we should at least get as close as possible. Hence we save 0 as our correct extension.
        if apogeeLower < TARGET_ALT:
            undershots += 1
            extFinal = extLower
            undershot = 1
        else:
            def const_extUpper(alt,vel,acc,extension,seaTemp,seaPressure):
                return extUpper

            apogeeUpper,timeHistory,altHistory,velHistory,accHistory,densityHistory,pressureHistory,tempHistory = run_simulation_default(
                seaTemp=temp,
                seaPressure=pres,
                lapseRate=lapse,
                initialVelocity=vel,
                initialAltitude=alt,
                extension_function=const_extUpper
            )

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

                    def const_extFinal(alt,vel,acc,extension,seaTemp,seaPressure):
                        return extFinal

                    apogeeBest,timeHistory,altHistory,velHistory,accHistory,densityHistory,pressureHistory,tempHistory = run_simulation_default(
                        seaTemp=temp,
                        seaPressure=pres,
                        lapseRate=lapse,
                        initialVelocity=vel,
                        initialAltitude=alt,
                        extension_function=const_extFinal
                    )

                    if apogeeBest - TARGET_ALT > 0:
                        extLower = extFinal
                        apogeeLower = apogeeBest
                    else:
                        extUpper = extFinal
                        apogeeUpper = apogeeBest

        
        # save result into the dataframe
        samples = random.sample(range(len(timeHistory)), SAMPLES_PER_TRAIL)
        for j in samples:
            dataFrame.loc[dataFrameIndex] = [altHistory[j], velHistory[j], accHistory[j], temp, pres, lapse, extFinal, undershot, overshot]
            dataFrameIndex += 1

        print(f"progess: {(i/numberTrails)*100:.0f}%",end='\r')

    # save the test data to a csv
    dataFrame.to_csv(f"{outputDirectory}/{outputFileName}.csv", index=False)
    print(f"Finished generating for file {outputFileName}.csv")
    print(f"undershots: {undershots}, overshots: {overshots}")

# generate training dataset
generate_data("data","trainingData",NUM_TRIALS_TRAIN)

# generatre validation dataset
generate_data("data","validationData",NUM_TRIALS_VAL)

# generatre test dataset
generate_data("data","testData",NUM_TRIALS_TEST)