import numpy as np


class IdGenerator:
    id = 0

    def get():
        IdGenerator.id += 1
        return IdGenerator.id


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
