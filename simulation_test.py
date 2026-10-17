import pytest
from Simulation.simulation import calculate_pressure
from Simulation.simulation import calculate_drag
from Simulation.simulation import run_simulation
from controllers import constant_extension,set_constant_extension

def test_calculate_pressure():

    # test type errors
    # altitude
    with pytest.raises(TypeError):
        calculate_pressure("test", 300, 100000, 0.02)
    # seaTemp
    with pytest.raises(TypeError):
        calculate_pressure(100, "test", 100000, 0.02)
    # seaPressure
    with pytest.raises(TypeError):
        calculate_pressure(100, 300, "test", 0.02)
    # lapseRate
    with pytest.raises(TypeError):
        calculate_pressure(100, 300, 100000, "test")

    # test range errors
    # altitude below 0
    with pytest.raises(ValueError):
        calculate_pressure(-100, 300, 100000, 0.02)
    # altitude above 100,000
    with pytest.raises(ValueError):
        calculate_pressure(100100, 300, 100000, 0.02)

    # seaTemp below 250
    with pytest.raises(ValueError):
        calculate_pressure(100, 100, 100000, 0.02)
    # seaTemp above 330
    with pytest.raises(ValueError):
        calculate_pressure(100, 500, 100000, 0.02)

    # seaPressure below 70 kilopascal
    with pytest.raises(ValueError):
        calculate_pressure(100, 300, 100, 0.02)
    # seaPressure above 150 kilopascal
    with pytest.raises(ValueError):
        calculate_pressure(100, 300, 400000, 0.02)

    # lapse rate below -0.05
    with pytest.raises(ValueError):
        calculate_pressure(100, 300, 100000, -50)
    # lapse rate greater than 0.05
    with pytest.raises(ValueError):
        calculate_pressure(100, 300, 100000, 0.5)

    # test cases, values calculated manually using desmos scientific

    assert calculate_pressure(100,300,100000,0.01) == pytest.approx(98868.98899)
    assert calculate_pressure(2000,290,100100,0.008) == pytest.approx(79576.20911)
    assert calculate_pressure(1500,282,98000,0.02) == pytest.approx(82449.96662)
    assert calculate_pressure(70000,288,99999,0.016) == pytest.approx(3370.144564)
    assert calculate_pressure(455,296,102000,0.0078) == pytest.approx(96809.42093)

def test_calculate_drag():
    # test type errors
    # velocity
    with pytest.raises(TypeError):
        calculate_drag("100",1.4,0.2,1.225)
    # drag coefficient
    with pytest.raises(TypeError):
        calculate_drag(100,"1.4",0.2,1.225)
    # cross sectional area
    with pytest.raises(TypeError):
        calculate_drag(100,1.4,"0.2",1.225)
    # air density
    with pytest.raises(TypeError):
        calculate_drag(100,1.4,0.2,"1.225")

    # range checks
    # velocity too high
    with pytest.raises(ValueError):
        calculate_drag(500,1.4,0.2,1.225)
    # velocity too low
    with pytest.raises(ValueError):
        calculate_drag(-500,1.4,0.2,1.225)

    # negative drag coefficent
    with pytest.raises(ValueError):
        calculate_drag(100,-1,0.2,1.225)

    # negative area
    with pytest.raises(ValueError):
        calculate_drag(100,1.4,-0.2,1.225)

    # negative air density
    with pytest.raises(ValueError):
        calculate_drag(100,1.4,0.2,-1.225)

    assert calculate_drag(100,1.4,0.2,1.225) == pytest.approx(1715)
    assert calculate_drag(212,0.61,0.212,1.4) == pytest.approx(4068.510656)
    assert calculate_drag(12,10.1,15.6,0.81) == pytest.approx(9188.8992)
    assert calculate_drag(276,1.273,8.87,0.98) == pytest.approx(421469.6122)
    assert calculate_drag(31,1.62,0.01,1.3) == pytest.approx(10.11933)

def test_run_simulation():
    # test type errors
    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation("0.01",270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,"270",100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,"100000",0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,"0.005",250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,0.005,"250",1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,0.005,250,"1000",0.4,0.5,0.181,0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,0.005,250,1000,"0.4",0.5,0.181,0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,"0.5",0.181,0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,"0.181",0.25,24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,"0.25",24,constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,"24",constant_extension,1)

    with pytest.raises(TypeError):
        set_constant_extension(0.5)
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,"1")

    # check type for extension_function
    # should not raise an error
    set_constant_extension(0.5)
    run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # test not a function
    with pytest.raises(TypeError):
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,"constant_extension",1)

    # test with a function with incorrect arguments
    def temp_function(i,have,wrong,arguments):
        return 1
    
    with pytest.raises(TypeError):
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,temp_function,1)

    # test with a function with correct inputs but wrong return type
    def temp_function_2(alt,vel,acc,extension,seaTemp,seaPressure,lapseRate):
        return [1,2,3,4]

    with pytest.raises(TypeError):
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,temp_function_2,1)



    # test range checks

    # 0 dt
    with pytest.raises(ValueError):
        run_simulation(0,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # too high sea temp
    with pytest.raises(ValueError):
        run_simulation(0.01,1000,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # too low sea temp
    with pytest.raises(ValueError):
        run_simulation(0.01,100,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # too low ground pressure
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # too high ground pressure
    with pytest.raises(ValueError):
        run_simulation(0.01,270,1000000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # too high lapse rate
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.1,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # too low lapse rate
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,-0.1,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # velocity > mach 1
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,400,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # negative velocity
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,-250,1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # negative initial altitude
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,250,-1000,0.4,0.5,0.181,0.25,24,constant_extension,1)

    # negative coedragClosed
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,250,1000,-0.4,0.5,0.181,0.25,24,constant_extension,1)

    # negative coedragOpen
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,-0.5,0.181,0.25,24,constant_extension,1)

    # negative areaClosed
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,-0.181,0.25,24,constant_extension,1)

    # negative area open
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,-0.25,24,constant_extension,1)

    # negative mass
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,-24,constant_extension,1)

    # negative extension speed
    with pytest.raises(ValueError):
        run_simulation(0.01,270,100000,0.005,250,1000,0.4,0.5,0.181,0.25,24,constant_extension,-1)