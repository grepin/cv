# subscribtion - для хранения состояния подписок и оплат по ним со следующими полями
    id: uuid
    user_id: str
    invoce_created: datetime
    payment_datetime: datetime
    subscribtion_expiration_datetime: datetime
    subscription_duration: int (выбираем из price)
    price: float (выбираем из price)
    currency: str (выбираем из price)
    payment_status: enum(invoce_created, payment_completed, payment_canceled)

# price - варианты подписок
    id: uuid
    duration: int
    price: float
    currency: enum
    created_at:
    admin_id:
    
# Я думаю state-машина будет работать следующим образом при оплате:
    - пользователь заходит в админку
    - при этом формируктся список актуальных подписок пользователя на текущий момент 
        и выдается пользователю
    - пользователь выбирает "новая подписка"
    - выбирает параметры подписки (начало и длительность подписки)
    - нажимает кнопку оплатить, при этом в subscribtion формируется запись со статусом invoce_created
    - в rabbitmq передается сообщение со следующими полями 
        {"user_id": user_id, "datetime": datetime.now(), "type_payment": "subscribtion_payment",
            "price":price, "subscribtion_id": subscribtion_id}
    - после этого пользователь перенаправляется на страницу оплаты
    - если оплата произведена успешно - по id в subscribtion меняем статус на payment_completed
    - отправляем пользователю письмо об успешной оплате
    - проверяем у пользователя действующие подписки и если есть - меняем role в таблице users на "subscriber"
    - и дальше нужно как-то придумать как пользователю обновить jwt-токены
   
# При возврате
    - пользователь заходит в админку
    - при этом формируктся список актуальных подписок пользователя на текущий момент 
        и выдается пользователю
    - пользователь выбирает действующую подписку
    - выбирает "отменить подписку"
    - высчитывается остаток для возврата
    - в rabbitmq передается сообщение со следующими полями 
        {"user_id": user_id, "datetime": datetime.now(), "subscribtion_reset",
            "price":price, "subscribtion_id": subscribtion_id}
    - после успешного прохождения возврата денег, по id в subscribtion меняем статус на payment_canceled
    - если у пользователя нет больше действубщих подписок - меняем role в таблице users на "unsubscriber"
    - тут заморачиваться с обновлением токенов не вижу смысла, т.к. в течение часа произойдет их обновление

