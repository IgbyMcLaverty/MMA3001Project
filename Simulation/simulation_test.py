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
    

    
    