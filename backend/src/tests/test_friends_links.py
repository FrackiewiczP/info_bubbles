from Simulation.friend_links import FriendLinks


def test_creating_initial_connections_random__non_directed():
    no_of_links = 8
    no_of_users = 200
    links, users_friends = FriendLinks.create_random_non_directed_friends_links(
        list(range(200)), no_of_links
    )
    # It is possible for certain no_of_links and no_of_users
    # that one user will have (no_of_links - 1) friends
    assert abs(len(links) - (no_of_users * no_of_links) / 2) <= 1
    for user in users_friends:
        assert len(users_friends[user]) == no_of_links
