from pymongo import MongoClient

CONNECTION_STRING="mongodb://mongodb:27017"
DATABASE_NAME="info_bubbles"
COLLECTION_NAME="simulations"
SOCKET_ID_KEY="socket_id"
STEP_NUM_KEY="step_num"
DATA_KEY="data"

class DatabaseConnector:
    def __init__(self, connection_string, db_name, collection_name):
        self.__collection = MongoClient(connection_string)[db_name][collection_name]
    
    def save_simulation_step(self, socket_id, step_num, data_to_add):
        to_add = {
            SOCKET_ID_KEY: socket_id,
            STEP_NUM_KEY: step_num,
            DATA_KEY: data_to_add,
        }
        self.__collection.insert_one(to_add)

    def get_simulation_step(self, socket_id, step_num):
        return self.__collection.find_one(
            {
                SOCKET_ID_KEY: socket_id,
                STEP_NUM_KEY: step_num,
            })[DATA_KEY]
    
    def delete_previous_simulation_of_socket(self, socket_id):
        self.__collection.delete_many({SOCKET_ID_KEY: socket_id})