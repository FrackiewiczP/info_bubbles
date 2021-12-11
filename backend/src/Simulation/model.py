"""
Module with models implementations

List of models:

1. Triple filter model


"""

from time import time
import tracemalloc
import numpy as np
import pandas as pd
from mesa import Model
from Simulation.website import Website
from Simulation.user_agent import UserAgent
from DatabaseConnection.database_connector import DatabaseConnector


class TripleFilterModel(Model):
    """
    Triple filter modelling of echo chambers and filter bubbles in social networks

    """

    def __init__(
        self,
        number_of_agents,
        number_of_links=10,
        mem_capacity=10,
        friend_lose_prob=0.01,
        communication_form="individual",
        inter_user_communication_form="to_one_random",
        acc_latitude=0.5,
        acc_sharpness=20,

        initial_connections="random",
        sd_of_user_latitudes=0.2,
    ):

        self.number_of_agents = number_of_agents
        self.acc_latitude = acc_latitude
        self.acc_sharpness = acc_sharpness
        self.mem_capacity = mem_capacity
        self.number_of_links = number_of_links
        self.friend_lose_prob = friend_lose_prob
        users = {}
        user_positions = {}

        user_latitudes = np.random.normal(
            self.acc_latitude, sd_of_user_latitudes, size=self.number_of_agents
        )

        for i in range(self.number_of_agents):
            a = UserAgent(
                i,
                self,
                self.mem_capacity,
                user_latitudes[i],
                self.acc_sharpness,
            )
            users[i] = a

            user_positions[i] = a.user_position

        self.website = Website(
            users,
            number_of_links,
            friend_lose_prob,
            initial_connections,
            communication_form,
            inter_user_communication_form,
            user_positions,
        )

    def step(self):
        # website.step returns a dict, where
        # key - userId
        # value - 1x2 numpy array with user's position
        return self.website.step()
