"""
Module with communication types implementations

List of classes:



1. CentralCommunication
2. IndividualCommunication
3. FilterDistantCommunication
4. FilterCloseCommunication


"""

import numpy as np


class Communication():
    def CreateInfoBit(user_position):
        return np.zeros((1,2))


class IndividualCommunication(Communication):
    """
    Individual form od communication.

    In each simulation step it returns random InfoBit for every user
    """


    def CreateInfoBit(user_postion):
        return np.random.rand(1,2)*2 -1
