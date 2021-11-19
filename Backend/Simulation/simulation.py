
import time
import tracemalloc

from Simulation.model import TripleFilterModel


class Simulation:
    def __init__(self, number_of_agents, number_of_steps, info_latitude, info_sharpness):
        self.number_of_agents = number_of_agents
        self.number_of_steps = number_of_steps
        self.info_latitude = info_latitude,
        self.info_sharpness = info_sharpness,
        self.model = TripleFilterModel(
            num_of_users=self.number_of_agents,
            communication_form="individual",
            latitude_of_acceptance=self.info_latitude,
            sharpness_parameter=self.info_sharpness,
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