import socket
import subprocess

import psutil
import pythoncom
import win32api
import wmi


def get_pc_name():
    return win32api.GetComputerName()


def get_process_info():
    process_info = [
        process.info for process in psutil.process_iter(["pid", "name", "status"])
    ]
    return process_info


def get_device_info():
    pythoncom.CoInitialize()
    device_info = []
    for device in wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0):
        device_info.append(
            {
                "device_id": device.DeviceID,
                "name": device.Name,
                "status": device.Status,
            }
        )
    pythoncom.CoInitialize()

    return device_info


def get_network_cidr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 1))
    local_ip = s.getsockname()[0]
    network_cidr = local_ip.rsplit(".", 1)[0] + ".0/24"
    return network_cidr


def check_network_host(ip_str):
    try:
        subprocess.check_output(
            ["ping", "-n", "1", "-w", "100", ip_str], stderr=subprocess.DEVNULL
        )
        try:
            hostname = socket.gethostbyaddr(ip_str)[0]
        except socket.herror:
            hostname = "Unknown"
    except subprocess.CalledProcessError:
        return None
    return {"ip": ip_str, "hostname": hostname}
