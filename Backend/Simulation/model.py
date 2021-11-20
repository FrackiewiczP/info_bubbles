"""
Module with models implementations

List of models:

1. Triple filter model


"""

import numpy as np
import pandas as pd
from mesa import Model
from Simulation.website import Website
from Simulation.user_agent import UserAgent


class TripleFilterModel(Model):
    """
    Triple filter modelling of echo chambers and filter bubbles in social networks

    """

    def create_from_file(file_name):
        start_data = {}
        with open('workfile') as f:
            start_data = json.load(f)

        return model(start_data.num_of_users,
                     start_data.communication_form,
                     start_data.list_of_infos_in_symulation,
                     start_data.latitude_of_acceptance,
                     start_data.sharpness_parameter,
                     start_data.memory_size,
                     start_data.number_of_links,
                     start_data.link_delete_prob,
                     start_data.inter_user_communication_form,
                     start_data.initial_connections,
                     start_data.sd_of_user_latitudes
                     )

    def __init__(
        self,
        num_of_users,
        communication_form="individual",
        list_of_infos_in_symulation = None,
        latitude_of_acceptance=0.5,
        sharpness_parameter=20,
        memory_size=10,
        number_of_links=10,
        link_delete_prob=0.01,
        inter_user_communication_form="to_one_random",
        initial_connections="random",
        sd_of_user_latitudes=0.2
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
            initial_position = np.random.rand(2) * 2 - 1

            a = UserAgent(
                i,
                self,
                initial_position,
                self.memory_size,
                user_latitudes[i],
                self.sharpness_parameter,
            )
            users[i] = a

            user_positions[i] = initial_position

        self.website = Website(
            users,
            number_of_links,
            link_delete_prob,
            initial_connections,
            communication_form,
            inter_user_communication_form,
            user_positions,
            list_of_infos_in_symulation
        )

        self.user_positions_in_prev[0] = dict(user_positions)

    def step(self):
        self.iterations += 1
        self.user_positions_in_prev[self.iterations] = self.website.step()

    def save_output(self):
        df = pd.DataFrame.from_dict(self.user_positions_in_prev, orient="index")
        df = df.melt(value_vars=df.columns, value_name="position", var_name="agent_id")
        df["x_pos"] = df.position.apply(lambda x: x[0])
        df["y_pos"] = df.position.apply(lambda x: x[1])
        df = df.drop(["position"], axis=1)
        df["step"] = list(range(self.iterations + 1)) * self.num_of_users
        df.to_csv("positions.csv")
    
    def get_output(self):
        ret = {}
        for step in self.user_positions_in_prev:
            ret[step] = {key: value.tolist() for key, value in self.user_positions_in_prev[step].items()}
        return ret

