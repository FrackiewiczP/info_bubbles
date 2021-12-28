"""
Module with communication types implementations

List of classes:

1. CentralCommunication
2. IndividualCommunication
3. FilterDistantCommunication
4. FilterCloseCommunication


"""

from enum import Enum
from Simulation.information import Information
import numpy as np
import math


class CommunicationType(Enum):
    INDIVIDUAL = 1
    CENTRAL = 2
    FILTER_CLOSE = 3
    FILTER_DISTANT = 4


class Communication:
    def __init__(self, users: dict):
        self.users = users

    def integrate_new_info(self):
        pass


class CentralCommunication(Communication):
    """
    Central form od communication.

    In each simulation step it returns the same new Information for every user
    """

    def integrate_new_info(self):
        info = Information()
        users_to_move = set()
        for user_id in self.users:
            u = self.users[user_id]
            if u.try_to_integrate_info_bit(info):
                users_to_move.add(user_id)
        return users_to_move


class IndividualCommunication(Communication):
    """
    Individual form od communication.

    In each simulation step it returns different new Information for every user
    """

    def integrate_new_info(self, information_position_func=None):
        users_to_move = set()
        for user_id in self.users:
            u = self.users[user_id]
            info = Information()
            if information_position_func != None:
                info.position = information_position_func(u.position, u.latitude)
            u.try_to_integrate_info_bit(info)
            if u.try_to_integrate_info_bit(info):
                users_to_move.add(user_id)
        return users_to_move


class FilterCloseCommunication(IndividualCommunication):
    """
    Filter close form od communication.

    In each simulation step it returns different new Information for every user
    Position of this Information is inside user latitude radius
    """

    def integrate_new_info(self):
        super().integrate_new_info(self.generate_close_position)

    def generate_close_position(self, user_position, user_latitude):
        alpha = math.pi * np.random.rand() * 2
        x_position = math.cos(alpha) * user_latitude + user_position[0]
        y_position = math.sin(alpha) * user_latitude + user_position[1]
        return np.array([x_position, y_position])


class FilterDistantCommunication(IndividualCommunication):
    """
    Filter distant form od communication.

    In each simulation step it returns different new Information for every user
    Position of this Information is outside user latitude radius
    """

    def integrate_new_info(self):
        super().integrate_new_info(self.generate_distant_position())

    def generate_distant_position(self, user_position, user_latitude):
        while True:
            position = np.random.sample(2) * 2 - 1
            if (position[0] - user_position[0]) ** 2 + (
                position[1] - user_position[1]
            ) ** 2 > user_latitude ** 2:
                return position
