
## Сервис биллинга в рамках сквозного проекта Yandex.Practicum // Middle python developer

![Диаграмма сервиса по спринту 10](/dev/gw/arch/005_ladiploma_c2-0.png?raw=true)

## Работа с платежными шлюзами/аггрегаторами

- External payments: реализация работы с [cloudpayments.ru](/dev/gw/payments/statemachine/providers/cloudpayments.py) для тестового аккаунта(ничто не мешает [реализовать поддержку любого другого провайдера](/dev/gw/payments/statemachine/providers/__init__.py#L57), поддерживающего widget-схему)
- Внешняя интеграция: 
  - [Pay](/dev/gw/payments/api/api/v1/pay.py) для [генерации платежнего виджета](/dev/gw/payments/api/services/pay.py) на базе json-параметров 
  - [Paid](/dev/gw/payments/api/api/v1/paid.py) для [приема callback и последующей обработки](/dev/gw/payments/api/services/paid.py)
  - [Cancel](/dev/gw/payments/api/api/v1/cancel.py) для [отмены подписки и возврата средств](/dev/gw/payments/api/services/cancel.py)
  - [Repay](/dev/gw/payments/api/api/v1/repay.py) для [повторной оплаты](/dev/gw/payments/api/services/repay.py) в соответствии с параметрами первой оплаты
- Внутренняя интеграция:
  - Из [Client Admin](dev/gw/payments-client/api/v1/subscriptions.py) читаем актуальные состояния напрямую из [StateStorage](/dev/gw/payments-client/models/models.py) или транслируем сообщения на шину (rabbitmq) 
  - Через SM (state machine, [набор Celery Tasks](/dev/gw/payments/statemachine/executor/tasks), реализующих **проведение внешних изменений** в lifecycle подписки в соответствии с сообщениями на шине) меняем состояние подписки

## Хранилище состояний (StateStorage)

- РСУБД (postgres) со всей информацией - от видов подписок до счетов и состояния по ним

## Машина состояния (StateMachine)

- Реализует модель состояния счетов в РСУБД (lifecycle событий по состоянию счета, требующих синхронизации с внешним провайдером)
- Обновляет модель по [consumed-сообщениям из rabbitmq](/dev/gw/payments/statemachine/paymessenger.py) (отдельный consumer-процесс)
- Запускает one-time и scheduled celery tasks, необходимые для реализации модели состояний
- Обновляет модель по результатам работы celery tasks

## PoC (Proof-of-Concept) UI
- простой [web UI на базу jQuery](/dev/gw/ui/web), исключительно для целей демо
- инфраструктурная обвязка (домен+хостинг с внешним ip, ssl, ip-DNAT на домашнюю инфраструктуру для возможности внешней демонстрации)
