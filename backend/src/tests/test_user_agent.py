from Simulation.user_agent import UserAgent
from Simulation.information import Information
import numpy as np


def test_addding_info_bit_to_memory():
    inf1 = Information()
    memory = UserAgent.Memory(first_info_bit=inf1, mem_capacity=10)
    inf2 = Information()
    inf3 = Information()
    memory.add_new_info_bit(inf2)
    memory.add_new_info_bit(inf3)

    assert memory.size == 3
    assert inf2.get_id() in memory.get_info_bits_ids()
    assert inf3.get_id() in memory.get_info_bits_ids()


def test_overflowing_memory():
    inf1 = Information()
    memory_capacity = 5
    memory = UserAgent.Memory(first_info_bit=inf1, mem_capacity=memory_capacity)
    for i in range(10):
        inf = Information()
        print(inf.get_id())
        memory.add_new_info_bit(inf)

    assert memory.size == memory_capacity


def test_replacing_info_when_memory_is_full():
    inf1 = Information()
    memory_capacity = 1
    memory = UserAgent.Memory(first_info_bit=inf1, mem_capacity=memory_capacity)
    inf2 = Information()
    memory.add_new_info_bit(inf2)
    assert memory.size == memory_capacity
    assert inf2.get_id() in memory.get_info_bits_ids()
    assert inf1.get_id() not in memory.get_info_bits_ids()


def test_calculating_mean_info_position():
    no_of_inf = 10
    inf1 = Information()
    positions = [inf1.position]
    memory = UserAgent.Memory(first_info_bit=inf1, mem_capacity=no_of_inf)
    for i in range(no_of_inf - 1):
        inf = Information()
        positions.append(inf.position)
        memory.add_new_info_bit(inf)
    total_x = sum(position[0] for position in positions)
    total_y = sum(position[1] for position in positions)
    assert memory.calculate_user_position()[0] == (total_x / no_of_inf)
    assert memory.calculate_user_position()[1] == (total_y / no_of_inf)


def test_trying_to_integrate_info_second_time_fails(mocker):

    user = UserAgent(
        unique_id=0,
        model=mocker.MagicMock(),
        memory_capacity=10,
        user_latitude=1,
        user_sharpness=20,
    )

    # trying to integrate inf that he already has
    inf = Information(user.get_random_information().to_numpy())
    assert not user.try_to_integrate_info_bit(inf)
