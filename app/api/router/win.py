from fastapi import APIRouter

from app.api.schema.base import RouterTags
from app.api.schema.res import win as res_win
from app.api.service import win as win_service

router = APIRouter(prefix="/win", tags=[RouterTags.win])


@router.get(
    "/system",
    status_code=200,
    response_model=res_win.GetWinSystem,
    summary="PC 시스템 구성 요소 조회"
)
def get_local_system():
    return win_service.get_local_system()


@router.get("/network/pc")
def get_private_network_pc():
    return win_service.get_private_network_pc()


@router.get("/network/enable-discovery")
def apply_network_enable_discovery():
    return win_service.apply_network_enable_discovery()
