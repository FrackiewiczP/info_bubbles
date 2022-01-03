from Simulation.information import Information
import numpy as np


def test_id_uniqueness():
    id_list = list()
    for i in range(1000):
        id_list.append(Information().get_id())
    assert len(set(id_list)) == len(id_list)


def test_memory_sharing():
    inf = Information()
    inf_data = inf.to_numpy()
    assert not np.shares_memory(inf_data, inf.to_numpy())


def test_creating_from_ndarray_and_getters():
    id = 1
    x_cord = 0.05
    y_cord = 0.78
    data = np.array([id, x_cord, y_cord])
    inf = Information(data)
    assert inf.get_id() == id
    assert inf.position[0] == x_cord
    assert inf.position[1] == y_cord
    assert inf.position.shape == (2,)


def test_eq():
    inf1 = Information()
    inf2 = Information(inf1.to_numpy())
    assert inf1 == inf2
