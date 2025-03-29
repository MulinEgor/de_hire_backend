"""Модуль для обработки событий с блокчейна"""

import asyncio
import json
import logging

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from web3 import Web3
from websockets import connect

import src.core.jobs.schemas as job_schemas
import src.core.ratings.schemas as rating_schemas
import src.core.resumes.schemas as resume_schemas
from src.core.jobs import JobService
from src.core.ratings.service import RatingService
from src.core.resumes.service import ResumeService
from src.worker import constants
from src.worker.settings import settings

logger = logging.getLogger("worker")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)


# MARK: ABI
async def get_abi() -> dict:
    """
    Получение ABI через Etherscan API

    Returns:
        dict: ABI в виде словаря
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(constants.ABI_URL) as response:
            data = await response.json()
            if data["status"] == "1":
                return json.loads(data["result"])

        raise Exception(f"Ошибка получения ABI: {data['result']}")


# MARK: Events
async def handle_event(
    event: dict,
    session: AsyncSession,
):
    """
    Обработка событий.
    Добавление или изменение данных в БД.

    Args:
        event (dict): Событие для обработки
        session (AsyncSession): Сессия базы данных
    """

    logger.info(f"Начало обработки события: {event['event']}")
    try:
        match event["event"]:
            # MARK: Job events
            case "JobCreatedEvent":
                logger.info(f"Добавление новой задачи: {event['args']}")
                schema = job_schemas.JobCreateSchema(**event["args"])
                await JobService.create(session, schema)

            case "JobApplicationEvent":
                logger.info(f"Добавление заявки на работу: {event['args']}")
                schema = job_schemas.JobApplicationSchema(**event["args"])
                await JobService.create_application(session, schema)

            case (
                "JobAssignedEvent",
                "JobWaitingReviewEvent",
                "JobCompletedEvent",
                "JobCancelledEvent",
                "JobReopenedEvent",
            ):
                logger.info(f"Обновление статуса задачи: {event['args']}")
                schema = job_schemas.JobUpdateSchema(
                    **event["args"],
                    status=constants.EVENT_TO_STATUS[event["event"]],
                )
                await JobService.update(
                    session,
                    schema.job_id,
                    schema.model_dump(exclude={"job_id"}),
                )

            # MARK: Ratings events
            case "RatingCreatedEvent":
                logger.info(f"Добавление новой оценки: {event['args']}")
                schema = rating_schemas.RatingSchema(**event["args"])
                await RatingService.create(session, schema)

            # MARK: Resume events
            case "ResumeCreatedEvent":
                logger.info(f"Добавление нового резюме: {event['args']}")
                schema = resume_schemas.ResumeCreateSchema(**event["args"])
                await ResumeService.create(session, schema)

            case _:
                logger.info(event)

        logger.info(f"Событие {event['event']} успешно обработано")

    except Exception as e:
        logger.error(f"Ошибка при обработке события: {e}")


# MARK: Listen
async def listen_to_events():
    w3 = Web3()
    contract_abi = await get_abi()
    contract = w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=contract_abi)

    logger.info("Подключение по WebSockets...")
    async with connect(constants.WEBSOCKET_URL) as ws:
        await ws.send(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "eth_subscribe",
                    "params": ["logs", {"address": settings.CONTRACT_ADDRESS}],
                }
            )
        )

        logger.info("Ожидание событий...")
        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)

                logger.info(f"Получено событие: {data}")

                if "params" in data:
                    log = data["params"]["result"]
                    for abi_entry in contract_abi:
                        if abi_entry["type"] == "event":
                            event_name = abi_entry["name"]
                            try:
                                event = getattr(
                                    contract.events, event_name
                                ).process_log(log)
                                await handle_event(event)

                            except Exception:
                                pass

            except Exception as e:
                logger.error(f"Ошибка: {e}, переподключаемся...")
                await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(listen_to_events())
