import pytest
from simulation import calculate_pressure

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

    # seaPressure below 0
    with pytest.raises(ValueError):
        calculate_pressure(100, 300, -100, 0.02)
    # seaPressure above 150 kilopascal
    with pytest.raises(ValueError):
        calculate_pressure(100, 300, 400000, 0.02)

    # lapse rate below -0.05
    with pytest.raises(ValueError):
        calculate_pressure(100, 300, 100000, -50)
    # lapse rate greater than 0.05
    with pytest.raises(ValueError):
        calculate_pressure(100, 300, 100000, 0.5)

    # test cases

    assert calculate_pressure(100,300,100,0.029) == 98.8677493469
    

    
    