from model import TripleFilterModel

if __name__ == "__main__":
    number_of_agents = 317
    number_of_steps = 50

    model = TripleFilterModel(40,"individual")

    for i in range(number_of_steps):
        print("--------------------" + str(i) + "----------------")
        model.step()
