from api.v1 import CancelNotification
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from services.cancel import CancelService
from services.cancel import service as cancel_service

router = APIRouter()


@router.post(
    "/",
    response_class=ORJSONResponse,
    summary="Отменяет подписку, если она ранее была оплачена пользоватлей и возвращает средства",
    description="Отправляет rabbitmq-сообщение для инициации соответствующей задаче по отмене платежа",
    response_description="JSON вида {'status': 'success'}",
    tags=['Отмена подписк и возврат платежа']
)
async def cancel(
    notification: CancelNotification,
    service: CancelService = Depends(cancel_service)
) -> str:
    try:
        await service.message2bus(notification.json())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
