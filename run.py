from model import TripleFilterModel
import time
import tracemalloc
import pandas as pd
import numpy as np

if __name__ == "__main__":
    number_of_agents = 100

    number_of_steps = 10

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
    df = model.datacollector.get_model_vars_dataframe()
    df.to_pickle("pos")
    df_list = list()
    df.positions.apply(lambda x: df_list.append(pd.DataFrame.from_dict(x, orient="index")))
    df = pd.concat(df_list)
    df = df.reset_index()
    df.columns = ["user_id", "x_pos", "y_pos"]
    df["step"] = np.repeat(range(number_of_steps), number_of_agents)
    df.to_csv("positions.csv")
