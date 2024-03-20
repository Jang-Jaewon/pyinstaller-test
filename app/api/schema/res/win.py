from pydantic import BaseModel, Field
from typing import List, Optional


class ProcessInfo(BaseModel):
    pid: int = Field(title="프로세스 ID", description="프로세스 ID")
    name: str = Field(title="프로세스 이름", description="프로세스 이름")
    status: str = Field(title="프로세스 상태", description="프로세스 상태")


class DeviceInfo(BaseModel):
    device_id: str = Field(title="장치 ID", description="장치 ID")
    name: Optional[str] = Field(None, title="장치 이름", description="장치 이름")
    status: str = Field(title="장치 ID", description="장치 ID")


class GetWinSystem(BaseModel):
    pc_name: str = Field(title="로컬 PC 이름", description="참여자 이름")
    process_info: List[ProcessInfo] = Field(title="프로세스 정보", description="프로세스 정보")
    device_info: List[DeviceInfo] = Field(title="장치 관리자 정보", description="장치 관리자 정보")

