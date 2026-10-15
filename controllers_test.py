import pytest
from controllers import tune_p_controller

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