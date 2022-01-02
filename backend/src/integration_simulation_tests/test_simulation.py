from Simulation.model import TripleFilterModel
from Simulation.communication_types import CommunicationType
from Simulation.website import InterUserCommunicationTypes


def run_model(num_of_steps: int, model: TripleFilterModel):
    for i in range(num_of_steps):
        model.step()


num_of_users = 100
num_of_steps = 100
memory_size = 10
num_of_links = 10
inter_user_communication_form = InterUserCommunicationTypes.TO_ONE_RANDOM


def test_filter_distant_communication():
    model_filter_distant = TripleFilterModel(
        num_of_users=num_of_users,
        number_of_links=num_of_links,
        memory_size=memory_size,
        communication_form=CommunicationType.FILTER_DISTANT,
        inter_user_communication_form=inter_user_communication_form,
    )
    run_model(num_of_steps, model_filter_distant)


def test_filter_close_communication():
    model_filter_close = TripleFilterModel(
        num_of_users=num_of_users,
        number_of_links=num_of_links,
        memory_size=memory_size,
        communication_form=CommunicationType.FILTER_CLOSE,
        inter_user_communication_form=inter_user_communication_form,
    )
    run_model(num_of_steps, model_filter_close)
