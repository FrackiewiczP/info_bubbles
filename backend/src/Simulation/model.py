"""
Module with models implementations

List of models:

1. Triple filter model


"""

import numpy as np
import pandas as pd
from mesa import Model
from Simulation.website import Website, InterUserCommunicationTypes
from Simulation.friend_links import FriendsLinksTypes
from Simulation.communication_types import CommunicationType
from Simulation.user_agent import UserAgent


class TripleFilterModel(Model):
    """
    Triple filter modelling of echo chambers and filter bubbles in social networks

    """

    def __init__(
        self,
        num_of_users,
        communication_form=CommunicationType.INDIVIDUAL,
        latitude_of_acceptance=0.5,
        sharpness_parameter=20,
        memory_size=10,
        number_of_links=10,
        link_delete_prob=0.01,
        inter_user_communication_form=InterUserCommunicationTypes.TO_ONE_RANDOM,
        initial_connections=FriendsLinksTypes.RANDOM_NON_DIRECTED,
        sd_of_user_latitudes=0.2,
        percent_of_the_same_group=80,
        no_of_groups=4
    ):

        self.num_of_users = num_of_users
        self.latitude_of_acceptance = latitude_of_acceptance
        self.sharpness_parameter = sharpness_parameter
        self.memory_size = memory_size
        self.number_of_links = number_of_links
        self.link_delete_prob = link_delete_prob
        self.iterations = 0
        self.user_positions_in_prev = {}
        users = {}
        user_positions = {}

        user_latitudes = np.random.normal(
            self.latitude_of_acceptance, sd_of_user_latitudes, size=self.num_of_users
        )

        for i in range(self.num_of_users):
            a = UserAgent(
                i,
                self,
                self.memory_size,
                user_latitudes[i],
                self.sharpness_parameter,
            )
            users[i] = a

            user_positions[i] = a.position

        self.website = Website(
            users,
            number_of_links,
            link_delete_prob,
            initial_connections,
            communication_form,
            inter_user_communication_form,
            user_positions,
            percent_of_the_same_group,
            no_of_groups
        )

        self.user_positions_in_prev[0] = dict(user_positions)

    def step(self):
        # website.step returns 3 things:
        # 1. dict, where
        # key - userId
        # value - 1x2 numpy array with user's position
        # 2. list of every link in simulation
        #   every element is pair of userID between which link exist
        # 3. mean fluctuation of users in step

        return StepData(self.website.step())


class StepData:
    """
    Class representing data from one simulation step

    """

    def __init__(self, data) -> None:
        self.users_positions = {
            str(key): list(value) for (key, value) in data[0].items()
        }
        self.links = [(int(link[0]), int(link[1])) for link in data[1]]
        self.mean_fluctuation = float(data[2])
