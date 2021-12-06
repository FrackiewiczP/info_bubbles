import asyncio
import socketio
import uvicorn
import random
from pymongo import MongoClient

from Simulation.simulation import Simulation

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(sio)
client = MongoClient("mongodb://mongodb:27017")
simulations = {}

# Test connection to db
# print(client.server_info())

def parse_data_from_frontend(data):
    return Simulation(
        number_of_agents=data["number_of_agents"],
        number_of_steps=data["number_of_steps"],
        number_of_links=data["number_of_links"],
        mem_capacity=data["mem_capacity"],
        friend_lose_prob=data["friend_lose_prob"],
        communication_form=data["communication_form"],
        inter_user_communication_form=data["inter_user_communication_form"],
        acc_latitude=data["acc_latitude"],
        acc_sharpness=data["acc_sharpness"]
    )

def perform_simulation(data):
    sim = parse_data_from_frontend(data)
    res = sim.run_simulation()
    return res

def perform_mock_simulation(num_of_users, num_of_steps):
    result = []
    for i in range(num_of_steps):
        curr_step = {}
        if i == 0:
            for j in range(num_of_users):
                curr_step[j] = [random.random()*2-1, random.random()*2-1]
        else:
            for j in range(num_of_users):
                curr_step[j] = [result[i-1][j][0]+get_random_step(), result[i-1][j][1]+get_random_step()]
        result.append(curr_step)
    return result

def get_random_step():
    r = random.random()
    if(r < 0.5):
        return -0.01
    else:
        return 0.01

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
    result = perform_simulation(data)
    await sio.emit('simulation_finished', [result, data["number_of_steps"]], room=sid)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
