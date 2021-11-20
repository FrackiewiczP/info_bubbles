"""
Module with communication types implementations

List of classes:



1. CentralCommunication
2. IndividualCommunication
3. FilterDistantCommunication
4. FilterCloseCommunication


"""

from Simulation.information import Information
import numpy as np

class Communication:
    def __init__(self, users: dict):
        self.users = users

    def integrate_new_info(self):
        pass

class FromFileCentralCommunication(Communication):
    def __init__(self, users: dict, info_in_steps:list):
        super().__init__(users)
        self.info = np.array(info_in_steps)
        self.step =0

    def integrate_new_info(self):
        info = Information(self.info[self.step,0:3])
        self.step +=1
        users_to_move = set()
        for index in self.users:
            u = self.users[index]
            if u.try_to_integrate_info_bit(info):
                users_to_move.add(index)
        return users_to_move



class CentralCommunication(Communication):
    def __init__(self, users: dict):
        super().__init__(users)

    def integrate_new_info(self):
        info = Information()
        users_to_move = set()
        for index in self.users:
            u = self.users[index]
            if u.try_to_integrate_info_bit(info):
                users_to_move.add(index)
        return users_to_move


class IndividualCommunication(Communication):
    """
    Individual form od communication.

    In each simulation step it returns random InfoBit for every user
    """

    def __init__(self, users: dict):
        super().__init__(users)

    def integrate_new_info(self):
        users_to_move = set()
        for index in self.users:
            u = self.users[index]
            info = Information()
            u.try_to_integrate_info_bit(info)
            if u.try_to_integrate_info_bit(info):
                users_to_move.add(index)
        return users_to_move
