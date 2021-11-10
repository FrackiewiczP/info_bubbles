"""
Module with communication types implementations

List of classes:



1. CentralCommunication
2. IndividualCommunication
3. FilterDistantCommunication
4. FilterCloseCommunication


"""

import numpy as np


class Communication:
    def __init__(self, model):
        self.model = model

    def CreateInfoBit(self, user_position):
        return np.zeros((1, 3))


class IndividualCommunication(Communication):
    """
    Individual form od communication.

    In each simulation step it returns random InfoBit for every user
    """

    def create_info_bit(self, user_postion, info_bit_id):
        info_bit = np.random.rand(1, 3) * 2 - 1
        info_bit[0, 0] = info_bit_id

        return info_bit
