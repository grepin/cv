from api.v1 import PaidNotification
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from services.paid import PaidCallbackService
from services.paid import service as paid_service

router = APIRouter()


@router.post(
    "/",
    response_class=ORJSONResponse,
    summary="Внешний callback, не требует ответа",
    description="Отправляет rabbitmq-сообщение для инициации соответствующей задаче по обновлению статуса платежа",
    response_description="JSON вида {'status': 'success'}",
    tags=['Коллбэки для приема ответов с виджетов']
)
async def paid(
    notification: PaidNotification,
    service: PaidCallbackService = Depends(paid_service)
) -> str:
    try:
        await service.message2bus(notification.json())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
