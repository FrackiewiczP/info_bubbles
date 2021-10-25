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
import time
import tracemalloc

class TripleFilterModel(Model):
    """
   Triple filter modelling of echo chambers and filter bubbles in social networks

    """

    def __init__(self, number_of_users, form_of_communication="individual", latitude_of_acceptance=0.5,
                 sharpness_parameter=20, memory_size=10, number_of_links=10, link_delete_prob=0.01):

        self.num_of_users = number_of_users
        self.latitude_of_acceptance = latitude_of_acceptance
        self.sharpness_parameter = sharpness_parameter
        self.memory_size = memory_size
        self.number_of_links=number_of_links
        self.link_delete_prob=link_delete_prob
        self.iterations = 0
        self.users = {}
        self.user_positions = {}
        self.users_moved = set()

        self.schedule = RandomActivation(self)



        if form_of_communication == "individual":
            self.communication_form = IndividualCommunication(self)
        # standard deviation temporary hard coded
        user_latitudes = np.random.normal(self.latitude_of_acceptance, 0.2, size=self.num_of_users)

        for i in range(self.num_of_users):
            initial_position = np.random.rand(1, 2) * 2 - 1

            a = UserAgent(i, self, self.communication_form, initial_position, self.memory_size,
                          user_latitudes[i], self.sharpness_parameter)
            self.users[i] = a
            self.user_positions[i] = initial_position

        start_time = time.time()
        self.network=RandomNetwork(self.link_delete_prob,self.users,self.number_of_links)


        print("--- %s seconds ---" % (time.time() - start_time))
        friends_num=list()
        for u in range(self.num_of_users):
            #print(str(len(self.users[u].user_friends)))
            friends_num.append((len(self.users[u].user_friends)))
        print(np.mean(friends_num))

        self.datacollector = DataCollector(
            model_reporters={"Positions": "user_positions"})


    def step(self):
        self.iterations += 1
        start_time = time.time()
        for i in range(self.num_of_users):
            self.users[i].communicate()
        print("communciating time  --- %s seconds ---" % (time.time() - start_time))
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
        print("recalculating time--- %s seconds ---" % (time.time() - start_time))
        start_time=time.time()
        self.network.unfriending()
        print("unfriending time --- %s seconds ---" % (time.time() - start_time))
        self.users_moved.clear()
        self.datacollector.collect(self)


def get_agent_position(agent):
    return agent.user_position