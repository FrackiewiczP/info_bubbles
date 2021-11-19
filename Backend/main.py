import asyncio
import socketio
import uvicorn
import random

from Simulation.simulation import Simulation

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(sio)
simulations = {}

def perform_simulation(num_of_agents, num_of_steps, info_latitude, info_sharpness):
    sim = Simulation(num_of_agents, num_of_steps, info_latitude, info_sharpness)
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
    result = perform_simulation(
        data["num_of_users"],
        data["num_of_steps"],
        data["info_latitude"],
        data["info_sharpness"])
    await sio.emit('simulation_finished', [result, data["num_of_steps"]], room=sid)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")