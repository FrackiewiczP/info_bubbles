import Simulation.integration_function as integration_function
import numpy as np


def test_integration_zero_distance():
    position1 = np.array([0, 0])
    position2 = np.array([0, 0])
    assert (
        integration_function.check_integration(
            position1=position1, position2=position2, latitude=0.5, sharpness=20
        )
        == True
    )
