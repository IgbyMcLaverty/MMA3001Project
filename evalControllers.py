from Simulation.simulation import run_simulation_default

def eval_controller(inputFileLoc,controller):
    """
    Uses a set of initial conditions and a provided controller and calculates evaluation criteria.
    Plots residuals for the controller against initial conditons.
    Plots histogram of achieved apogees.
    
    Args:
        inputFileLoc (string): The location of the initial condition data csv file. Include directory and .csv in string
        controller (function): A function which contains the control algorithm being evaluated
    
    Returns:
        None
    """