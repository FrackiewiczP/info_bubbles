from Simulation.user_agent import UserAgent
from Simulation import communication_types
import numpy as np


def test_central_communication(mocker):
    users = {}
    for i in range(1000):
        user = UserAgent(
            unique_id=0,
            model=mocker.MagicMock(),
            memory_capacity=10,
            user_latitude=1,
            user_sharpness=20,
        )
        users[i] = user

    central = communication_types.CentralCommunication(users)
    users_to_move = central.integrate_new_info()
    info_ids = set()
    for i in users_to_move:
        assert users[i].memory.size == 2
        for id in users[i].memory.get_info_bits_ids():
            info_ids.add(id)

    # number of unique inf among users that moved is equal to their
    # number ( one starting knowledge) + one central information passed by
    # CentralCommunication
    if not len(users_to_move) == 0:
        assert len(info_ids) == len(users_to_move) + 1


def test_individual_communication(mocker):
    users = {}
    for i in range(1000):
        user = UserAgent(
            unique_id=0,
            model=mocker.MagicMock(),
            memory_capacity=10,
            user_latitude=1,
            user_sharpness=20,
        )
        users[i] = user

    central = communication_types.IndividualCommunication(users)
    users_to_move = central.integrate_new_info()
    info_ids = set()
    for i in users_to_move:
        assert users[i].memory.size == 2
        for id in users[i].memory.get_info_bits_ids():
            info_ids.add(id)

    # number of unique inf among users that moved is equal to 2*their
    # number (one starting knowledge + one individual information passed by
    # IndividualCommunication_
    assert len(info_ids) == 2 * len(users_to_move)


def test_filter_close_communication():
    users = {}
    user_position = np.random.rand(2) * 2 - 1
    user_latitude = np.random.rand()
    filter_close = communication_types.FilterCloseCommunication(users)
    for i in range(1000):
        assert (
            np.round(
                np.linalg.norm(
                    user_position
                    - filter_close.generate_close_position(user_position, user_latitude)
                ),
                3,
            )
            <= np.round(user_latitude, 3)
        )


def test_filter_distant_communication():
    users = {}
    user_position = np.random.rand(2) * 2 - 1
    user_latitude = np.random.rand()
    filter_distant = communication_types.FilterDistantCommunication(users)
    for i in range(1000):
        assert (
            np.linalg.norm(
                user_position
                - filter_distant.generate_distant_position(user_position, user_latitude)
            )
            >= user_latitude
        )
