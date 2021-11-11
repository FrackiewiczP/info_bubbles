import asyncio
import socketio
import uvicorn
import random

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = socketio.ASGIApp(sio)

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
    ret = {}
    for i in range(int(data)):
        ret[i] = [random.random(), random.random()]
    await sio.emit('simulation_finished', ret)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")