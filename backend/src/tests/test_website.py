from Simulation.user_agent import UserAgent
from Simulation.website import Website, InterUserCommunicationTypes
from Simulation.friend_links import FriendsLinksTypes
from Simulation.communication_types import CommunicationType
from Simulation.information import Information
import numpy as np


def test_calculating_user_statistics(mocker):
    num_of_users = 10
    users = {}
    user_positions = {}
    for i in range(num_of_users):
        a = UserAgent(
            unique_id=i,
            model=mocker.MagicMock(),
            memory_capacity=10,
            user_latitude=1,
            user_sharpness=20,
        )
        users[i] = a
        user_positions[i] = a.position

    website = Website(
        users=users,
        no_of_links=2,
        unfriend_chance=1,
        initial_connections=FriendsLinksTypes.RANDOM_NON_DIRECTED,
        communication_mode=CommunicationType.INDIVIDUAL,
        users_communication_mode=InterUserCommunicationTypes.TO_ONE_RANDOM,
        user_positions=user_positions,
        percent_of_the_same_group=0.8,
        no_of_groups=2,
    )
    prev_positions = dict(user_positions)
    mean_fluctuation = 0
    mean_dist_to_infos = 0
    for i, id in enumerate(users):
        users[id].memory.add_new_info_bit(Information())
        users[id].memory.add_new_info_bit(Information())
        user_positions[id] = users[id].update_position()
        mean_fluctuation += np.linalg.norm(prev_positions[id] - user_positions[id])
        mean_dist_to_infos += users[id].mean_info_dist
    mean_fluctuation /= i + 1
    mean_dist_to_infos /= i + 1
    (
        mean_fluctuation_website,
        mean_info_dist_website,
        _,
    ) = website.calculate_users_statistics(prev_positions)
    assert round(mean_fluctuation, 7) == round(mean_fluctuation_website, 7)
    assert round(mean_dist_to_infos, 7) == round(mean_info_dist_website, 7)
