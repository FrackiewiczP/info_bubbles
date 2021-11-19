
import time
import tracemalloc

from Simulation.model import TripleFilterModel


class Simulation:
    def __init__(self, number_of_agents, number_of_steps):
        self.number_of_agents = number_of_agents
        self.number_of_steps = number_of_steps
        self.model = TripleFilterModel(number_of_agents, "central")
    
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