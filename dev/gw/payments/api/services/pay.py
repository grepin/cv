import base64
import json

from core.config import settings
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# accountId = user_id
# invoiceId = subscription_id
# {
#     "template": "cloudpayments.html",
#     "on_completed_callback": "http://pycinema.ru/paid/",
#     "description": "Оплата подписки в pycinema.ru",
#     "amount": "200",
#     "currency": "RUB",
#     "accountId": "c2d61d2b-4042-4a32-bea0-7cde7dceeca0",
#     "invoiceId": "cb64078d-16b2-4923-9a35-ea2ea4b13aad",
#     "email": "georgy.v.repin@yandex.ru",
#     "language": "ru-RU",
#     "data": { "referer": "https://pycinema.ru/subscriptions/" }
# }


class PaymentWidgetService:
    def __init__(self):
        self.template = Jinja2Templates(directory=settings.TEMPLATES_DIR)

    async def widget(self, request: Request, b64json: str) -> HTMLResponse:
        string = base64.urlsafe_b64decode(b64json)
        data = json.loads(string)
        return self.template.TemplateResponse(data['template'], {"request": request, **data})


def service():
    return PaymentWidgetService()
