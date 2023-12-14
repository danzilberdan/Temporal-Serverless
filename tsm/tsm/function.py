from io import BytesIO
import os
from pathlib import Path

import typer
import docker as dockerlib

from tsm.config import load_config, Function

from tsm.config import save_config


app = typer.Typer()
docker = dockerlib.from_env()


@app.command()
def create():
    config = load_config()

    while True:
        name = typer.prompt('Function name:', 'greet')
        if name and len(name) > 0 and config.func(name) is None:
            break
        typer.echo(f'A function named {name} already exist.')
    version = typer.prompt('Function version:', '0.1.0')
    description = typer.prompt('Function description:', default="")
    
    template = Path(os.path.abspath(__file__)).parent / 'function.template.py'
    with template.open() as file:
        pycode = file.read().format(workflow=name[0].upper() + name[1:], function=name)
    funcpath = Path(name + '.py')
    with funcpath.open('w') as file:
        file.write(pycode)
        
    config.functions.append(Function(name=name, version=version, description=description))
    save_config(config)


@app.command()
def build(func_name: str):
    funcconf = load_config().func(func_name)
    dockerfile = Path(os.path.abspath(__file__)).parent / 'Dockerfile'

    for line in docker.api.build(path='.', dockerfile=dockerfile, tag=funcconf.name, decode=True):
        if 'stream' in line:
            typer.echo(line['stream'])
        if 'error' in line:
            typer.echo(line['errorDetail']['message'])
