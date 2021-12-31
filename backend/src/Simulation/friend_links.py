from enum import Enum
import tracemalloc
import numpy as np
import random


class FriendsLinksTypes(Enum):
    RANDOM_NON_DIRECTED = 1


class FriendLinks:
    def __init__(
            self, links_type: FriendsLinksTypes, vertices: list, no_of_links: int,procent_of_the_same_group:int,no_of_grups:int
    ) -> None:
        if links_type == FriendsLinksTypes.RANDOM_NON_DIRECTED:
            (
                self.__links,
                self.__users_friends,
            ) = self.create_random_non_directed_friends_links(vertices, no_of_links,procent_of_the_same_group,no_of_grups)

    @property
    def links(self):
        return self.__links

    def __getitem__(self, user_id):
        return self.__users_friends[user_id]

    def delete_link(self, link: tuple[int]):
        """
        Deletes link between user1 and user2 and creates a new link between user1
        and random friend of his friends
        """
        user1_id = link[0]
        user2_id = link[1]
        # unfriending
        self.__links.remove(link)
        self.__users_friends[user1_id].remove(user2_id)
        self.__users_friends[user2_id].remove(user1_id)
        # creating new friendship
        possible_new_friends = set()
        for friend in self.__users_friends[user1_id]:
            possible_new_friends = possible_new_friends.union(
                set(self.__users_friends[friend])
            )
        if user2_id in possible_new_friends:
            possible_new_friends.remove(user2_id)
        if user1_id in possible_new_friends:
            possible_new_friends.remove(user1_id)
        if len(possible_new_friends) == 0:
            possible_new_friends = list(self.__users_friends.keys())
            possible_new_friends.remove(user1_id)
            possible_new_friends.remove(user2_id)
            new_friend = random.choice(possible_new_friends)
        else:
            new_friend = random.choice(tuple(possible_new_friends))
        self.__users_friends[user1_id].append(new_friend)
        self.__users_friends[new_friend].append(user1_id)
        self.__links.append((new_friend, user1_id))

    @staticmethod
    def create_random_non_directed_friends_links(vertices: list, no_of_links: int,procent_of_the_same_group:int,no_of_grups:int):
        no_of_links = no_of_links / 2
        in_each_group = (len(vertices) / no_of_grups)
        in_same_group = ((no_of_links * procent_of_the_same_group) / 100)
        # TODO błąd przy niemożliwości spełnienia warunków
        graph = np.zeros((len(vertices), len(vertices)))
        for gr in range(no_of_grups):
            start = int(gr * in_each_group)  # włącznie
            stop = int((gr + 1) * in_each_group)  # wyłacznie
            if gr == no_of_grups:
                stop = len(vertices)
            # in the same group
            for po in range(int(in_same_group * (stop - start))):
                a = 0
                b = 0
                while a == b or graph[a, b] == 1:
                    a = random.randrange(start, stop)
                    b = random.randrange(start, stop)
                graph[a, b] = 1
                graph[b, a] = 1
            # in different groups
            choice = list()
            if gr != 0:
                choice.extend(range(0, start))
            if gr != no_of_grups:
                choice.extend(range(stop, len(vertices)))
            for po in range(int((no_of_links - in_same_group) * (stop - start))):
                lin = [0, 0]
                while lin[1] == lin[0] or graph[lin[0], lin[1]] == 1:
                    lin = random.sample(choice, k=2)
                graph[lin[0], lin[1]] = 1
                graph[lin[1], lin[0]] = 1
        # tu zmenić na to co zwracamy
        links = list()
        users_friends = dict.fromkeys(vertices)
        for i in users_friends:
            users_friends[i] = list()
        for x in range(len(vertices)):
            for y in range(len(vertices)):
                if (graph[x, y] == 1):
                    users_friends[vertices[x]].append(vertices[y])
        for x in range(len(vertices)):
            for y in range(x, len(vertices)):
                if(graph[x,y]==1):
                    links.append((vertices[x], vertices[y]))
        return links, users_friends
