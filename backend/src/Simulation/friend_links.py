from enum import Enum
import tracemalloc
import numpy as np
import random


class FriendsLinksTypes(Enum):
    RANDOM_NON_DIRECTED = 1
    RANDOM_DIRECTED = 2


class FriendLinks:
    def __init__(
        self,
        links_type: FriendsLinksTypes,
        vertices: list,
        no_of_links: int,
        percent_of_the_same_group: int,
        no_of_groups: int,
    ) -> None:
        self.type = links_type
        if links_type == FriendsLinksTypes.RANDOM_DIRECTED:
            (
                self.__links,
                self.__users_friends,
                self.__user_groups,
            ) = self.create_random_directed_friends_links(
                vertices, no_of_links, percent_of_the_same_group, no_of_groups
            )
        if links_type == FriendsLinksTypes.RANDOM_NON_DIRECTED:
            (
                self.__links,
                self.__users_friends,
                self.__user_groups,
            ) = self.create_random_non_directed_friends_links(
                vertices, no_of_links, percent_of_the_same_group, no_of_groups
            )

    @property
    def links(self):
        return self.__links

    @property
    def groups(self):
        return self.__user_groups

    def __getitem__(self, user_id):
        return self.__users_friends[user_id]

    def delete(self, link: tuple[int]):
        if self.type == FriendsLinksTypes.RANDOM_DIRECTED:
            self.delete_directed_link(link)
        if self.type == FriendsLinksTypes.RANDOM_NON_DIRECTED:
            self.delete_link(link)

    def delete_directed_link(self, link: tuple[int]):
        """
        Deletes link between user1 and user2 and creates a new link between user1
        and random friend of his friends
        """
        user1_id = link[0]
        user2_id = link[1]
        # unfriending
        self.__links.remove(link)
        self.__users_friends[user1_id].remove(user2_id)
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
        for friend in self.__users_friends[user1_id]:
            if friend in possible_new_friends:
                possible_new_friends.remove(friend)
        if len(possible_new_friends) == 0:
            possible_new_friends = list(self.__users_friends.keys())
            possible_new_friends.remove(user1_id)
            possible_new_friends.remove(user2_id)
            new_friend = random.choice(possible_new_friends)
        else:
            new_friend = random.choice(tuple(possible_new_friends))
        self.__users_friends[user1_id].append(new_friend)
        self.__links.append((user1_id, new_friend))

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
        # 50% chance that user2 will have new friend
        if np.random.rand(1) <= 0.5:
            tmp = user1_id
            user1_id = user2_id
            user2_id = tmp
        possible_new_friends = set()
        for friend in self.__users_friends[user1_id]:
            possible_new_friends = possible_new_friends.union(
                set(self.__users_friends[friend])
            )
        if user2_id in possible_new_friends:
            possible_new_friends.remove(user2_id)
        if user1_id in possible_new_friends:
            possible_new_friends.remove(user1_id)
        for friend in self.__users_friends[user1_id]:
            if friend in possible_new_friends:
                possible_new_friends.remove(friend)
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
    def create_random_non_directed_friends_links(
        vertices: list,
        no_of_links: int,
        percent_of_the_same_group: int,
        no_of_groups: int,
    ):
        no_of_links = no_of_links / 2
        in_each_group = (len(vertices) / no_of_groups)
        in_same_group = ((no_of_links * percent_of_the_same_group) / 100)
        graph = dict()
        users_in_groups = dict()
        for x in range(len(vertices)):
            graph[x] = dict()
        for gr in range(no_of_groups):
            start = int(gr * in_each_group)  # inclusive
            stop = int((gr + 1) * in_each_group)  # exclusive
            users_in_groups[gr] = list(vertices[start:stop])
            if gr == no_of_groups:
                stop = len(vertices)
            # in the same group
            for po in range(int(in_same_group * (stop - start))):
                a = 0
                b = 0
                while a == b:
                    a = random.randrange(start, stop)
                    b = random.randrange(start, stop)
                    try:
                        if graph[a][b] == 1:
                            a = b
                    except KeyError:
                        pass
                graph[a][b] = 1
                graph[b][a] = 1
            # in different groups
            choice = list()
            if gr != 0:
                choice.extend(range(0, start))
            if gr != no_of_groups:
                choice.extend(range(stop, len(vertices)))
            for po in range(int((no_of_links - in_same_group) * (stop - start))):
                lin = [0, 0]
                while lin[1] == lin[0]:
                    lin = random.sample(choice, k=2)
                    try:
                        if graph[lin[0]][lin[1]] == 1:
                            lin[1] = lin[0]
                    except KeyError:
                        pass
                graph[lin[0]][lin[1]] = 1
                graph[lin[1]][lin[0]] = 1

        # translating to user keys
        links = list()
        users_friends = dict.fromkeys(vertices)
        for i in users_friends:
            users_friends[i] = list()
        for k, v in graph.items():
            for x in v.keys():
                users_friends[vertices[k]].append(vertices[x])
                if x < k:
                    links.append((vertices[x], vertices[k]))
        return links, users_friends, users_in_groups

    @staticmethod
    def create_random_directed_friends_links(
        vertices: list,
        no_of_links: int,
        percent_of_the_same_group: int,
        no_of_groups: int,
    ):
        no_of_links = no_of_links
        in_each_group = (len(vertices) / no_of_groups)
        in_same_group = ((no_of_links * percent_of_the_same_group) / 100)
        graph = dict()
        users_in_groups = dict()
        for x in range(len(vertices)):
            graph[x] = dict()
        for gr in range(no_of_groups):
            start = int(gr * in_each_group)  # inclusive
            stop = int((gr + 1) * in_each_group)  # exclusive
            users_in_groups[gr] = list(vertices[start:stop])
            if gr == no_of_groups:
                stop = len(vertices)
            # in the same group
            for po in range(int(in_same_group * (stop - start))):
                a = 0
                b = 0
                while a == b:
                    a = random.randrange(start, stop)
                    b = random.randrange(start, stop)
                    try:
                        if graph[a][b] == 1:
                            a = b
                    except KeyError:
                        pass
                graph[a][b] = 1
            # in different groups
            choice = list()
            if gr != 0:
                choice.extend(range(0, start))
            if gr != no_of_groups:
                choice.extend(range(stop, len(vertices)))
            for po in range(int((no_of_links - in_same_group) * (stop - start))):
                lin = [0, 0]
                while lin[1] == lin[0]:
                    lin = random.sample(choice, k=2)
                    try:
                        if graph[lin[0]][lin[1]] == 1:
                            lin[1] = lin[0]
                    except KeyError:
                        pass
                graph[lin[0]][lin[1]] = 1
        # translating to user keys
        links = list()
        users_friends = dict.fromkeys(vertices)
        for i in users_friends:
            users_friends[i] = list()
        for k, v in graph.items():
            for x in v.keys():
                users_friends[vertices[k]].append(vertices[x])
                links.append((vertices[k], vertices[x]))
        return links, users_friends, users_in_groups
