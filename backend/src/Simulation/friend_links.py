from enum import Enum
import tracemalloc
import numpy as np
import random


class FriendsLinksTypes(Enum):
    RANDOM_NON_DIRECTED = 1


class FriendLinks:
    def __init__(
        self, links_type: FriendsLinksTypes, vertices: list, no_of_links: int
    ) -> None:
        if links_type == FriendsLinksTypes.RANDOM_NON_DIRECTED:
            (
                self.__links,
                self.__users_friends,
            ) = self.create_random_non_directed_friends_links(vertices, no_of_links)

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
            possible_new_friends = list(range(len(self.users)))
            possible_new_friends.remove(user1_id)
            possible_new_friends.remove(user2_id)
            new_friend = random.choice(possible_new_friends)
        else:
            new_friend = random.choice(tuple(possible_new_friends))
        self.__users_friends[user1_id].append(new_friend)
        self.__users_friends[new_friend].append(user1_id)
        self.__links.append((new_friend, user1_id))

    @staticmethod
    def create_random_non_directed_friends_links(vertices: list, no_of_links: int):
        tracemalloc.start()
        ranks = dict.fromkeys(vertices, 0)
        users_friends = dict.fromkeys(vertices)
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
