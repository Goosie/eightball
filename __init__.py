import asyncio

from fastapi import APIRouter
from lnbits.db import Database
from lnbits.tasks import create_permanent_unique_task
from loguru import logger

from .tasks import wait_for_paid_invoices
from .views import eightball_ext_generic
from .views_api import eightball_ext_api

db = Database("ext_eightball")

scheduled_tasks: list[asyncio.Task] = []

eightball_ext: APIRouter = APIRouter(prefix="/eightball", tags=["eightball"])
eightball_ext.include_router(eightball_ext_generic)
eightball_ext.include_router(eightball_ext_api)

eightball_static_files = [
    {
        "path": "/eightball/static",
        "name": "eightball_static",
    }
]


def eightball_stop():
    for task in scheduled_tasks:
        try:
            task.cancel()
        except Exception as ex:
            logger.warning(ex)


def eightball_start():
    # ignore will be removed in lnbits `0.12.6`
    # https://github.com/lnbits/lnbits/pull/2417
    task = create_permanent_unique_task("ext_testing", wait_for_paid_invoices)  # type: ignore
    scheduled_tasks.append(task)
