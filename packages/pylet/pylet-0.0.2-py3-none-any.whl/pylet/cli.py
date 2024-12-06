import asyncio

import click
import uvicorn

from pylet.client import PyletClient
from pylet.server import app
from pylet.worker import Worker


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--head",
    type=str,
    default=None,
    help="Head node address (ip:port). If not provided, starts the head node.",
)
@click.option(
    "--cpu-cores",
    type=int,
    default=4,
    help="Number of CPU cores for the worker.",
)
@click.option(
    "--gpu-units",
    type=int,
    default=0,
    help="Number of GPU units for the worker.",
)
@click.option(
    "--memory-mb",
    type=int,
    default=4096,
    help="Amount of memory in MB for the worker.",
)
def start(head, cpu_cores, gpu_units, memory_mb):
    """
    Start the Pylet server (head node) or a worker node.
    """
    if head is None:
        # Start the server (head node)
        click.echo("Starting Pylet server...")
        uvicorn.run(
            "pylet.server:app", host="0.0.0.0", port=8000, reload=False
        )
    else:
        # Start a worker node connected to the head node
        click.echo(f"Starting Pylet worker connected to head node at {head}...")
        worker = Worker(
            head_address=head,
            cpu_cores=cpu_cores,
            gpu_units=gpu_units,
            memory_mb=memory_mb,
        )
        asyncio.run(worker.run())


@cli.command()
@click.argument("command", nargs=-1, required=True)
@click.option("--cpu-cores", type=int, default=1, help="CPU cores required.")
@click.option("--gpu-units", type=int, default=0, help="GPU units required.")
@click.option(
    "--memory-mb", type=int, default=512, help="Memory in MB required."
)
@click.option("--name", type=str, help="Optional task name.")
def submit(command, cpu_cores, gpu_units, memory_mb, name):
    """
    Submit a new task to the Pylet cluster.
    """

    async def submit_task():
        client = PyletClient()
        try:
            task_id = await client.submit_task(
                task_data=list(command),
                resource_requirements={
                    "cpu_cores": cpu_cores,
                    "gpu_units": gpu_units,
                    "memory_mb": memory_mb,
                },
                name=name,
            )
            click.echo(f"Task submitted with ID: {task_id}")
        except Exception as e:
            click.echo(f"Error submitting task: {e}", err=True)
        finally:
            await client.close()

    asyncio.run(submit_task())


@cli.command()
@click.option("--task-id", type=str, help="Task ID.")
@click.option("--name", type=str, help="Task name.")
def get_task(task_id, name):
    """
    Get task details by ID or name.
    """

    async def get_task_details():
        client = PyletClient()
        try:
            if name:
                task = await client.get_task_by_name(name)
            else:
                task = await client.get_task(task_id)
            click.echo(f"Task details: {task}")
        except Exception as e:
            click.echo(f"Error retrieving task: {e}", err=True)
        finally:
            await client.close()

    asyncio.run(get_task_details())


@cli.command()
@click.argument("task_id", type=str)
def get_result(task_id):
    """
    Get the result of a task by task ID.
    """

    async def get_task_result():
        client = PyletClient()
        try:
            result = await client.get_task_result(task_id)
            click.echo(f"Task result: {result}")
        except Exception as e:
            click.echo(f"Error retrieving task result: {e}", err=True)
        finally:
            await client.close()

    asyncio.run(get_task_result())


@cli.command()
def list_workers():
    """
    List all registered workers.
    """

    async def list_all_workers():
        client = PyletClient()
        try:
            workers = await client.list_workers()
            click.echo(f"Workers: {workers}")
        except Exception as e:
            click.echo(f"Error listing workers: {e}", err=True)
        finally:
            await client.close()

    asyncio.run(list_all_workers())


if __name__ == "__main__":
    cli()
