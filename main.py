from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utils import food_trucks


def food_trucks_data():
    return food_trucks.get_food_trucks_data()

model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    model['data'] = food_trucks_data
    yield
    model.clear()

app = FastAPI(lifespan=lifespan)

origins = '*'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/get-nearby-foodTrucks')
async def near_by_foodTrucks(address: str):
    data =  model['data']()
    add= food_trucks.get_latlong(address)
    
    result = sorted(
    [dict(x, distance=food_trucks.get_distance(add[0], add[1], x['latitude'], x['longitude'])) for x in data if food_trucks.get_distance(add[0], add[1], x['latitude'], x['longitude']) < 3],
    key=lambda x: x['distance']
)
    
    return result

@app.get('/trucks-data')
async def trucks_data():
    result = model['data']()
    return result
