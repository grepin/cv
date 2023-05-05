from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from services.pay import PaymentWidgetService
from services.pay import service as widget_service

router = APIRouter()


@router.get(
    "/{base64json}",
    response_class=HTMLResponse,
    summary="Получить HTML-страницу платежного виджета",
    description="Возвращает HTML-страницу платежного виджета, заполенную параметрами из base64 encoded json",
    response_description="HTML-страница платежного виджета",
    tags=['Параметризованный виджет для оплаты клиентом']
)
async def widget(
    request: Request,
    base64json: str,
    service: PaymentWidgetService = Depends(widget_service)
) -> str:
    try:
        return await service.widget(request, base64json)
    except Exception as e:
        raise HTTPException(status_code=501, detail=str(e))
