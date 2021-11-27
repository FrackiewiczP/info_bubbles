from user_agent import UserAgent
import communication_types


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
    for i in users_to_move:
        assert users[i].user_memory.get_size() == 2
