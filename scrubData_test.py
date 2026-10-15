import pytest
from scrubData import scrub_data

def test_scrub_data():
    scrub_data("saturnSims/Without_Airbrakes","pytestTempDirectory")

    # test type errors

    with pytest.raises(TypeError):
        scrub_data(1,"pytestTempDirectory")

    with pytest.raises(TypeError):
        scrub_data("saturnSims/Without_Airbrakes",1)

    # test missing input directory

    with pytest.raises(ValueError):
        scrub_data("doesntExist","pytestTempDirectory")