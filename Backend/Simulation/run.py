import time
import tracemalloc

from model import TripleFilterModel

if __name__ == "__main__":
    number_of_agents = 1000

    number_of_steps = 10
    steps = [[100,0.1,0.1],
             [101, 0.1, 0.1],
             [102, 0.1, 0.1],
             [103, 0.1, 0.1],
             [104, 0.1, 0.1],
             [105, 0.1, 0.1],
             [106, 0.1, 0.1],
             [107, 0.1, 0.1],
             [108, 0.1, 0.1],
             [109, 0.1, 0.1],
             [110, 0.1, 0.1],
             [111, 0.1, 0.1]]
    model = TripleFilterModel(number_of_agents, "fromFileCentral",steps)

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
