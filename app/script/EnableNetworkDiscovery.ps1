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
