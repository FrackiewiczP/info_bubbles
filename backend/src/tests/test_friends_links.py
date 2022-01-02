from Simulation.friend_links import FriendLinks


def test_creating_initial_connections_random__non_directed():
    no_of_links = 4
    no_of_users = 100
    no_of_groups = 4
    percent = 80

    links, users_friends, groups = FriendLinks.create_random_non_directed_friends_links(
        list(range(no_of_users)), no_of_links, percent, no_of_groups
    )

    # is number of links ok
    assert len(links) > (no_of_links * no_of_users / 2) - (len(links) * 0.1)
    assert len(links) < (no_of_links * no_of_users / 2) + (len(links) * 0.1)
    # is grups assign
    assert len(groups) == no_of_groups
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
