import numpy as np


class IdGenerator:
    __id = 0

    def get():
        IdGenerator.__id += 1
        return IdGenerator.__id


class Information:
    def __init__(self, data: np.ndarray = None):
        """
        By default it creates new information in random position

        But it is possible to pass ndarray of existing information to create copy
        """

        if data is None:
            # first column is unique id, second and third represents information position
            data = np.random.rand(3) * 2 - 1
            data[0] = IdGenerator.get()

        self.__data = data.reshape(3)

    def get_position(self):
        return self.__data[1:2]

    def to_numpy(self):
        return self.__data.reshape((1, 3))

    def get_id(self):
        return self.__data[0]

    def __eq__(self, other):
        return self.__data[0] == other.__data[0]

    def __str__(self):
        return (
            "{Information id:"
            + self.__data[0]
            + "position: "
            + self.__data[1:2]
            + "}\n"
        )
