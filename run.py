from model import TripleFilterModel
import time
import tracemalloc
import pandas as pd
import numpy as np

if __name__ == "__main__":
    number_of_agents = 10000
    
    number_of_steps = 1000

    model = TripleFilterModel(number_of_agents, "individual")
    start_time = time.time()
    tracemalloc.start()
    for i in range(number_of_steps):
        print("--------------------" + str(i) + "----------------")
        model.step()
    print("total  --- %s seconds ---" % (time.time() - start_time))
    current, peak = tracemalloc.get_traced_memory()
    print(f"Peak memory usage was {peak / 10 ** 6} MB")
    tracemalloc.stop()
    positions = model.datacollector.get_model_vars_dataframe()
    positions = positions['Positions'].apply(pd.Series)
    positions = pd.melt(positions, value_vars=positions.columns[0:number_of_agents], var_name='ID',
                        value_name=' Position')
    positions["Time_step"] = np.repeat(range(number_of_steps), number_of_agents)
    positions.to_pickle("pos")
    positions.to_csv("postions.csv")
