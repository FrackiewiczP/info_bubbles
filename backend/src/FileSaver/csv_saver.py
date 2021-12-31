from DatabaseConnection.database_connector import DatabaseConnector
import csv


class CsvSaver:
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector

    def save_simulation_to_file(self, socket_id: str, filename: str) -> bool:
        max_step = self.db_connector.get_number_of_steps_for_socket(socket_id)
        if max_step is None:
            return False

        with open(filename, 'w') as f:
            data_writer = csv.writer(f)
            data_writer.writerow(["STEP", "USER_ID", "X", "Y"])
            for i in range (1, max_step+1):
                curr_step_data = self.db_connector.get_simulation_step(socket_id, i)
                for user_id in curr_step_data:
                    data_writer.writerow([str(i), user_id, curr_step_data[user_id][0], curr_step_data[user_id][1]])
        return True
