import win32api
import pythoncom
import psutil
import wmi

from fastapi import APIRouter


router = APIRouter(prefix="/win", tags=["win"])


@router.get("/win/api/computer")
def win_api_computer():
    win_computer_name = win32api.GetComputerName()
    return {"win_computer_name": win_computer_name}


@router.get("/win/api/process")
def win_api_process():
    process_count = len(psutil.pids())
    process_info = [process.info for process in psutil.process_iter(["pid", "name", "status"])]
    return {
        "process_count": process_count,
        "process_info": process_info
    }


@router.get("/win/api/device-manager")
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
