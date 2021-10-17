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
        self.users = {}

        self.schedule = RandomActivation(self)

        if form_of_communication == "individual":
            self.communication_form = IndividualCommunication()
        # standard deviation temporary hard coded
        user_latitudes = np.random.normal(self.latitude_of_acceptance, 0.2, size=self.num_of_users)

        for i in range(self.num_of_users):
            a = UserAgent(i, self, self.communication_form, np.random.rand(1, 2) * 2 - 1, self.memory_size,
                          user_latitudes[i], self.sharpness_parameter)
            self.schedule.add(a)
            self.users[i] = a
