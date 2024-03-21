from fastapi import APIRouter

from app.api.schema.base import RouterTags
from app.api.schema.win import (GetPrivateNetworkEnableResponseSchema,
                                GetPrivateNetworkResponseSchema,
                                GetWinSystemResponseSchema)
from app.api.service import win as win_service

router = APIRouter(prefix="/win", tags=[RouterTags.win])


@router.get(
    "/system",
    status_code=200,
    response_model=GetWinSystemResponseSchema,
    summary="PC 시스템 구성 요소 조회",
)
def get_local_system():
    return win_service.get_local_system()


@router.get(
    "/network/private",
    status_code=200,
    response_model=GetPrivateNetworkResponseSchema,
    summary="로컬 네트워크 스캔 결과 조회",
)
def get_private_network_pc():
    return win_service.get_private_network_pc()


@router.get(
    "/network/enable-discovery",
    status_code=200,
    response_model=GetPrivateNetworkEnableResponseSchema,
    summary="로컬 네트워크 탐색 기능 활성화",
)
def apply_network_enable_discovery():
    return win_service.apply_network_enable_discovery()
