
import time
import tracemalloc

from Simulation.model import TripleFilterModel


class Simulation:
    def __init__(
            self,
            number_of_agents,
            number_of_steps,
            number_of_links,
            mem_capacity,
            friend_lose_prob,
            communication_form,
            inter_user_communication_form,
            acc_latitude,
            acc_sharpness,
            ):
        self.number_of_agents = number_of_agents
        self.number_of_steps = number_of_steps
        self.number_of_links = number_of_links
        self.mem_capacity = mem_capacity
        self.friend_lose_prob = friend_lose_prob
        self.communication_form = communication_form
        self.inter_user_communication_form = inter_user_communication_form
        self.acc_latitude = acc_latitude
        self.acc_sharpness = acc_sharpness

        self.model = TripleFilterModel(
            num_of_users=self.number_of_agents,
            number_of_links=self.number_of_links,
            memory_size=self.mem_capacity,
            link_delete_prob=self.friend_lose_prob,
            inter_user_communication_form=self.inter_user_communication_form,
            communication_form=self.communication_form,
            latitude_of_acceptance=self.acc_latitude,
            sharpness_parameter=self.acc_sharpness,
            sd_of_user_latitudes=0 # for now, let's keep the model simple, so it's easier to grasp and debug
            )
    
    def run_simulation(self):
        start_time = time.time()

        tracemalloc.start()
        for i in range(self.number_of_steps):
            print("--------------------" + str(i) + "----------------")
            self.model.step()
        print("total  --- %s seconds ---" % (time.time() - start_time))
        current, peak = tracemalloc.get_traced_memory()
        print(f"Peak memory usage was {peak / 10 ** 6} MB")
        tracemalloc.stop()
        self.model.save_output()
        return self.model.get_output()