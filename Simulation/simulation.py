import numpy as np

AIR_R = 287 # J/kg*kelvin
GRAVITY = 9.81 # m/s^2

COE_DRAG_CLOSED = 0.39146244 # the default coefficient of drag with the flaps retracted to be applied across the whole flight
COE_DRAG_OPEN = 0.53332019 # the default coefficient of drag with the flaps extended to be applied across the whole flight
AREA_CLOSED = 0.01824 # the default cross sectional area of rocket with the air brakes retracted
AREA_OPEN = AREA_CLOSED + 0.0108 # the default cross sectional area of rocket with the air brakes extended
MASS = 24.510768830369635 # the default mass of the rocket
DT = 0.005 # the default timestep in seconds

def run_simulation_default(seaTemp, seaPressure, lapseRate, initialVelocity, initialAltitude, extension_function):
    """Runs the 1DOF simulation with the time step, default coefficient of drag, cross sectional area and mass
    
    Args:
        seaTemp (float): The temperature at sea level in kelvin
        seaPressure (float): The pressure at sea level in pascal
        lapseRate (float): The change in tempature as altitude increases in degrees kelvin per meter
        initialVelocity (float): The vertical velocity which the rocket begins at in m/s
        initialAltitude (float): The altitude at which the simulation begins, does not have to be ground altitude in meters
        extension_function (function): The function which takes in the rocket state and returns the requested Air Brakes extension. See run_simulation for argument structure
    
    Returns:
        apogee (float): The maximum altitude the simulation reached in meters
        timeHistory (list): A list containing the time of each timestep
        altHistory (list): A list containing the calculated altitude at each timestep
        accHistory (list): A list containing the calculated acceleration at each timestep
        densityHistory (list): A list containing the calcualte air density at each timestep
        tempHistory (list): A list containing the calculated temperature at each timestep
        pressureHistory (list): A list containing the calculated pressure at each timestep

    """

    return run_simulation(
        dt=DT,
        seaTemp= seaTemp,
        seaPressure=seaPressure,
        lapseRate=lapseRate,
        initialAltitude=initialAltitude,
        initialVelocity=initialVelocity,
        coeDragClosed=COE_DRAG_CLOSED,
        coeDragOpen=COE_DRAG_OPEN,
        areaClosed=AREA_CLOSED,
        areaOpen=AREA_OPEN,
        mass=MASS,
        extension_function=extension_function,
        extensionSpeed=0
    )

