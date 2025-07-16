from fastapi import FastAPI
from presentation.api.routes import student_routes
from infrastructure.database.db import Base, engine

app = FastAPI(swagger_ui_parameters={
    "syntaxHighlight": False
})

Base.metadata.create_all(bind=engine)

app.include_router(StudentRoutes.router)
