import numpy as np


def integration_probability(position1, position2, latitude, sharpness):
    dist = np.linalg.norm(position1 - position2)
    probability = latitude ** sharpness / (dist ** sharpness + latitude ** sharpness)
    return probability


def check_integration(position1, position2, latitude, sharpness):
    return np.random.rand() <= integration_probability(
        position1, position2, latitude, sharpness
    )


def check_link_integration(
    position1, position2, latitude, sharpness, refriend_probability
):
    return np.random.rand() <= refriend_probability * (
        1 - integration_probability(position1, position2, latitude, sharpness)
    )
