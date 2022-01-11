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
    DATABASE_NAME,
)
from Simulation.model import TripleFilterModel
from Simulation.simulation_runner import SimulationRunner
from Simulation.communication_types import CommunicationType
from Simulation.website import InterUserCommunicationTypes
from FileSaver.csv_saver import CsvSaver

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

fastapi_app = FastAPI()
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
db_reader = DatabaseConnector(CONNECTION_STRING, DATABASE_NAME, POSITIONS_COLLECTION_NAME, LINKS_COLLECTION_NAME, FLUCTUATION_COLLECTION_NAME)
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
        percent_of_the_same_group=data["percent_of_the_same_group"],
        no_of_groups=data["no_of_groups"]
    )
    return SimulationRunner(
        data["number_of_steps"],
        model,
        DatabaseConnector(CONNECTION_STRING, DATABASE_NAME, POSITIONS_COLLECTION_NAME, LINKS_COLLECTION_NAME, FLUCTUATION_COLLECTION_NAME),
        sio,
        socket_id,
    )


async def perform_simulation(socket_id, data):
    if socket_id in current_simulations:
        await sio.emit("simulation_already_running")
        return
    current_simulations.add(socket_id)
    try:
        model = parse_data_from_frontend(socket_id, data)
    except:
        await sio.emit("error", "Data is invalid", room=socket_id)
        return
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
    if not ValidateData(data):
        await sio.emit("error", "Data is invalid", room=sid)
    else:
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
    return True

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