def run_simulation(dt, seaTemp, seaPressure, lapseRate, initialVelocity, initialAltitude,coeDragClosed,coeDragOpen,areaClosed,areaOpen,mass,extension_function,extensionSpeed):
    """Runs the 1DOF simulation
    
    Args:
        dt (float): The timestep of the simulation in seconds
        seaTemp (float): The temperature at sea level in kelvin
        seaPressure (float): The pressure at sea level in pascal
        lapseRate (float): The change in tempature as altitude increases in degrees kelvin per meter
        initialVelocity (float): The vertical velocity which the rocket begins at in m/s
        initialAltitude (float): The altitude at which the simulation begins, does not have to be ground altitude in meters
        coeDragClosed (float): The coefficient of drag of the body with the flaps retracted
        coeDragOpen (float): The coefficient of drag of the body with the flaps extended
        areaClosed (float): The cross sectional area of the body with the flaps retracted in m^2
        areaOpen (float): The cross sectional area of the body with the flaps extened in m^2
        mass (float): The mass of the body in kg 
        extension_function (function): The function which takes in the rocket state and returns the requested Air Brakes extension. Must return a single float. Arguments: alt (altitude in meters), vel (velocity in m/s), acc (acceleration in m/s^2), currExt (The current extension between 0 and 1), gndTemp (The ground temperature in Kelvin), gndPres (The ground pressure in pascal)
        extensionSpeed (float): The time taken to extended from 0 to 100 percent in seconds. Set to 0 for no extension delay
    
    Returns:
        apogee (float): The maximum altitude the simulation reached in meters
        timeHistory (list): A list containing the time of each timestep
        altHistory (list): A list containing the calculated altitude at each timestep
        accHistory (list): A list containing the calculated acceleration at each timestep
        densityHistory (list): A list containing the calcualte air density at each timestep
        tempHistory (list): A list containing the calculated temperature at each timestep
        pressureHistory (list): A list containing the calculated pressure at each timestep

    """
    vel = initialVelocity
    alt = initialAltitude
    time = 0
    extension = 0

    if extensionSpeed > 0:
        maxExtensionDelta = dt/extensionSpeed

    altHistory = []
    velHistory = []
    accHistory = []
    timeHistory = []
    densityHistory = []
    tempHistory = []
    pressureHistory = []
    extensionHistory = []
    targetExtensionHistory = []

    # Force due to gravity only calculated once since the mass of the body is constant
    fGrav = GRAVITY*mass

    # temporary altitude check while the sim is behaving wrong
    while vel > 0 and alt < 90000:
        # first round of RK2
        pressure = calculate_pressure(alt,seaTemp,seaPressure,lapseRate)
        temperature = seaTemp + lapseRate*alt 
        # from ideal gas law
        density = pressure/(AIR_R*temperature) # WRITE AS A FUNCTION LATER

        coeDrag = coeDragClosed + (coeDragOpen-coeDragClosed)*extension
        area = areaClosed + (areaOpen-areaClosed)*extension

        fDrag = calculate_drag(vel,coeDrag,area,density)
        fNet = fGrav + fDrag

        # acceleration should be negative as the forces both act downwards
        acc1 = -fNet/mass

        # evaluate altitude and velocity at at the half step.
        alt1 = alt + vel*dt/2
        vel1 = vel + acc1*dt/2

        # recalculate the acceleration at this midpoint

        pressure2 = calculate_pressure(alt1,seaTemp,seaPressure,lapseRate)
        temperature2 = seaTemp + lapseRate*alt1 
        # from ideal gas law
        density2 = pressure2/(AIR_R*temperature2) # WRITE AS A FUNCTION LATER

        fDrag2 = calculate_drag(vel1,coeDrag,area,density2)
        fNet2 = fGrav + fDrag2

        # acceleration should be negative as the forces both act downwards
        acc = -fNet2/mass

        # use the acceleration from the midpoint as the average acceleration
        vel += acc*dt

        # Using naive integration
        # assumes constant velocity between this timestep and the now. With the velocity that velocity being at the later timestep
        # Will most likely underestimate altitude at high dt's
        alt += vel*dt

        # calculate the target extension based on the input algorithm
        TargetExtension = extension_function(alt,vel,acc,extension,seaTemp,seaPressure)

        # limit the target extension to between 0 and 1
        if TargetExtension < 0: TargetExtension = 0
        if TargetExtension > 1: TargetExtension = 1

        if extensionSpeed > 0:
            # if within 1 step of the target, set extension exactly to the target
            if extension > TargetExtension-maxExtensionDelta and extension < TargetExtension+maxExtensionDelta:
                extension = TargetExtension
            # other wise, increase or decrease by the maximum amount allowed
            elif extension < TargetExtension: extension += maxExtensionDelta
            else: extension += maxExtensionDelta
        else:
            extension = TargetExtension


        altHistory.append(alt)
        velHistory.append(vel)
        accHistory.append(acc)
        timeHistory.append(time)
        densityHistory.append(density)
        pressureHistory.append(pressure)
        tempHistory.append(temperature)
        extensionHistory.append(extension)

        time += dt

    return alt,timeHistory,altHistory,velHistory,accHistory,densityHistory,pressureHistory,tempHistory

