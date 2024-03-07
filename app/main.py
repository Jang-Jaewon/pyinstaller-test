from contextlib import asynccontextmanager

import uvicorn
import win32api
import win32com.client
import pythoncom
import psutil
import wmi

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import ALLOWED_ORIGINS, APP_ENV, DEBUG
from app.core.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"INFO:     Hello, Run in the {APP_ENV} environment 👋")
    yield
    print(f"INFO:     Bye, Shut down in the {APP_ENV} environment 👋")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api-health-check")
def api_health_check():
    return {
        "api_health_check": "api-server is Ok",
        "APP_ENV": APP_ENV,
        "DEBUG": DEBUG,
        "ALLOWED_ORIGINS": ALLOWED_ORIGINS,
    }


@app.get("/win/api/computer")
def win_api_computer():
    win_computer_name = win32api.GetComputerName()
    return {"win_computer_name": win_computer_name}


@app.get("/win/api/process")
def win_api_process():
    process_count = len(psutil.pids())
    process_info = [process.info for process in psutil.process_iter(["pid", "name", "status"])]
    return {
        "process_count": process_count,
        "process_info": process_info
    }


@app.get("/win/api/device-manager")
def win_api_device_manager():
    pythoncom.CoInitialize()
    unknown_devices = []
    for device in wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0):
        unknown_devices.append({
                "DeviceID": device.DeviceID,
                "Name": device.Name,
                "Description": device.Description,
                "Status": device.Status
            }
        )
    pythoncom.CoInitialize()
    return unknown_devices


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
