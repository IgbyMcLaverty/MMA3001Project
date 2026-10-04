TARGET_APOGEE = 3048 # target apogee in meters

pControllerKP = 0.01 # the propotional gain for p_controller

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

    return pControllerKP(TARGET_APOGEE-alt)

def tune_p_controller():
    """
    Uses a set of initial conditions to find best average proportional gain for those conditions.
    
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
    
