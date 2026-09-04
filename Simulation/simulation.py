import numpy as np

def run_simulation(dt, groundTemp, groundPressure, groundAltitude, lapseRate, initialVelocity, initialAltitude):
    """Runs the 1DOF simulation
    
    Args:
        dt (float): The timestep of the simulation
        groundTemp (float): The temperature at ground level in Kelvin
        groundPressure (float): The pressure at ground level in kilopascal
        groundAltitude (float): The altitude above sea level at ground level in meters; the altitude at which the ground temperature and pressure were measured at
        lapseRate (float): The change in tempature as altitude increases in degrees celius per kilometer
        initialVelocity (float): The vertical velocity which the rocket begins at
        initialAltitude (float): The altitude at which the simulation begins, does not have to be ground altitude
    
    Returns:
        apogee (float): The maximum altitude the simulation reached in meters

    """

    print("Hello I am the run_simulation function!")