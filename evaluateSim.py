from Simulation.simulation import run_simulation
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import root_mean_squared_error


def eval_on_frames(frameLoc,dt,numFrames):
    """
    Runs the sim with intial condtions from the supplied saturn sim with the set dt value. Plots residuals and RMSE.
    Coefficient of drag and cross sectional area are left as constants.
    
    Args:
        frameLoc (string): A string which contains the path to the folder where the frames are stored. Should not include the final /
        dt (float): The dt value to be used in the sim
        numFrames (int): The number of frames to compare against. Count starts from frame 0
    
    Returns:
        None
    """

    # type and value checks for arguments

    if not isinstance(numFrames, (int)):
        raise TypeError(f"numFrames must be an integer")

    if numFrames <= 0:
        raise ValueError(f"numFrames must be > 0")

    trueApogees = []
    calcApogees = []

    # each loop is a different input frame
    for i in range(numFrames):
        frame = pd.read_csv(frameLoc+f"/frame{i}_initialconds.csv")
        seaLevelTemp = frame["groundTemp"][0]
        seaLevelPressure = frame["groundPressure"][0]
        lapseRate = frame["lapserate"][0]
        initialVelocity = frame["initialVelocity"][0]
        initialAltitude = frame["initialAltitude"][0]
        coefficientOfDrag = 0.39146244 # taken from meridian_final.csv under mach 0.6, no pitch, no roll, no extension
        crossectionalArea = 0.0754767635 # m^2
        mass = 24.510768830369635 # kg
        dt = 0.001 # seconds

        apogee,altHistory,accHistory = run_simulation(
            dt=dt,
            seaTemp=seaLevelTemp,
            seaPressure=seaLevelPressure,
            lapseRate=lapseRate,
            initialVelocity=initialVelocity,
            initialAltitude=initialAltitude,
            coeDrag=coefficientOfDrag,
            area=crossectionalArea,
            mass=mass
        )

        trueApogees.append(frame["apogee"][0])
        calcApogees.append(apogee)

    rmse = root_mean_squared_error(trueApogees,calcApogees)

    print(f"final RMSE: {rmse:.2f} meters")

        

def manual_sim_eval():
    """
    Used for debugging purposes only. Code needs to be altered in order to change initial condtions
    
    Args:
        None
    
    Returns:
        None
    """
    # values obtained manually from saturn frame 0
    seaLevelTemp = 280.8126697952598 # kelvin
    seaLevelPressure = 98851.6944512164 # pascal
    lapseRate = 0.00118 # kelvin per meter
    initialVelocity = 239.15 # m/s
    initialAltitude = 1137.745636727661 # meters
    coefficientOfDrag = 0.39146244 # taken from meridian_final.csv under mach 0.6, no pitch, no roll, no extension
    crossectionalArea = 0.0754767635 # m^2
    mass = 24.510768830369635 # kg
    dt = 0.001 # seconds

    apogee,altHistory,accHistory = run_simulation(
        dt=dt,
        seaTemp=seaLevelTemp,
        seaPressure=seaLevelPressure,
        lapseRate=lapseRate,
        initialVelocity=initialVelocity,
        initialAltitude=initialAltitude,
        coeDrag=coefficientOfDrag,
        area=crossectionalArea,
        mass=mass
    )

    print(f"Final apogee: {apogee:.2f}")

    plt.plot(altHistory)
    plt.xlabel("Index")
    plt.ylabel("altitude (m)")

    plt.show()

    plt.plot(accHistory)
    plt.xlabel("Index")
    plt.ylabel("Acceleration (m/s^2)")

    plt.show()


# uncommented required function
# manual_sim_eval()
eval_on_frames("saturnSims/Without_Airbrakes_Scrubbed",0.01,150)