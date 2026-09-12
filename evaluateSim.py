from Simulation.simulation import run_simulation
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import root_mean_squared_error


def eval_on_frames(frameLoc,dt,numFrames):
    """
    Runs the sim with intial condtions from the supplied saturn sim with the set dt value. Plots residuals and RMSE.
    Coefficient of drag and cross sectional area are left as constants.
    
    Args:
        fileLoc (string): A string which contains the path to initial conditions csv.
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

    coefficientOfDrag = 0.39146244 # taken from meridian_final.csv under mach 0.6, no pitch, no roll, no extension
    crossectionalArea = 0.0754767635 # m^2
    mass = 24.510768830369635 # kg

    frame = pd.read_csv(frameLoc)

    calcApogees = []

    # each loop is a different set of initial condtions
    for i in range(numFrames):
        seaLevelTemp = frame["groundTemp"][i]
        seaLevelPressure = frame["groundPressure"][i]
        lapseRate = frame["lapserate"][i]
        initialVelocity = frame["initialVelocity"][i]
        initialAltitude = frame["initialAltitude"][i]

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

        calcApogees.append(apogee)

        print(f"progess: {(i/numFrames)*100:.0f}%",end='\r')

    rmse = root_mean_squared_error(frame.loc[0:(numFrames-1), "apogee"],calcApogees)

    print()
    print(f"All sims complete")
    print(f"final RMSE: {rmse:.2f} meters")

def eval_sim_convergance(maxdt,tolerance):
    """
    Runs the sim with the same initial conditions multiple times with decreasing values time steps.
    Each sim uses half the time step of the previous. Sims stop when the output apogee between one sim and the next drops below the tolerance
    
    Args:
        maxdt (float): The starting time step in seconds which will then be halved each interation
        tolerance (float): The acceptable absolute difference in meters between iterations after which the sims will stop.
    
    Returns:
        None
    """
    if tolerance <= 0:
        raise ValueError(f"tolerance must be greater than 0, got {tolerance}")

    # values obtained manually from saturn frame 0
    seaLevelTemp = 280.8126697952598 # kelvin
    seaLevelPressure = 98851.6944512164 # pascal
    lapseRate = 0.00118 # kelvin per meter
    initialVelocity = 239.15 # m/s
    initialAltitude = 1137.745636727661 # meters
    coefficientOfDrag = 0.39146244 # taken from meridian_final.csv under mach 0.6, no pitch, no roll, no extension
    crossectionalArea = 0.0754767635 # m^2
    mass = 24.510768830369635 # kg

    delta = 100000
    prevApogee = 0

    dt = maxdt

    while(True):
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

        delta = abs(prevApogee-apogee)

        # Stop running when sims converge
        if delta < tolerance:
            break

        prevApogee = apogee
        dt = dt/2

    print(f"Final dt:{dt}, with delta: {delta}")

        

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
#manual_sim_eval()
#eval_on_frames("saturnSims/Without_Airbrakes_Scrubbed/all_initialconds.csv",0.01,150)
eval_sim_convergance(10,0.1)