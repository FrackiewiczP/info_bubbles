from pymongo import MongoClient
import pymongo
from Simulation.model import StepData

CONNECTION_STRING = "mongodb://mongodb:27017"
DATABASE_NAME = "info_bubbles"
POSITIONS_COLLECTION_NAME = "positons"
LINKS_COLLECTION_NAME = "links"
FLUCTUATION_COLLECTION_NAME = "fluctuation"
SOCKET_ID_KEY = "socket_id"
STEP_NUM_KEY = "step_num"
DATA_KEY = "data"


class DatabaseConnector:
    def __init__(
        self,
        connection_string,
        db_name,
        positions_collection_name,
        links_collection_name,
        fluctuation_collection_name,
    ):
        self.__positions_collection = MongoClient(connection_string)[db_name][
            positions_collection_name
        ]
        self.__links_collection = MongoClient(connection_string)[db_name][
            links_collection_name
        ]
        self.__fluctuation_collection = MongoClient(connection_string)[db_name][
            fluctuation_collection_name
        ]

    def save_simulation_step(self, socket_id, step_num, data_to_add: StepData):
        pos_to_add = {
            SOCKET_ID_KEY: socket_id,
            STEP_NUM_KEY: step_num,
            DATA_KEY: data_to_add.users_positions,
        }
        self.__positions_collection.insert_one(pos_to_add)
        links_to_add = {
            SOCKET_ID_KEY: socket_id,
            STEP_NUM_KEY: step_num,
            DATA_KEY: data_to_add.links,
        }
        self.__links_collection.insert_one(links_to_add)
        fluc_to_add = {
            SOCKET_ID_KEY: socket_id,
            STEP_NUM_KEY: step_num,
            DATA_KEY: data_to_add.mean_fluctuation,
        }
        self.__fluctuation_collection.insert_one(fluc_to_add)

    def get_simulation_step(self, socket_id, step_num):
        return self.__positions_collection.find_one(
            {
                SOCKET_ID_KEY: socket_id,
                STEP_NUM_KEY: step_num,
            }
        )[DATA_KEY]

    def delete_previous_simulation_of_socket(self, socket_id):
        self.__positions_collection.delete_many({SOCKET_ID_KEY: socket_id})

    def get_number_of_steps_for_socket(self, socket_id):
        res = self.__positions_collection.find_one(
            {
                SOCKET_ID_KEY: socket_id,
            },
            sort=[(STEP_NUM_KEY, pymongo.DESCENDING)],
        )
        if res is None:
            return None
        else:
            return res[STEP_NUM_KEY]

    def get_statistics_for_socket(self, socket_id, statistic):
        collection = self.__statistic_to_collection(int(statistic))
        result = collection.find(
            {
                SOCKET_ID_KEY: socket_id
            },
            sort=[(STEP_NUM_KEY, pymongo.ASCENDING)]
        )
        return [x[DATA_KEY] for x in result]


    def __statistic_to_collection(self, statistic):
        match statistic:
            case 1:
                return self.__fluctuation_collection
            # case 2:
            #     return self.__avg_friend_dist_collection
            # case 3:
            #     return self.__avg_info_dist_collection

