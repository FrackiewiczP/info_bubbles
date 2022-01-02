import asyncio
import socketio
import uvicorn
import random
from pymongo import MongoClient

from DatabaseConnection.database_connector import DatabaseConnector
from DatabaseConnection.database_connector import (
    CONNECTION_STRING,
    COLLECTION_NAME,
    DATABASE_NAME,
)
from Simulation.model import TripleFilterModel
from Simulation.simulation_runner import SimulationRunner
from Simulation.communication_types import CommunicationType
from Simulation.website import InterUserCommunicationTypes

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")
app = socketio.ASGIApp(sio)
db_reader = DatabaseConnector(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME)
current_simulations = set()


def parse_data_from_frontend(socket_id, data):
    match data["communication_form"]:
        case "individual":
            communication_form = CommunicationType.INDIVIDUAL
        case "central":
            communication_form = CommunicationType.CENTRAL
        case "filter_distant":
            communication_form = CommunicationType.FILTER_DISTANT
        case "filter_close":
            communication_form = CommunicationType.FILTER_CLOSE
    match data["inter_user_communication_form"]:
        case "to_one_random":
            inter_user_communication_form= InterUserCommunicationTypes.TO_ONE_RANDOM
        case "to_all":
            inter_user_communication_form = InterUserCommunicationTypes.TO_ALL
    model = TripleFilterModel(
        num_of_users=data["number_of_agents"],
        number_of_links=data["number_of_links"],
        memory_size=data["mem_capacity"],
        link_delete_prob=data["friend_lose_prob"],
        communication_form=communication_form,
        inter_user_communication_form=inter_user_communication_form,
        latitude_of_acceptance=data["acc_latitude"],
        sharpness_parameter=data["acc_sharpness"],
    )
    return SimulationRunner(
        data["number_of_steps"],
        model,
        DatabaseConnector(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME),
        sio,
        socket_id,
    )


async def perform_simulation(socket_id, data):
    if socket_id in current_simulations:
        await sio.emit("simulation_already_running")
        return
    current_simulations.add(socket_id)
    model = parse_data_from_frontend(socket_id, data)
    await model.run_simulation()
    current_simulations.remove(socket_id)


@sio.event
async def connect(sid, environ):
    print("connect ", sid)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


@sio.event
async def start_simulation(sid, data):
    print(sid)
    print(data)
    await perform_simulation(sid, data)


@sio.event
async def simulation_step_requested(sid, step_num):
    step = db_reader.get_simulation_step(sid, int(step_num))
    await sio.emit("simulation_step_sent", step)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
