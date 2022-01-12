import numpy as np


class IdGenerator:
    """
    Class reposinble for generating sequential unique Information id's
    """

    __id = 0

    def get() -> int:
        """Returns new unique id

        Returns:
            int: unique id
        """
        IdGenerator.__id += 1
        return IdGenerator.__id


class Information:
    def __init__(self, data: np.ndarray = None):
        """
        By default it creates new information in random position

        But it is possible to pass ndarray of existing Information to create copy

        Args:
            data (np.ndarray, optional): Array representing another Information that we want to create copy of. Defaults to None.
        """

        if data is None:
            # first column is unique id, second and third represents information position
            data = np.random.rand(3) * 2 - 1
            data[0] = IdGenerator.get()

        self.__data = data.reshape(3)

    @property
    def position(self) -> np.ndarray:
        """Returns position of Information

        Returns:
            np.ndarray: Cordinates of Information as numpy array
        """
        return self.__data[1:3]

    @position.setter
    def position(self, pos):
        self.__data[1:3] = pos

    def to_numpy(self) -> np.ndarray:
        """Converts Information to numpy.ndarray

        Returns:
            np.ndarray: Numpy array representation of Information
        """
        return self.__data.reshape((1, 3)).copy()

    def get_id(self) -> int:
        """Returns id of Information

        Returns:
            int: Id of Information
        """
        return self.__data[0]

    def __eq__(self, other):
        return self.__data[0] == other.__data[0]

    def __str__(self) -> str:
        """
        Return text representation of Information

        Returns:
            str: Text representation of Information
        """
        return (
            "{Information id:"
            + self.__data[0]
            + "position: "
            + self.__data[1:2]
            + "}\n"
        )
