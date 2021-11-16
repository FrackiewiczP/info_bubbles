import numpy as np


class IdGenerator:
    __id = 0

    def get():
        IdGenerator.__id += 1
        return IdGenerator.__id


class Information:

    def copy(data):
        i = Information([1,1])
        i.__data = data.copy().reshape((3, 1))
        return i

    def __init__(self, position: list):
        position.insert(0,IdGenerator.get())
        self.__data = np.array(position).reshape((3, 1))

    def getPosition(self):
        return self.__data[1:2]

    def getAllData(self):
        return self.__data

    def __eq__(self, other):
        if self.__data[0] == other.__data[0]:
            return True
        return False

    def __str__(self):
        return "{Information id:" + self.__data[0] + "position: " + self.__data[1:2] + "}\n"
