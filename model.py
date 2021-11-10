"""
Module with models implementations

List of models:

1. Triple filter model


"""

from mesa import Model
from mesa.datacollection import DataCollector
from communication_types import IndividualCommunication
from network_types import RandomNetwork
from user_agent import UserAgent
from mesa.time import RandomActivation
import numpy as np
import pandas as pd
import pickle
import time
import tracemalloc


class TripleFilterModel(Model):
    """
    Triple filter modelling of echo chambers and filter bubbles in social networks

    """

    def __init__(
        self,
        number_of_users,
        form_of_communication="individual",
        latitude_of_acceptance=0.5,
        sharpness_parameter=20,
        memory_size=10,
        number_of_links=10,
        link_delete_prob=0.01,
    ):

        self.num_of_users = number_of_users
        self.latitude_of_acceptance = latitude_of_acceptance
        self.sharpness_parameter = sharpness_parameter
        self.memory_size = memory_size
        self.number_of_links = number_of_links
        self.link_delete_prob = link_delete_prob
        self.iterations = 0
        self.users = {}
        self.user_positions = {}
        self.users_moved = set()

        self.user_positions_in_prev = {}

        self.schedule = RandomActivation(self)

        self.datacollector = DataCollector(
            model_reporters={"positions": "user_positions"},
            agent_reporters={"user_pos": "user_position"},
        )

        if form_of_communication == "individual":
            self.communication_form = IndividualCommunication(self)
        # standard deviation temporary hard coded
        user_latitudes = np.random.normal(
            self.latitude_of_acceptance, 0.2, size=self.num_of_users
        )

        for i in range(self.num_of_users):
            initial_position = np.random.rand(1, 2) * 2 - 1

            a = UserAgent(
                i,
                self,
                self.communication_form,
                initial_position,
                self.memory_size,
                user_latitudes[i],
                self.sharpness_parameter,
            )
            self.users[i] = a
            self.schedule.add(a)
            self.user_positions[i] = np.reshape(initial_position, 2)

        self.user_positions_in_prev[0] = dict(self.user_positions)
        start_time = time.time()
        self.network = RandomNetwork(
            self.link_delete_prob, self.users, self.number_of_links
        )

        print("--- %s seconds ---" % (time.time() - start_time))

    def register_user_movement(self, user_id):
        self.users_moved.add(user_id)

    def forward_info_bit(self, user_id, info_bit):
        self.users[user_id].try_to_integrate_info_bit(info_bit)

    def step(self):
        self.iterations += 1
        start_time = time.time()
        for i in range(self.num_of_users):
            self.users[i].communicate()
        print("communicating time  --- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        user_order = list(range(self.num_of_users))
        np.random.shuffle(user_order)
        for i in user_order:
            self.users[i].send_info_to_friends()
        print("sending time  --- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        for moved_user_id in self.users_moved:
            user = self.users[moved_user_id]
            current_position = user.update_position()
            self.user_positions[user.unique_id] = current_position

        self.user_positions_in_prev[self.iterations] = dict(self.user_positions)
        print("recalculating time--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        self.network.unfriending()
        print("unfriending time --- %s seconds ---" % (time.time() - start_time))
        self.users_moved.clear()
        # self.datacollector.collect(self)

    # self.schedule.step()

    def save_output(self):

        df = pd.DataFrame.from_dict(self.user_positions_in_prev, orient="index")
        df = df.melt(value_vars=df.columns, value_name="position", var_name="agent_id")
        df["x_pos"] = df.position.apply(lambda x: x[0])
        df["y_pos"] = df.position.apply(lambda x: x[1])
        df = df.drop(["position"], axis=1)
        df["step"] = list(range(self.iterations + 1)) * self.num_of_users
        df.to_csv("positions.csv")
