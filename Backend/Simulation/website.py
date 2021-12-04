"""
Module with website class

Class representing



"""

from enum import Enum
import random
import tracemalloc
from enum import Enum
from numpy.core import numeric
from integration_function import check_integration
import communication_types
import numpy as np
from collections import defaultdict
import time

class InitialFriendsLinksTypes(Enum):
    RANDOM_NON_DIRECTED =1

class InitialFriendLinks:
    @staticmethod
    def create_random_non_directed_friends_links(no_of_users: int, no_of_links: int):
        tracemalloc.start()
        vertices = list(range(no_of_users))
        ranks = dict.fromkeys(vertices, 0)
        users_friends =  dict.fromkeys(vertices)
        for i in users_friends:
            users_friends[i] = list()
        links = list()
        while len(vertices) > 1:
            new_link = np.random.choice(vertices, size=2, replace=False)
            users_friends[new_link[0]].append(new_link[1])
            users_friends[new_link[1]].append(new_link[0])
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
        return links, users_friends

class InterUserCommunicationTypes(Enum):
    TO_ONE_RANDOM = 1
    TO_ALL = 2

class InterUserCommunication:
    @staticmethod
    def send_info_to_random_friend(users: dict, user_id: int, user_friends: list):
        info = users[user_id].get_random_information()
        users_to_move = set()
        try:
            friend = random.choice(user_friends)
        except IndexError:
            # user_friends is empty
            return users_to_move
        if users[friend].try_to_integrate_info_bit(info):
            users_to_move.add(friend)
        return users_to_move

    @staticmethod
    def send_info_to_all_friends(users: dict, user_id: int, user_friends: list):
        info = users[user_id].get_random_information()
        users_to_move = set()
        for friend in user_friends:
            if users[friend].try_to_integrate_info_bit(info):
                users_to_move.add(friend)
        return users_to_move


class Website:
    def __init__(
        self,
        users: dict,
        no_of_links: int,
        unfriend_chance: numeric,
        initial_connections: str,
        communication_mode: str,
        users_communication_mode: str,
        user_positions: dict,
    ):
        self.unfriend_chance = unfriend_chance
        self.links = list()
        self.users = users

        self.user_positions = user_positions

        match initial_connections:
            case InitialFriendsLinksTypes.RANDOM_NON_DIRECTED :
                self.links, self.users_friends = InitialFriendLinks.create_random_non_directed_friends_links(len(users), no_of_links)
        match communication_mode:
            case communication_types.CommunicationTypes.CENTRAL :
                 self.communication_form = communication_types.IndividualCommunication(users)
            case communication_types.CommunicationTypes.INDIVIDUAL :
                 self.communication_form = communication_types.CentralCommunication(users)
        match users_communication_mode:
            case InterUserCommunicationTypes.TO_ONE_RANDOM :
                 self.users_communication = InterUserCommunication.send_info_to_random_friend
            case InterUserCommunicationTypes.TO_ALL :
                 self.users_communication = InterUserCommunication.send_info_to_all_friends

    def step(self):
        start_time = time.time()
        users_to_moved = self.communication_form.integrate_new_info()
        print("communicating time  --- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        users_order = list(self.users.keys())
        np.random.shuffle(users_order)
        for i in users_order:
            users_to_moved = users_to_moved.union(
                self.users_communication(self.users, i, self.users_friends[i])
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
                if self.try_to_unfriend_users(link[0], link[1]):
                    self.links.remove(link)

    def try_to_unfriend_users(self, user1_id: int, user2_id: int):
        """
        Check if one user wants to unfriend other
        """
        user1_pos = self.users[user1_id].user_position
        user2_pos = self.users[user2_id].user_position
        latitude = self.users[user1_id].user_latitude
        sharpness = self.users[user1_id].user_sharpness
        if check_integration(user1_pos, user2_pos, latitude, sharpness):
            self.unfriend_users(user1_id, user2_id)
            return True
        return False

    def unfriend_users(self, user1_id: int, user2_id: int):
        """
        Perform unfriending and create new friendship
        """
        # unfriending
        self.users_friends[user1_id].remove(user2_id)
        self.users_friends[user2_id].remove(user1_id)
        # creating new friendship
        possible_new_friends = set()
        for friend in self.users_friends[user1_id]:
            possible_new_friends = possible_new_friends.union(
                set(self.users_friends[friend])
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
        self.users_friends[user1_id].append(new_friend)
        self.users_friends[new_friend].append(user1_id)
        self.links.append((new_friend, user1_id))
