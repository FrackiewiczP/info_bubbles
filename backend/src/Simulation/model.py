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
        number_of_steps,
        number_of_links=10,
        mem_capacity=10,
        friend_lose_prob=0.01,
        communication_form="individual",
        inter_user_communication_form="to_one_random",
        acc_latitude=0.5,
        acc_sharpness=20,

        initial_connections="random",
        sd_of_user_latitudes=0.2,
        db_connector: DatabaseConnector=None,
        socket_id=None,
    ):

        self.number_of_agents = number_of_agents
        self.number_of_steps = number_of_steps
        self.db_connector = db_connector
        self.socket_id=socket_id
        self.acc_latitude = acc_latitude
        self.acc_sharpness = acc_sharpness
        self.mem_capacity = mem_capacity
        self.number_of_links = number_of_links
        self.friend_lose_prob = friend_lose_prob
        self.iterations = 0
        self.user_positions_in_prev = {}
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

        self.user_positions_in_prev[0] = dict(user_positions)

    def step(self):
        self.iterations += 1

        # website.step returns a dict, where
        # key - userId
        # value - 1x2 numpy array with user's position
        current_step_data = self.website.step()

        # MongoDB only allows strings as document keys
        current_step_data_with_string_keys = {str(key): list(value) for (key,value) in current_step_data.items()}
        self.user_positions_in_prev[self.iterations] = current_step_data
        self.db_connector.save_simulation_step(self.socket_id,self.iterations, current_step_data_with_string_keys)

    def save_output(self):
        df = pd.DataFrame.from_dict(self.user_positions_in_prev, orient="index")
        df = df.melt(value_vars=df.columns, value_name="position", var_name="agent_id")
        df["x_pos"] = df.position.apply(lambda x: x[0])
        df["y_pos"] = df.position.apply(lambda x: x[1])
        df = df.drop(["position"], axis=1)
        df["step"] = list(range(self.iterations + 1)) * self.number_of_agents
        df.to_csv("positions.csv")
    
    def get_output(self):
        ret = {}
        for step in self.user_positions_in_prev:
            ret[step] = {key: value.tolist() for key, value in self.user_positions_in_prev[step].items()}
        return ret

    def run_simulation(self):
        start_time = time()
        self.db_connector.delete_previous_simulation_of_socket(self.socket_id)
        tracemalloc.start()
        for i in range(self.number_of_steps):
            print("--------------------" + str(i) + "----------------")
            self.step()
        print("total  --- %s seconds ---" % (time() - start_time))
        current, peak = tracemalloc.get_traced_memory()
        print(f"Peak memory usage was {peak / 10 ** 6} MB")
        tracemalloc.stop()
        # self.save_output()
        # return self.get_output()
