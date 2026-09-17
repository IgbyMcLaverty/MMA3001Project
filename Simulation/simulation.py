import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator

AIR_R = 287 # J/kg*kelvin
GRAVITY = 9.81 # m/s^2

COE_DRAG = 0.39146244 # the default single coefficient of drag to be applied across the whole flight
AREA = 0.01824 # the default cross sectional area of rocket with the air brakes retracted
MASS = 24.510768830369635 # the default mass of the rocket
DT = 0.0003 # the default timestep in seconds

GAMMA = 1.4 # ratio of specific heats for air

def run_simulation_default(seaTemp, seaPressure, lapseRate, initialVelocity, initialAltitude):
    """Runs the 1DOF simulation with the time step, default coefficient of drag, cross sectional area and mass
    
    Args:
        seaTemp (float): The temperature at sea level in kelvin
        seaPressure (float): The pressure at sea level in pascal
        lapseRate (float): The change in tempature as altitude increases in degrees kelvin per meter
        initialVelocity (float): The vertical velocity which the rocket begins at in m/s
        initialAltitude (float): The altitude at which the simulation begins, does not have to be ground altitude in meters
    
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
        coeDrag=COE_DRAG,
        area=AREA,
        mass=MASS
    )

def run_simulation(dt, seaTemp, seaPressure, lapseRate, initialVelocity, initialAltitude,coeDrag,area,mass):
    """Runs the 1DOF simulation
    
    Args:
        dt (float): The timestep of the simulation in seconds
        seaTemp (float): The temperature at sea level in kelvin
        seaPressure (float): The pressure at sea level in pascal
        lapseRate (float): The change in tempature as altitude increases in degrees kelvin per meter
        initialVelocity (float): The vertical velocity which the rocket begins at in m/s
        initialAltitude (float): The altitude at which the simulation begins, does not have to be ground altitude in meters
        coeDrag (float): The coefficient of drag of the body
        area (float): The cross sectional area of the body in m^2
        mass (float): The mass of the body in kg 
    
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

    altHistory = []
    velHistory = []
    accHistory = []
    timeHistory = []
    densityHistory = []
    tempHistory = []
    pressureHistory = []

    # Force due to gravity only calculated once since the mass of the body is constant
    fGrav = GRAVITY*mass

    # temporary altitude check while the sim is behaving wrong
    while vel > 0 and alt < 90000:
        pressure = calculate_pressure(alt,seaTemp,seaPressure,lapseRate)
        temperature = seaTemp - lapseRate*alt 
        # from ideal gas law
        density = pressure/(AIR_R*temperature) # WRITE AS A FUNCTION LATER

        fDrag = calculate_drag(vel,coeDrag,area,density)
        fNet = fGrav + fDrag

        # acceleration should be negative as the forces both act downwards
        acc = -fNet/mass

        # Using naive integration
        # Assumes constant acceleration between the previous timestep and now. With the drag force at the later timestep.
        # will most likely overestimate the decrease in velocity at high dt's
        vel += acc*dt

        # Using naive integration
        # assumes constant velocity between this timestep and the now. With the velocity that velocity being at the later timestep
        # Will most likely underestimate altitude at high dt's
        alt += vel*dt

        altHistory.append(alt)
        velHistory.append(vel)
        accHistory.append(acc)
        timeHistory.append(time)
        densityHistory.append(density)
        pressureHistory.append(pressure)
        tempHistory.append(temperature)

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

# Generated by Claude then modified manually ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
def load_drag_data(filePath="drag_data.csv"):
    """Load the drag coefficient lookup table and build the 2D interpolator.

    Reads a CSV containing the columns "mach", "extension" and "cd", then
    constructs a Delaunay-based linear interpolator over the (mach, extension)
    points. The resulting interpolator is stored in the module-level global
    ``dragInterpolator`` so that ``calculate_cd`` can be called without passing
    the table around.

    Args:
        filePath (str): Path to the drag data CSV. Defaults to "drag_data.csv".

    Returns:
        scipy.interpolate.LinearNDInterpolator: The interpolator object, also
            assigned to the global ``dragInterpolator``.

    Raises:
        FileNotFoundError: If the CSV does not exist at the given path.
        ValueError: If required columns are missing, the table contains
            non-numeric or NaN entries, or there are too few unique points to
            triangulate.
    """
    global dragInterpolator

    dragFrame = pd.read_csv(filePath)

    requiredColumns = {"mach", "extension", "cd"}
    missingColumns = requiredColumns - set(dragFrame.columns)
    if missingColumns:
        raise ValueError(f"drag data is missing column(s): {sorted(missingColumns)}")

    dragFrame = dragFrame[["mach", "extension", "cd"]].apply(pd.to_numeric, errors="coerce")
    if dragFrame.isnull().values.any():
        raise ValueError("drag data contains missing or non-numeric values")

    samplePoints = dragFrame[["mach", "extension"]].to_numpy(dtype=float)
    sampleValues = dragFrame["cd"].to_numpy(dtype=float)

    if len(np.unique(samplePoints, axis=0)) < 3:
        raise ValueError("at least 3 unique (mach, extension) points are required")

    dragInterpolator = RegularGridInterpolator(samplePoints, sampleValues)
    return dragInterpolator

# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

# Generated by Claude then modified manually ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
def interpolate_coe_drag(velocity,airTemp,extension):
    """Interpolates the drag coefficient based on the CFD data

    Requires load_drag_data to have been run before being called
    
    Args:
        velocity (float): The velocity in m/s
        airTemp (float): The current air temperature in kelvin
        extension (float): The current Air Brakes extension between 0 and 1
    
    Returns:
        coeDrag: The coefficient of drag based on the current state
    """

    if dragInterpolator is None:
        raise RuntimeError("drag data not loaded - call load_drag_data() first")

    numeric_args = {
        "velocity": velocity,
        "airTemp": airTemp,
        "extension": extension
    }

    for name, value in numeric_args.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"'{name}' must be a number (int or float), got {type(value).__name__}"
            )

    if not 0.0 <= extension <= 1.0:
        raise ValueError(f"extension number must be between 0 and 1 inclusive, got {extension}")

    # calculate the speed of sound at current temperature
    a = np.sqrt(GAMMA*AIR_R*airTemp)

    # calculate mach number from velocity and speed of sound
    mach = velocity/a

    if not 0.0 <= mach <= 1.0:
        raise ValueError(f"mach number must be between 0 and 1 inclusive, got {mach}")

    dragCoefficient = float(dragInterpolator(float(mach), float(extension)))

    if np.isnan(dragCoefficient):
        raise ValueError(
            f"(mach={mach}, extension={extension}) lies outside the drag data hull"
        )

    return dragCoefficient
# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;