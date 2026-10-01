from Simulation.simulation import run_simulation_default
import random
import os
import pandas as pd

MIN_VEL = 200 # m/s
MAX_VEL = 260 # m/s

MIN_ALT = 1000 # m
MAX_ALT = 1500 # m

MIN_TEMP = 250 # Kelvin
MAX_TEMP = 310 # Kelvin

MIN_PRES = 98500 # Pascal
MAX_PRES = 100000 # Pascal

MIN_LAPSE = -0.015 # Kelvin/m
MAX_LAPSE = 0.015 # Kelvin/m

NUM_TRAILS_TRAIN = 150
NUM_TRIALS_VAL = 50
NUM_TRAILS_TEST = 100

SAMPLES_PER_TRAIL = 100

RAND_SEED = 1234

OUTPUT_LOC = "data"

TARGET_ALT = 3048 # m, 10,000 feet in meters
TARGET_TOLERANCE = 0.1 # m, altitude above or below which is considered close enough

random.seed(RAND_SEED)

# if the directory does not exist create it
if not os.path.exists(OUTPUT_LOC):
    os.makedirs(OUTPUT_LOC)

# dataframe for the initial conditions which will be saved to a csv
columnNames = ["altitude","velocity","acceleration1","seaTemp","groundPressure","lapserate","extension","undershot","overshot"]
testDataFrame = pd.DataFrame(columns = columnNames)
testDataFrameIndex = 0

undershots = 0
overshots = 0

for i in range(NUM_TRAILS_TRAIN):
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
        print(f"Couldn't reach target, undershot, apogee: {apogeeLower}")
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
            print(f"Couldn't reach target, overshot, apogee: {apogeeUpper}")
        else:
            # using the false position method to find narrow in on value

            test = 0

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

                test += 1

            print(f"extFinal = {extFinal}, apogeeBest = {apogeeBest}")
            print(f"took {test} iterations")

    
    # save result into the dataframe
    samples = random.sample(range(len(timeHistory)), SAMPLES_PER_TRAIL)
    for j in samples:
        testDataFrame.loc[testDataFrameIndex] = [altHistory[j], velHistory[j], accHistory[j], temp, pres, lapse, extFinal, undershot, overshot]
        testDataFrameIndex += 1

# save the test data to a csv
testDataFrame.to_csv(f"{OUTPUT_LOC}/testData.csv", index=False)

print(f"undershots: {undershots}, overshots: {overshots}")