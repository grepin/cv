from db.rabbitmq import RabbitMQ
from db.rabbitmq import instance as rmq_instance
from fastapi import Depends


class RepayService:
    def __init__(self, rmq: RabbitMQ):
        self.rmq = rmq

    async def message2bus(self, options: str) -> None:
        await self.rmq.publish(message=options, headers={"from": "client-repay"})


def service(
    rmq: RabbitMQ = Depends(rmq_instance)
):
    return RepayService(rmq=rmq)
