"""
Module with website class

Class representing website - environment where users learn new information



"""

from enum import Enum
import random
import numpy as np
import time
from Simulation.integration_function import check_integration
import Simulation.communication_types as communication_types
import numpy as np
from Simulation.friend_links import FriendLinks, FriendsLinksTypes
import time


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
        unfriend_chance: float,
        initial_connections: str,
        communication_mode: str,
        users_communication_mode: str,
        user_positions: dict,
        percent_of_the_same_group: int,
        no_of_groups: int
    ):
        self.unfriend_chance = unfriend_chance
        self.users = users

        self.user_positions = user_positions

        match initial_connections:
            case FriendsLinksTypes.RANDOM_NON_DIRECTED :
                self.friend_links = FriendLinks(FriendsLinksTypes.RANDOM_NON_DIRECTED, list(self.users.keys()), no_of_links, percent_of_the_same_group,no_of_groups)
        match communication_mode:
            case communication_types.CommunicationType.CENTRAL :
                 self.communication_form = communication_types.CentralCommunication(users)
            case communication_types.CommunicationType.INDIVIDUAL :
                 self.communication_form = communication_types.IndividualCommunication(users)
            case communication_types.CommunicationType.FILTER_DISTANT:
                self.communication_form = communication_types.FilterDistantCommunication(users)
            case communication_types.CommunicationType.FILTER_CLOSE:
                self.communication_form = communication_types.FilterCloseCommunication(users)
        match users_communication_mode:
            case InterUserCommunicationTypes.TO_ONE_RANDOM :
                 self.users_communication = InterUserCommunication.send_info_to_random_friend
            case InterUserCommunicationTypes.TO_ALL :
                 self.users_communication = InterUserCommunication.send_info_to_all_friends

    def step(self):
        start_time = time.time()
        users_to_move = self.communication_form.integrate_new_info()
        print("communicating time  --- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        users_order = list(self.users.keys())
        np.random.shuffle(users_order)
        for i in users_order:
            users_to_move = users_to_move.union(
                self.users_communication(self.users, i, self.friend_links[i])
            )
        print("sending time  --- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        for moved_user_id in users_to_move:
            user = self.users[moved_user_id]
            current_position = user.update_position()
            self.user_positions[user.unique_id] = current_position
        print("recalculating time--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        self.find_links_to_remove()
        print("unfriending time --- %s seconds ---" % (time.time() - start_time))
        return dict(self.user_positions)

    def find_links_to_remove(self):
        for link in self.friend_links.links:
            if np.random.rand(1) <= self.unfriend_chance:
                if self.try_to_unfriend_users(link[0], link[1]):
                    self.friend_links.delete_link(link)

    def try_to_unfriend_users(self, user1_id: int, user2_id: int):
        """
        Check if one user wants to unfriend other
        """
        user1_pos = self.users[user1_id].position
        user2_pos = self.users[user2_id].position
        latitude = self.users[user1_id].latitude
        sharpness = self.users[user1_id].sharpness
        if check_integration(user1_pos, user2_pos, latitude, sharpness):
            return False
        return True

    
