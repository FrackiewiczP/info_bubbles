import asyncio
import fastapi
import socketio
from starlette.background import BackgroundTask, BackgroundTasks
import uvicorn
import random
import os
import tempfile
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from DatabaseConnection.database_connector import DatabaseConnector
from DatabaseConnection.database_connector import (
    CONNECTION_STRING,
    POSITIONS_COLLECTION_NAME,
    LINKS_COLLECTION_NAME,
    FLUCTUATION_COLLECTION_NAME,
    FRIEND_MEAN_DIST_COLLECTION_NAME,
    INFO_MEAN_DIST_COLLECTION_NAME,
    DATABASE_NAME,
)
from Simulation.model import TripleFilterModel
from Simulation.simulation_runner import SimulationRunner
from Simulation.communication_types import CommunicationType
from Simulation.website import InterUserCommunicationTypes
from FileSaver.csv_saver import CsvSaver
from Simulation.friend_links import FriendsLinksTypes

sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")

fastapi_app = FastAPI()
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
db_reader = DatabaseConnector(
    CONNECTION_STRING,
    DATABASE_NAME,
    POSITIONS_COLLECTION_NAME,
    LINKS_COLLECTION_NAME,
    FLUCTUATION_COLLECTION_NAME,
    FRIEND_MEAN_DIST_COLLECTION_NAME,
    INFO_MEAN_DIST_COLLECTION_NAME,
)
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
            inter_user_communication_form = InterUserCommunicationTypes.TO_ONE_RANDOM
        case "to_all":
            inter_user_communication_form = InterUserCommunicationTypes.TO_ALL
    match data["initial_connections"]:
        case "random_directed":
            initial_connections = FriendsLinksTypes.RANDOM_DIRECTED
        case "random_non_directed":
            initial_connections = FriendsLinksTypes.RANDOM_NON_DIRECTED
    model = TripleFilterModel(
        num_of_users=data["number_of_agents"],
        number_of_links=data["number_of_links"],
        memory_size=data["mem_capacity"],
        link_delete_prob=data["friend_lose_prob"],
        communication_form=communication_form,
        inter_user_communication_form=inter_user_communication_form,
        initial_connections=initial_connections,
        latitude_of_acceptance=data["acc_latitude"],
        sharpness_parameter=data["acc_sharpness"],
        percent_of_the_same_group=data["percent_of_the_same_group"],
        no_of_groups=data["no_of_groups"]
    )
    return SimulationRunner(
        data["number_of_steps"],
        model,
        DatabaseConnector(
            CONNECTION_STRING,
            DATABASE_NAME,
            POSITIONS_COLLECTION_NAME,
            LINKS_COLLECTION_NAME,
            FLUCTUATION_COLLECTION_NAME,
            FRIEND_MEAN_DIST_COLLECTION_NAME,
            INFO_MEAN_DIST_COLLECTION_NAME,
        ),
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
    print(f"Socket {sid} requested simulation with data {data}")
    result = ValidateData(data)
    if result != None:
        await sio.emit("error", result, room=sid)
        return
    await perform_simulation(sid, data)


@sio.event
async def simulation_step_requested(sid, step_num):
    step = db_reader.get_simulation_step(sid, int(step_num))
    await sio.emit("simulation_step_sent", step, room=sid)


@sio.event
async def simulation_stats_requested(sid, data):
    print(f"Socket {sid} requested simulation statistics for stat {data}")
    ret = db_reader.get_statistics_for_socket(sid, data)
    await sio.emit("simulation_stats_sent", ret, room=sid)


@fastapi_app.get("/simulation")
async def get_simulation(socket_id: str, background_tasks: BackgroundTasks):
    csv_saver = CsvSaver(db_reader)
    filename = f"{socket_id}.csv"

    # Send back 404, if a simulation for given socket_id haven't been run
    if not csv_saver.save_simulation_to_file(socket_id, filename):
        await sio.emit("error", "Simulation haven't been run", room=socket_id)

    background_tasks.add_task(delete_file, filename)
    return FileResponse(
        path=filename,
        media_type="application/octet-stream",
        filename=filename,
    )


def delete_file(path):
    os.remove(path)


def ValidateData(data):
    number_of_agents = data["number_of_agents"]
    memory_size = data["mem_capacity"]
    link_delete_prob = data["friend_lose_prob"]

    communication_form = None
    inter_user_communication_form = None
    initial_connections = None
    match data["initial_connections"]:
        case "random_directed":
            initial_connections = FriendsLinksTypes.RANDOM_DIRECTED
        case "random_non_directed":
            initial_connections = FriendsLinksTypes.RANDOM_NON_DIRECTED
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
            inter_user_communication_form = InterUserCommunicationTypes.TO_ONE_RANDOM
        case "to_all":
            inter_user_communication_form = InterUserCommunicationTypes.TO_ALL
    latitude_of_acceptance = data["acc_latitude"]
    sharpness_parameter = data["acc_sharpness"]
    percent_of_the_same_group = int(data["percent_of_the_same_group"])
    no_of_groups = data["no_of_groups"]
    number_of_links = data["number_of_links"]

    no_of_links = number_of_links * number_of_agents / 2
    links_on_group = no_of_links / no_of_groups
    in_each_group = number_of_agents / no_of_groups
    in_same_group_available = in_each_group * (in_each_group - 1) / 2
    in_same_group = (links_on_group * percent_of_the_same_group) / 100
    inter_group_available = in_each_group * (number_of_agents - in_each_group)
    inter_group_used = (links_on_group * (100 - percent_of_the_same_group)) / 100

    if in_same_group >= in_same_group_available or inter_group_used >= inter_group_available:
        return "Za dużo linków wewnątrz jednej grupy lub na zewnątrz niej"
    if number_of_agents < no_of_groups:
        return "Za dużo grup w stosunku do liczby agentów, zwiększ liczbę agentów ponad liczbę grup"
    if percent_of_the_same_group > 100 or percent_of_the_same_group < 0:
        return "Procent powinien być w przedziale [0,100]"
    if latitude_of_acceptance < 0 or latitude_of_acceptance > 1:
        return "Próg akceptacji powinien być w przedziale [0,1]"
    if communication_form is None:
        return "Nieznana wartość Komunikacji serwisu"
    if inter_user_communication_form is None:
        return "Nieznana wartość Komunikacji między użytkownikami"
    if initial_connections is None:
        return "Nieznana wartość Znajomości"
    if number_of_agents < 0 or no_of_groups < 0 or number_of_links < 0 or sharpness_parameter < 0 or memory_size < 0:
        return "Minimalna wartość to 0, jedna z wartości parametrów które ustawiłeś jest mniejsza od 0, popraw to"
    if link_delete_prob < 0 or link_delete_prob> 1:
        return "Prawdopodobieństwo stracenia przyjaciela powinno być z przedziału [0,1]"
    return None


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
