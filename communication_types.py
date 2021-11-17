"""
Module with communication types implementations

List of classes:



1. CentralCommunication
2. IndividualCommunication
3. FilterDistantCommunication
4. FilterCloseCommunication


"""

import random

from information import Information


class Communication:
    def __init__(self, users: dict):
        self.users = users

    def integrate_new_info(self):
        pass


class CentralCommunication(Communication):
    def __init__(self, users: dict):
        super().__init__(users)

    def integrate_new_info(self):

        info = Information()
        for index in self.users:
            u = self.users[index]
            u.try_to_integrate_info_bit(info)



class IndividualCommunication(Communication):
    """
    Individual form od communication.

    In each simulation step it returns random InfoBit for every user
    """

    def __init__(self, users: dict):
        super().__init__(users)

    def integrate_new_info(self):
        for index in self.users:
            u = self.users[index]
            info = Information()
            u.try_to_integrate_info_bit(info)

