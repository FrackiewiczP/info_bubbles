import asyncio
import socketio
import uvicorn
import random
from pymongo import MongoClient

from DatabaseConnection.database_connector import DatabaseConnector
from DatabaseConnection.database_connector import CONNECTION_STRING, COLLECTION_NAME, DATABASE_NAME
from Simulation.model import TripleFilterModel

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(sio)
db_reader = DatabaseConnector(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME)

def parse_data_from_frontend(socket_id, data):
    return TripleFilterModel(
        number_of_agents=data["number_of_agents"],
        number_of_steps=data["number_of_steps"],
        number_of_links=data["number_of_links"],
        mem_capacity=data["mem_capacity"],
        friend_lose_prob=data["friend_lose_prob"],
        communication_form=data["communication_form"],
        inter_user_communication_form=data["inter_user_communication_form"],
        acc_latitude=data["acc_latitude"],
        acc_sharpness=data["acc_sharpness"],
        db_connector=DatabaseConnector(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME),
        socket_id=socket_id,
    )

def perform_simulation(socket_id, data):
    model = parse_data_from_frontend(socket_id, data)
    model.run_simulation()

@sio.event
async def connect(sid, environ):
    print("connect ", sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def start_simulation(sid, data):
    print(sid)
    print(data)
    perform_simulation(sid, data)
    await sio.emit('simulation_finished', data["number_of_steps"], room=sid)

@sio.event
async def simulation_step_requested(sid, step_num):
    step = db_reader.get_simulation_step(sid, int(step_num))
    print(f"Socket {sid} requested step {step_num}")
    await sio.emit("simulation_step_sent", step)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")