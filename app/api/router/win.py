import psutil
import pythoncom
import win32api
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from ipaddress import ip_network
import wmi
import subprocess
from fastapi import APIRouter

from app.api.schema.base import RouterTags

router = APIRouter(prefix="/win", tags=[RouterTags.win])


@router.get("/computer")
def win_api_computer():
    win_computer_name = win32api.GetComputerName()
    return {"win_computer_name": win_computer_name}


@router.get("/process")
def win_api_process():
    process_count = len(psutil.pids())
    process_info = [
        process.info for process in psutil.process_iter(["pid", "name", "status"])
    ]
    return {"process_count": process_count, "process_info": process_info}


@router.get("/device-manager")
def win_api_device_manager():
    pythoncom.CoInitialize()
    unknown_devices = []
    for device in wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0):
        unknown_devices.append(
            {
                "DeviceID": device.DeviceID,
                "Name": device.Name,
                "Description": device.Description,
                "Status": device.Status,
            }
        )
    pythoncom.CoInitialize()
    return unknown_devices


@router.get("/network/enable-discovery")
def win_api_enable_network_discovery():
    script = '''
    $lang = (Get-Culture).Name
    if ($lang -eq "ko-KR") {
        $networkDiscovery = "네트워크 검색"
        $fileAndPrinterSharing = "파일 및 프린터 공유"
    } else {
        $networkDiscovery = "Network Discovery"
        $fileAndPrinterSharing = "File and Printer Sharing"
    }

    # 프라이빗 네트워크 설정
    Get-NetConnectionProfile | Where-Object { $_.NetworkCategory -eq "Public" } | Set-NetConnectionProfile -NetworkCategory Private

    # 필요한 서비스 설정
    Set-Service -Name FDResPub -StartupType Automatic
    Set-Service -Name SSDPSRV -StartupType Automatic
    Set-Service -Name upnphost -StartupType Automatic

    Start-Service -Name FDResPub
    Start-Service -Name SSDPSRV
    Start-Service -Name upnphost

    # 방화벽 규칙 활성화
    Enable-NetFirewallRule -DisplayGroup $networkDiscovery
    Enable-NetFirewallRule -DisplayGroup $fileAndPrinterSharing
    '''
    result = subprocess.run(["powershell", "-Command", script], capture_output=True, text=True)
    if result.returncode == 0:
        return {"status": "success", "message": "Network sharing has been enabled."}
    else:
        return {"status": "error", "message": result.stderr}


def check_host(ip_str):
    try:
        subprocess.check_output(["ping", "-n", "1", "-w", "100", ip_str], stderr=subprocess.DEVNULL)
        try:
            hostname = socket.gethostbyaddr(ip_str)[0]
        except socket.herror:
            hostname = "Unknown"
    except subprocess.CalledProcessError:
        return None
    return ip_str, hostname


def get_local_devices(network_cidr):
    network = ip_network(network_cidr)
    local_devices = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_host, str(ip)) for ip in network.hosts()]
        for future in as_completed(futures):
            result = future.result()
            if result:
                local_devices.append(result)

    return local_devices


@router.get("/network/local-computer")
def win_api_enable_network_local_computer():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 1))
    local_ip = s.getsockname()[0]
    network_cidr = local_ip.rsplit(".", 1)[0] + ".0/24"
    local_devices = get_local_devices(network_cidr)
    return {"devices": local_devices}
