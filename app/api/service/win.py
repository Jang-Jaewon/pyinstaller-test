import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from ipaddress import ip_network

from app.core.util import win_api


def get_local_system():
    pc_name = win_api.get_pc_name()
    process_info = win_api.get_process_info()
    device_info = win_api.get_device_info()

    local_system = {
        "pc_name": pc_name,
        "process_info": process_info,
        "device_info": device_info,
    }
    return local_system


def get_private_network_pc():
    network_cidr = win_api.get_network_cidr()
    network = ip_network(network_cidr)
    private_network = []

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(win_api.check_network_host, str(ip))
            for ip in network.hosts()
        ]
        for future in as_completed(futures):
            result = future.result()
            if result:
                private_network.append(result)

    return {"private_network_scan": private_network}


def apply_network_enable_discovery():
    script = """
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
    """
    result = subprocess.run(
        ["powershell", "-Command", script], capture_output=True, text=True
    )
    if result.returncode == 0:
        return {"status": "success", "message": "Network sharing has been enabled."}
    else:
        return {"status": "error", "message": result.stderr}
