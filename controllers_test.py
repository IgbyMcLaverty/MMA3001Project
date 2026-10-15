import pytest
import pandas as pd
from controllers import constant_extension, set_constant_extension
from controllers import tune_p_controller
from controllers import eval_controller_mean
from controllers import train_linear_regression
from controllers import train_linear_regression_2
from controllers import train_svr
from controllers import train_nn

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

    tune_p_controller("data/trainingData_initialConditions.csv",0.1,"pytestTempDirectory/p_controller_model.npz")

def test_eval_controller_mean():
    initialConditions = pd.read_csv("data/trainingData_initialConditions.csv")
    set_constant_extension(0)

    # test type errors
    with pytest.raises(TypeError):
        eval_controller_mean("initialConditions",constant_extension)
    with pytest.raises(TypeError):
        eval_controller_mean(initialConditions,"constant_extension")

    eval_controller_mean(initialConditions,constant_extension)

def test_train_linear_regression():

    # test type errors
    with pytest.raises(TypeError):
        train_linear_regression(10,"pytestTempDirectory/linear_regression_model.npz")
    with pytest.raises(TypeError):
        train_linear_regression("data/trainingData.csv",10)

    # missing input file
    with pytest.raises(ValueError):
        train_linear_regression("missing.csv","pytestTempDirectory/linear_regression_model.npz")
    # incorrect input file type
    with pytest.raises(ValueError):
        train_linear_regression("controllers.py","pytestTempDirectory/linear_regression_model.npz")
    # incorrect output type
    with pytest.raises(ValueError):
        train_linear_regression("missing.csv","pytestTempDirectory/linear_regression_model.csv")

    train_linear_regression("data/trainingData.csv","pytestTempDirectory/linear_regression_model.npz")

def test_train_linear_regression_2():

    # test type errors
    with pytest.raises(TypeError):
        train_linear_regression_2(10,"pytestTempDirectory/linear_regression_model.npz")
    with pytest.raises(TypeError):
        train_linear_regression_2("data/trainingData.csv",10)

    # missing input file
    with pytest.raises(ValueError):
        train_linear_regression_2("missing.csv","pytestTempDirectory/linear_regression_model.npz")
    # incorrect input file type
    with pytest.raises(ValueError):
        train_linear_regression_2("controllers.py","pytestTempDirectory/linear_regression_model.npz")
    # incorrect output type
    with pytest.raises(ValueError):
        train_linear_regression_2("missing.csv","pytestTempDirectory/linear_regression_model.csv")

    train_linear_regression_2("data/trainingData.csv","pytestTempDirectory/linear_regression_model.npz")

def test_train_svr():

    train_svr("data/trainingData.csv","pytestTempDirectory/svr_model.npz",2,0.1,0.1667)

    # test type errors
    with pytest.raises(TypeError):
        train_svr(21,"pytestTempDirectory/svr_model.npz",2,0.1,0.1667)
    with pytest.raises(TypeError):
        train_svr("data/trainingData.csv",123,2,0.1,0.1667)
    with pytest.raises(TypeError):
        train_svr("data/trainingData.csv","pytestTempDirectory/svr_model.npz","2",0.1,0.1667)
    with pytest.raises(TypeError):
        train_svr("data/trainingData.csv","pytestTempDirectory/svr_model.npz",2,"0.1",0.1667)
    with pytest.raises(TypeError):
        train_svr("data/trainingData.csv","pytestTempDirectory/svr_model.npz",2,0.1,"0.1667")

    # missing training file
    with pytest.raises(ValueError): 
        train_svr("data/trainingFarta.csv","pytestTempDirectory/svr_model.npz",2,0.1,0.1667)
    # incorrect input file type
    with pytest.raises(ValueError):
        train_svr("controllers.py","pytestTempDirectory/svr_model.npz",2,0.1,0.1667)
    # incorrect output file type
    with pytest.raises(ValueError):
        train_svr("data/trainingData.csv","pytestTempDirectory/svr_model.csv",2,0.1,0.1667)

def test_train_nn():
    train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation="relu",learningRate=1e-3,batchSize=128,maxEpochs=500,patience=30,valFraction=0.15,seed=0)

    # type tests
    with pytest.raises(TypeError):
        train_nn(123,"pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation="relu",learningRate=1e-3,batchSize=128,maxEpochs=500,patience=30,valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv",123,hiddenSizes=(64,64),activation="relu",learningRate=1e-3,batchSize=128,maxEpochs=500,patience=30,valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes="64",activation="relu",learningRate=1e-3,batchSize=128,maxEpochs=500,patience=30,valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,"64"),activation="relu",learningRate=1e-3,batchSize=128,maxEpochs=500,patience=30,valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation=1,learningRate=1e-3,batchSize=128,maxEpochs=500,patience=30,valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation="relu",learningRate="1e-3",batchSize=128,maxEpochs=500,patience=30,valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation="relu",learningRate=1e-3,batchSize="128",maxEpochs=500,patience=30,valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation="relu",learningRate=1e-3,batchSize=128,maxEpochs="500",patience=30,valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation="relu",learningRate=1e-3,batchSize=128,maxEpochs=500,patience="30",valFraction=0.15,seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation="relu",learningRate=1e-3,batchSize=128,maxEpochs=500,patience=30,valFraction="0.15",seed=0)

    with pytest.raises(TypeError):
        train_nn("data/trainingData.csv","pytestTempDirectory/nn_model.npz",hiddenSizes=(64,64),activation="relu",learningRate=1e-3,batchSize=128,maxEpochs=500,patience=30,valFraction=0.15,seed="0")