import numpy as np


class IdGenerator:
    __id = 0

    def get():
        IdGenerator.__id += 1
        return IdGenerator.__id


class Information:

    def __init__(self, position: list):
        self.id = IdGenerator.get()
        self.__position = np.array(position)

    def getPosition(self):
        return self.__position

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __str__(self):
        return "{Information id:" + self.id + "position: " + self.position + "}\n"
