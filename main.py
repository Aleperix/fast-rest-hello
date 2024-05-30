from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.routes import user, locations
from src.config.db import engine, Base
from sqladmin import Admin
import src.admin as admin_backend 

app = FastAPI(
    title="Fast Rest API", #Docs page project title
    description="A FastAPI backend boilerplate", #Docs page project description
    version="0.1.0", #Docs page project version
    swagger_ui_parameters={"defaultModelsExpandDepth": -1} #Remove schemas from docs page
)
admin = Admin(app, engine)
admin_backend.init(admin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "This is an example route"}


app.include_router(user.route)
app.include_router(locations.route)

Base.metadata.create_all(engine)

if __name__=="__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)