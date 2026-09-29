from Simulation.simulation import run_simulation_default
import random
import os

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

RAND_SEED = 1234

OUTPUT_LOC = "data"

TARGET_ALT = 3048 # m, 10,000 feet in meters

random.seed(RAND_SEED)

# if the directory does not exist create it
if not os.path.exists(OUTPUT_LOC):
    os.makedirs(OUTPUT_LOC)

undershots = 0
overshots = 0

for i in range(NUM_TRAILS_TRAIN):
    vel = random.uniform(MIN_VEL,MAX_VEL)
    alt = random.uniform(MIN_ALT,MAX_ALT)
    temp = random.uniform(MIN_TEMP,MAX_TEMP)
    pres = random.uniform(MIN_PRES,MAX_PRES)
    lapse = random.uniform(MIN_LAPSE,MAX_LAPSE)

    ext1 = 0.0
    ext2 = 1.0

    def const_ext1(alt,vel,acc,extension,seaTemp,seaPressure):
        return ext1

    apogeeZero,timeHistory,altHistory,velHistory,accHistory,densityHistory,pressureHistory,tempHistory = run_simulation_default(
        seaTemp=temp,
        seaPressure=pres,
        lapseRate=lapse,
        initialVelocity=vel,
        initialAltitude=alt,
        extension_function=const_ext1
    )

    if apogeeZero < TARGET_ALT:
        undershots += 1
        print(f"Couldn't reach target, undershot, apogee: {apogeeZero}")
        continue

    def const_ext2(alt,vel,acc,extension,seaTemp,seaPressure):
        return ext2

    apogeeOne,timeHistory,altHistory,velHistory,accHistory,densityHistory,pressureHistory,tempHistory = run_simulation_default(
        seaTemp=temp,
        seaPressure=pres,
        lapseRate=lapse,
        initialVelocity=vel,
        initialAltitude=alt,
        extension_function=const_ext2
    )

    if apogeeOne > TARGET_ALT:
        overshots += 1
        print(f"Couldn't reach target, overshot, apogee: {apogeeOne}")
        continue

print(f"undershots: {undershots}, overshots: {overshots}")