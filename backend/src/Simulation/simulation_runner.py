from time import time
import socketio
import tracemalloc
from Simulation.model import TripleFilterModel
import numpy as np
from DatabaseConnection.database_connector import DatabaseConnector


class SimulationRunner:
    def __init__(self, number_of_steps, model, db_connector, socket_server, socket_id):
        self.number_of_steps = number_of_steps
        self.model: TripleFilterModel = model
        self.db_connector: DatabaseConnector = db_connector
        self.socket_server: socketio.AsyncServer = socket_server
        self.socket_id = socket_id
        self.__iterations = 0

    async def run_simulation(self):
        start_time = time()
        tracemalloc.start()

        self.db_connector.delete_previous_simulation_of_socket(self.socket_id)
        for i in range(self.number_of_steps):
            print("--------------------" + str(i) + "----------------")
            self.__iterations += 1
            current_step_data = self.model.step()
            self.save_to_database(current_step_data)
            await self.send_to_socket(current_step_data)

        print("total  --- %s seconds ---" % (time() - start_time))
        current, peak = tracemalloc.get_traced_memory()
        print(f"Peak memory usage was {peak / 10 ** 6} MB")
        tracemalloc.stop()

    def save_to_database(self, current_step_data):
        self.db_connector.save_simulation_step(
            self.socket_id, self.__iterations, current_step_data
        )

    async def send_to_socket(self, current_step_data):
        current_step_data_with_list_values = {
            key: list(value)
            for (key, value) in current_step_data.users_positions.items()
        }
        data_to_send = {
            "step_number": self.__iterations,
            "step_data": current_step_data_with_list_values,
        }
        await self.socket_server.emit(
            "simulation_step_finished", data_to_send, room=self.socket_id
        )

    async def calculate_mean_distance_to_friends(self):
        for i in range(1, self.number_of_steps + 1):
            links = self.db_connector.get_links_from_step(self.socket_id, i)
            print(type(links))
            user_positions = self.db_connector.get_simulation_step(self.socket_id, i)
            distances = {str(id): [] for id in user_positions.keys()}
            for link in links:
                distance = np.linalg.norm(
                    np.array(user_positions[str(link[0])])
                    - np.array(user_positions[str(link[1])])
                )
                distances[str(link[0])].append(distance)
                distances[str(link[1])].append(distance)
            mean_distances = list()
            for id in distances:
                try:
                    mean_distances.append(sum(distances[id]) / len(distances[id]))
                except ZeroDivisionError:
                    continue
            mean_distance_in_step = sum(mean_distances) / len(mean_distances)
            self.db_connector.save_mean_distance_to_friends(
                self.socket_id, i, mean_distance_in_step
            )
