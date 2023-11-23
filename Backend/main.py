from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ReportRouter
from db import Tag, Location, Report
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from decouple import config


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ReportRouter.router)

 
@app.on_event('startup')
async def connect_db():
    client = AsyncIOMotorClient(
        config("MONGO_URL", cast=str, default="mongodb://localhost:27017"))

    await init_beanie(database=client.Hackaty, document_models=[Tag, Location, Report])


@app.get("/")
def index():
    return {"message": "Hello from Hackaty✌️"}


@app.get("/api")
def api():
    return {"message": "Hello dev from Hackaty✌️"}


@app.get("/mock")
async def mock_data():
    tags = [{'name': 'น้ำท่วม'}, {'name': 'เตือนภัย'},
           {'name': 'ถนน'}, {'name': 'ความปลอดภัย'}]
    for x in tags:
        await Tag.insert(Tag(**x))

    location = [{"lat": 42.941033134628, "lon":  153.794558983582}, {
        "lat": 24.078036436108, "lon": -120.782015917934}]

    for y in location:
        await Location.insert(Location(**y))

    report = {"title": "น้ำท่วม", "user": "user1",
               "tags": [{'name': 'น้ำท่วม'}, {'name': 'เตือนภัย'}],
               "location": {"lat": 42.941033134628, "lon":  153.794558983582},
               "description": "ช่วยด้วยย",
               "timestamp": '2023-11-22 11:49:10.833520',
               "priority": 'Low',
               "report_status": "Inbox",
               "vote_score": 12
               }
    
    await Report.insert(Report(**report))
    return {"message": "Mock data successfully"}
