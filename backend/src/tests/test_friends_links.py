from Simulation.friend_links import FriendLinks


def test_creating_initial_connections_random__non_directed():
    no_of_links = 8
    no_of_users = 200
    no_of_groups = 4
    percent = 80

    links, users_friends = FriendLinks.create_random_non_directed_friends_links(
        list(range(200)), no_of_links, percent, no_of_groups
    )

    # is number of links ok
    assert len(links) == no_of_links * no_of_users
    for it in users_friends:
        for it2 in users_friends[it]:
            # there is no links to myself
            assert it2 != it
            # the links are non directed
            non_direct = False
            for it3 in users_friends[it2]:
                if it3 == it:
                    non_direct = True
            assert non_direct
