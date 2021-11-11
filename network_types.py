"""
Module with network types implementations



"""
import numpy as np
import random
import tracemalloc


class RandomNetwork:
    def __init__(self, unfriend_chance, users, no_of_links):
        self.unfriend_chance = unfriend_chance
        self.links = list()
        self.users = users
        self.create_initial_friend_links(users, no_of_links)

    def create_initial_friend_links(self, users, no_of_links):
        no_of_users = len(users)

        tracemalloc.start()
        vertices = list(range(no_of_users))
        ranks = dict.fromkeys(vertices, 0)
        while len(vertices) > 1:
            new_link = np.random.choice(vertices, size=2, replace=False)
            users[new_link[0]].user_friends.append(new_link[1])
            users[new_link[1]].user_friends.append(new_link[0])
            self.links.append((new_link[0], new_link[1]))
            ranks[new_link[0]] += 1
            ranks[new_link[1]] += 1
            if ranks[new_link[0]] == no_of_links:
                vertices.remove(new_link[0])
            if ranks[new_link[1]] == no_of_links:
                vertices.remove(new_link[1])

        current, peak = tracemalloc.get_traced_memory()
        print(f"Peak memory usage was {peak / 10 ** 6} MB")
        tracemalloc.stop()

    def unfriending(self):
        n = len(self.links)
        probs = np.random.rand(n)
        links_to_remove = list()
        for i in range(n):
            if probs[i] <= self.unfriend_chance:
                links_to_remove.append((self.links[i][0], self.links[i][1]))
                self.try_to_integrate_user(self.links[i][0], self.links[i][1])
        for link in links_to_remove:
            self.links.remove(link)

    def try_to_integrate_user(self, user1_id, user2_id):
        """
        Check if
        """
        user1_pos = self.users[user1_id].user_position
        user2_pos = self.users[user2_id].user_position
        dist = np.linalg.norm( user1_pos - user2_pos)
        latitude = self.users[user1_id].user_latitude
        sharpness = self.users[user1_id].user_sharpness
        probability = latitude ** sharpness / (
            dist ** sharpness + latitude ** sharpness
        )
        if np.random.rand() <= probability:
            # unfriend two people
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
            # print("size of user friends", str(len(self.users[user1_id].user_friends)))
            # print("size of possibilites", str(len(possible_new_friends)))
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