def calculate_pressure(altitude, seaTemp, seaPressure, lapseRate):
    """Calculates the pressure at a given altitude using the barometric formula

    Args:
        altitude (float): The altitude to evaluate the pressure at in meters
        seaTemp (float): The temperature at sea level in Kelvin
        seaPressure (float): The pressure at sea level in pascal
        lapseRate (float): The change in tempature as altitude increases in kelvin per meter
    
    Returns:
        pressure (float): The pressure at the given altitude in pascal
    """

    # Generated by Claude then modified manually ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    # ---- Type checks ----
    # bool is a subclass of int, so explicitly exclude it to avoid True/False
    # silently passing as 1/0.
    numeric_args = {
        "altitude": altitude,
        "seaTemp": seaTemp,
        "seaPressure": seaPressure,
        "lapseRate": lapseRate,
    }

    for name, value in numeric_args.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"'{name}' must be a number (int or float), got {type(value).__name__}"
            )

    # ---- Range checks ----
    # Altitude: do not allow for negative altitudes. Maximum value up to edge of usable atmosphere for the barometric formula.
    if not (0 <= altitude <= 100_000.0):
        raise ValueError(
            f"'altitude' must be between 0 and 100000 meters, got {altitude}"
        )

    # sea temperature: must be a physically valid, positive Kelvin value.
    # Limited between reasonable upper and lower bounds, approximately -20 to 60 degrees celius
    if not (250 <= seaTemp <= 330):
        raise ValueError(
            f"'seaTemp' must be between -250 and 330 Kelvin, got {seaTemp}"
        )

    # sea pressure: must be positive; upper bound generous (sea-level is
    # ~101325 Pa, extreme highs are still well under 150000 Pa). Lower bound set to prevent accidentally inputting kilopascal
    if not (70_000 < seaPressure <= 150_000.0):
        raise ValueError(
            f"'seaPressure' must be between 0 (exclusive) and 150000 pascal, got {seaPressure}"
        )

    # Lapse rate: typical atmospheric lapse rates are a few degrees C per km;
    # allow a generous margin for unusual/inverted conditions.
    if not (-0.05 <= lapseRate <= 0.05):
        raise ValueError(
            f"'lapseRate' must be between -0.05 and 0.05 Kelvin per meter, got {lapseRate}"
        )
    # ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    # define constants
    g = 9.81 # acceleration due to gravity in m/s^2
    R0 = 8.314462618 # univeral gas constant
    M = 0.02896968 # molar mass of air
    return seaPressure*(1+lapseRate*altitude/seaTemp)**(-g*M/(R0*lapseRate))

def calculate_drag(velocity, coeDrag, area, airDensity):
    """Calculate the force due to drag given the velocity, body parameters and air density
    
    Args:
        velocity (float): The velocity in m/s
        coeDrag (float): The coefficient of drag for the body
        area (float): the cross sectional area of the body in m^2
        airDensity (float): The air density in kg/m^3
    
    Returns:
        dragForce (float): The drag force experienced by the body in Newtons
    """

    # do type checks on all inputs
    numeric_args = {
        "altitude": velocity,
        "seaTemp": coeDrag,
        "seaPressure": area,
        "lapseRate": airDensity,
    }

    for name, value in numeric_args.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"'{name}' must be a number (int or float), got {type(value).__name__}"
            )

    # range check for velocity. Should be less than the speed of sound in either direction
    if not (-343 <= velocity <= 343):
        raise ValueError(
            f"'velocity' must be between -343 and 343 meters per second, got {velocity}"
        )
    
    # range check for coeDrag. Should be greater than or equal to 0
    if not (0 <= coeDrag):
        raise ValueError(
            f"'coeDrag' must be greater than or equal to 0, got {coeDrag}"
        )

    # range check for area. Must be greater than 0
    if not (0 < area):
        raise ValueError(
            f"'area' must be greater 0 square meters, got {area}"
        )

    # range check for density. Should be greater than 0
    if not (airDensity > 0):
        raise ValueError(
            f"'airDensity' must greater than 0 kg/m^3, got {airDensity}"
        )

    # actually calculate the drag
    return 0.5*airDensity*velocity**2*coeDrag*area