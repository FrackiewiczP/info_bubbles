"""
Module with models implementations

List of models:

1. Triple filter model


"""

from mesa import Model
from communication_types import IndividualCommunication
from user_agent import UserAgent
from mesa.time import RandomActivation
import numpy as np


class TripleFilterModel(Model):
    """
   Triple filter modelling of echo chambers and filter bubbles in social networks

    """

    def __init__(self, number_of_users, form_of_communication="individual", latitude_of_acceptance=0.5,
                 sharpness_parameter=20, memory_size=10):

        self.num_of_users = number_of_users
        self.latitude_of_acceptance = latitude_of_acceptance
        self.sharpness_parameter = sharpness_parameter
        self.memory_size = memory_size
        self.iterations=0
        self.users = {}
        self.user_positions = {}
        self.users_moved = set()

        self.schedule = RandomActivation(self)

        if form_of_communication == "individual":
            self.communication_form = IndividualCommunication()
        # standard deviation temporary hard coded
        user_latitudes = np.random.normal(self.latitude_of_acceptance, 0.2, size=self.num_of_users)

        for i in range(self.num_of_users):
            starting_position = np.random.rand(1, 2) * 2 - 1
            a = UserAgent(i, self, self.communication_form, starting_position, self.memory_size,
                          user_latitudes[i], self.sharpness_parameter,[6,7,4,2])
            self.users[i] = a
            self.user_positions[i] = starting_position

    def step(self):
        self.iterations+=1
        for i in range(self.num_of_users):
            self.users[i].communicate()

        user_order=list(range(self.num_of_users))
        np.random.shuffle(user_order)
        for i in user_order:
            self.users[i].send_info_to_friends()

        for moved_user_id in self.users_moved:
            user=self.users[moved_user_id]
            current_position = user.update_position()
            self.user_positions[user.unique_id] = current_position

        self.users_moved.clear()
