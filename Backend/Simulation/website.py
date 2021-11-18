"""
Module with website class

Class representing



"""

import random
import tracemalloc


from numpy.core import numeric
from integration_function import check_integration
import communication_types
import numpy as np

import time


def create_random_friend_links(users: dict, no_of_links: int):
    no_of_users = len(users)
    tracemalloc.start()
    vertices = list(range(no_of_users))
    ranks = dict.fromkeys(vertices, 0)
    links = list()
    while len(vertices) > 1:
        new_link = np.random.choice(vertices, size=2, replace=False)
        users[new_link[0]].user_friends.append(new_link[1])
        users[new_link[1]].user_friends.append(new_link[0])
        links.append((new_link[0], new_link[1]))
        ranks[new_link[0]] += 1
        ranks[new_link[1]] += 1
        if ranks[new_link[0]] == no_of_links:
            vertices.remove(new_link[0])
        if ranks[new_link[1]] == no_of_links:
            vertices.remove(new_link[1])

    current, peak = tracemalloc.get_traced_memory()
    print(f"Peak memory usage was {peak / 10 ** 6} MB")
    tracemalloc.stop()
    return links


def send_info_to_random_friend(users: dict, user_id: int):
    friends = users[user_id].user_friends
    info = users[user_id].get_random_information()
    friend = random.choice(friends)
    users_to_move = set()
    if users[friend].try_to_integrate_info_bit(info):
        users_to_move.add(friend)
    return users_to_move


def send_info_to_all_friends(users: dict, user_id: int):
    friends = users[user_id].user_friends
    info = users[user_id].get_random_information()
    users_to_move = set()
    for friend in friends:
        if users[friend].try_to_integrate_info_bit(info):
            users_to_move.add(friend)
    return users_to_move


class Website:
    def __init__(
        self,
        users: dict,
        no_of_links: int,
        unfriend_chance: numeric,
        initial_connections: int,
        communication_mode: str,
        users_communication_mode: str,
        user_positions: dict,
    ):
        self.unfriend_chance = unfriend_chance
        self.links = list()
        self.users = users
        self.user_positions = user_positions

        match initial_connections:
            case "random" : self.links = create_random_friend_links(users, no_of_links)

        match communication_mode:
            case "individual" : self.communication_form = communication_types.IndividualCommunication(users)
            case "central" : self.communication_form = communication_types.CentralCommunication(users)

        match users_communication_mode:
            case "toOneRandom" : self.users_communication = send_info_to_random_friend
            case "ToAll" : self.users_communication = send_info_to_all_friends

    def step(self):

        start_time = time.time()

        users_to_moved = self.communication_form.integrate_new_info()

        print("communicating time  --- %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        users_order = list(self.users.keys())
        np.random.shuffle(users_order)
        for i in users_order:
            users_to_moved = users_to_moved.union(
                self.users_communication(self.users, i)
            )

        print("sending time  --- %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        for moved_user_id in users_to_moved:
            user = self.users[moved_user_id]
            current_position = user.update_position()
            self.user_positions[user.unique_id] = current_position

        print("recalculating time--- %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        self.find_links_to_remove()
        print("unfriending time --- %s seconds ---" % (time.time() - start_time))

        return self.user_positions

    def find_links_to_remove(self):
        for link in self.links:
            if np.random.rand(1) <= self.unfriend_chance:
                self.try_to_integrate_user(link[0], link[1])
                self.links.remove(link)

    def try_to_integrate_user(self, user1_id: int, user2_id: int):
        """
        Check if one user wants to unfriend other
        """
        user1_pos = self.users[user1_id].user_position
        user2_pos = self.users[user2_id].user_position
        latitude = self.users[user1_id].user_latitude
        sharpness = self.users[user1_id].user_sharpness
        if check_integration(user1_pos, user2_pos, latitude, sharpness):
            self.unfriend_users(user1_id, user2_id)

    def unfriend_users(self, user1_id: int, user2_id: int):
        """
        Perform unfriending and create new friendship
        """
        # unfriending
        self.users[user1_id].user_friends.remove(user2_id)
        self.users[user2_id].user_friends.remove(user1_id)
        # creating new friendship
        possible_new_friends = set()
        for friend in self.users[user1_id].user_friends:
            possible_new_friends = possible_new_friends.union(
                set(self.users[friend].user_friends)
            )
        if user2_id in possible_new_friends:
            possible_new_friends.remove(user2_id)
        if user1_id in possible_new_friends:
            possible_new_friends.remove(user1_id)
        if len(possible_new_friends) == 0:
            possible_new_friends = list(range(len(self.users)))
            possible_new_friends.remove(user1_id)
            possible_new_friends.remove(user2_id)
            new_friend = random.choice(possible_new_friends)
        else:
            new_friend = random.choice(tuple(possible_new_friends))
        self.users[user1_id].user_friends.append(new_friend)
        self.users[new_friend].user_friends.append(user1_id)
        self.links.append((new_friend, user1_id))
