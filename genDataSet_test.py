import pytest
from genDataSet import generate_data

def test_generate_data():
    generate_data("pytestTempDirectory","pytestGenData",1)

    # output file directory type error
    with pytest.raises(TypeError):
        generate_data(26,"pytestGenData",100)

    # output file name type error
    with pytest.raises(TypeError):
        generate_data("pytestTempDirectory",26,100)

    # number of trials type error
    with pytest.raises(TypeError):
        generate_data("pytestTempDirectory","pytestGenData","100")

    # number of trails equal zero
    with pytest.raises(ValueError):
        generate_data("pytestTempDirectory","pytestGenData",0)

    # number of trails is negative
    with pytest.raises(ValueError):
        generate_data("pytestTempDirectory","pytestGenData",-10)