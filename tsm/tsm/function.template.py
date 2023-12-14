import asyncio
from datetime import timedelta
import random

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


@activity.defn
async def flaky_greeting(name: str) -> str:
    if random.randint(0, 10) > 5:
        raise Exception('Randomly failed')
    else:
        return 'Hello ' + name


@workflow.defn
class {workflow}Workflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            flaky_greeting,
            'Alice',
            start_to_close_timeout=timedelta(seconds=10)
        )


async def main():
    client = await Client.connect("temporal:7233")

    async with Worker(
        client,
        task_queue="{function}-task-queue",
        workflows=[{workflow}Workflow],
        activities=[flaky_greeting],
    ):
        await asyncio.wait_for(asyncio.Future())


if __name__ == "__main__":
    asyncio.run(main())
