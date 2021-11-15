import random

import information


class InterUserCommunication:
    def __init__(self,users:{}):
        self.users = users
    def send_info_to_friends(self,frends:[],info:information):
        pass

class ToAllCommunication(InterUserCommunication):
    def __init__(self, users: {}):
        super(ToAllCommunication, self).__init__(users)
    def send_info_to_friends(self,frends:[],info:information):
        for friend in frends:
            self.users[friend].try_to_integrate_info_bit(info)

class ToOneRandomCommunication(InterUserCommunication):
    def __init__(self, users: {}):
        super(ToOneRandomCommunication, self).__init__(users)
    def send_info_to_friends(self,frends:[],info:information):
        friend = random.choice(frends)
        self.users[friend].try_to_integrate_info_bit(info)