from fastapi import FastAPI
from API.Routes import StudentRoutes
from Infraestructure.Database.Db import Base, engine

app = FastAPI(swagger_ui_parameters={
    "syntaxHighlight": False
})

Base.metadata.create_all(bind=engine)

app.include_router(StudentRoutes.router)
