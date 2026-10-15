import pytest
import pandas as pd
from controllers import constant_extension, set_constant_extension
from controllers import tune_p_controller
from controllers import eval_controller_mean

def test_tune_p_controller():
    # test type checks
    with pytest.raises(TypeError):
        tune_p_controller(100,0.1,"pytestTempDirectory/p_controller_model.npz")
    with pytest.raises(TypeError):
        tune_p_controller("data/trainingData_initialConditions.csv","0.1","pytestTempDirectory/p_controller_model.npz")
    with pytest.raises(TypeError):
        tune_p_controller("data/trainingData_initialConditions.csv",0.1,16)

    # input file doesn't exist
    with pytest.raises(ValueError):
        tune_p_controller("bungus.csv",0.1,"pytestTempDirectory/p_controller_model.npz")
    # wrong input file type
    with pytest.raises(ValueError):
        tune_p_controller("controllers.py",0.1,"pytestTempDirectory/p_controller_model.npz")
    # wrong output file type
    with pytest.raises(ValueError):
        tune_p_controller("data/trainingData_initialConditions.csv",0.1,"pytestTempDirectory/bungus.csv")
    with pytest.raises(ValueError):
        tune_p_controller("data/trainingData_initialConditions.csv",-10,"pytestTempDirectory/p_controller_model.npz")

def test_eval_controller_mean():
    initialConditions = pd.read_csv("data/trainingData_initialConditions.csv")
    set_constant_extension(0)

    # test type errors
    with pytest.raises(TypeError):
        eval_controller_mean("initialConditions",constant_extension)
    with pytest.raises(TypeError):
        eval_controller_mean(initialConditions,"constant_extension")

    eval_controller_mean(initialConditions,constant_extension)