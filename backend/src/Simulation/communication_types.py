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
    Position of this Information is inside user latitude radius.
    """

    def integrate_new_info(self):
        return super().integrate_new_info(self.generate_close_position)

    def generate_close_position(self, user_position, user_latitude):
        r = user_latitude * math.sqrt(np.random.rand())
        alpha = math.pi * np.random.rand() * 2
        x_position = math.cos(alpha) * r + user_position[0]
        if x_position < -1:
            x_position = -1
        if x_position > 1:
            x_position = 1
        y_position = math.sin(alpha) * r + user_position[1]
        if y_position > 1:
            y_position = 1
        if y_position < -1:
            y_position = -1
        return np.array([x_position, y_position])


class FilterDistantCommunication(IndividualCommunication):
    """
    Filter distant form od communication.

    In each simulation step it returns different new Information for every user
    Position of this Information is outside user latitude radius
    """

    def integrate_new_info(self):
        return super().integrate_new_info(self.generate_distant_position)

    def generate_distant_position(self, user_position, user_latitude):
        while True:
            # it may occur that on certain random x cordinate it won't be
            # possible to choose y cordinate outside a cricle, tat's why it's inside while loop
            x_position = np.random.rand() * 2 - 1
            distance_to_center = abs(x_position - user_position[0])
            if distance_to_center > user_latitude:
                # x = x_position doesn't cross a circle
                y_position = np.random.rand() * 2 - 1
                return np.array([x_position, y_position])
            if distance_to_center == user_latitude:
                # x = x_position cross a circle in one place
                y_position = np.random.rand() * 2 - 1
                while y_position == user_position[1]:
                    y_position = np.random.rand() * 2 - 1
                return np.array([x_position, y_position])
            # x = x_position cross a circle in two places
            sqr_in_circle_eq = math.sqrt(
                user_latitude ** 2 - (x_position - user_position[0]) ** 2
            )
            y_circle_1 = sqr_in_circle_eq + user_position[1]
            y_circle_2 = -sqr_in_circle_eq + user_position[1]
            if y_circle_2 > y_circle_1:
                temp = y_circle_1
                y_circle_1 = y_circle_2
                y_circle_2 = temp
            if y_circle_1 <= 1 or y_circle_2 >= -1:
                if y_circle_1 >= 1:
                    y_position = np.random.rand() * (y_circle_2 + 1) - 1
                    return np.array([x_position, y_position])
                if y_circle_2 <= -1:
                    y_position = np.random.rand() * (1 - y_circle_1) - y_circle_1
                    return np.array([x_position, y_position])
                # i can choose y cordiante "below circle" or "over a circle"
                # I randomly choose which to return
                if np.random.rand() < 0.5:
                    y_position = np.random.rand() * (y_circle_2 + 1) - 1
                    return np.array([x_position, y_position])
                y_position = np.random.rand() * (1 - y_circle_1) - y_circle_1
                return np.array([x_position, y_position])
