from api.v1 import RepaymentNotification
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from services.repay import RepayService
from services.repay import service as repayment_service

router = APIRouter()


@router.post(
    "/",
    response_class=ORJSONResponse,
    summary="Осуществляет повторную оплату по токену",
    description="Отправляет rabbitmq-сообщение для инициации recurrent-платежа по токену",
    response_description="JSON вида {'status': 'success'}",
    tags=['Повторный платеж']
)
async def repay(
    notification: RepaymentNotification,
    service: RepayService = Depends(repayment_service)
) -> str:
    try:
        await service.message2bus(notification.json())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
