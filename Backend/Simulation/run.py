import time
import tracemalloc

from model import TripleFilterModel

if __name__ == "__main__":
    number_of_agents = 1000

    number_of_steps = 1000

    model = TripleFilterModel(number_of_agents, "central")

    start_time = time.time()

    tracemalloc.start()
    for i in range(number_of_steps):
        print("--------------------" + str(i) + "----------------")
        model.step()
    print("total  --- %s seconds ---" % (time.time() - start_time))
    current, peak = tracemalloc.get_traced_memory()
    print(f"Peak memory usage was {peak / 10 ** 6} MB")
    tracemalloc.stop()
    model.save_output()
