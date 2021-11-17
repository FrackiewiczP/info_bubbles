import random

import information


class InterUserCommunication:
    def __init__(self, users: dict):
        self.users = users

    def send_info_to_friends(self, friends: dict, info: information):
        pass


class ToAllCommunication(InterUserCommunication):
    def __init__(self, users: dict):
        super(ToAllCommunication, self).__init__(users)

    def send_info_to_friends(self, friends: list, info: information):
        for friend in friends:
            self.users[friend].try_to_integrate_info_bit(info)


class ToOneRandomCommunication(InterUserCommunication):
    def __init__(self, users: dict):
        super(ToOneRandomCommunication, self).__init__(users)

    def send_info_to_friends(self, friends: list, info: information):
        friend = random.choice(friends)
        self.users[friend].try_to_integrate_info_bit(info)
