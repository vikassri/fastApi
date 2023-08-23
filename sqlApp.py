from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import databases
import sqlalchemy
import uvicorn, os
from datetime import datetime

# database url
DATABASE_URL = "sqlite:///./store.db"

# get the metadata of data stored
metadata = sqlalchemy.MetaData()

# create database conntions
database = databases.Database(DATABASE_URL)

# register the table into database
register = sqlalchemy.Table(
    "register",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(500)),
    sqlalchemy.Column("email", sqlalchemy.String(500)),
    sqlalchemy.Column("password", sqlalchemy.String(500)),
    sqlalchemy.Column("date_created", sqlalchemy.DateTime())
)

# create sql engine
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

# create fastapi instance
app = FastAPI()


# pydantic schema class
# input to API
class RegisterIn(BaseModel):
    name: str = Field(...)
    email: str =Field(...)
    password: str = Field(...)


# response model
class Register(BaseModel):
    id: int
    name: str
    email: str
    password: str
    date_created: datetime


@app.on_event("startup")
async def connect():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post('/register/', response_model=Register)
async def create(r: RegisterIn = Depends()):
    query = register.insert().values(
        name=r.name,
        email=r.email,
        password=r.password,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@app.post('/register/{id}', response_model=Register)  # path parameter
async def create(id: int, r: RegisterIn = Depends()):  # query parameter
    query = register.insert().values(
        id=id,
        name=r.name,
        email=r.email,
        password=r.password,
        date_created=datetime.utcnow()
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@app.get('/register/{id}', response_model=Register)
async def get_one(id: int):
    query = register.select().where(register.c.id == id)
    user = await database.fetch_one(query)
    return {**user}


@app.get('/register/', response_model=List[Register])
async def get_all():
    query = register.select()
    all_get = await database.fetch_all(query)
    return all_get


@app.put('/register/{id}', response_model=Register)
async def update(id: int, r: RegisterIn = Depends()):

    query = register.update().where(register.c.id == id).values(
        password=r.password,
        date_created=datetime.utcnow(),
    )
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == id)
    row = await database.fetch_one(query)
    return {**row}


@app.delete("/register/{id}", response_model=Register)
async def delete(id: int):
    query = register.delete().where(register.c.id == id)
    return await database.execute(query)

if __name__ == "__main__":
    uvicorn.run(app, host=os.uname()[1], port=8000, workers=1)
