import os

from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional

import yaml


CONFIG_NAME = 'tsm.yaml'


class Function(BaseModel):
    name: str
    version: str
    description: Optional[str] = None

class AppConfig(BaseModel):
    functions: List[Function] = []

    def func(self, name: str):
        return next(filter(lambda func: func.name == name, self.functions), None)


def load_config() -> AppConfig:
    if Path(CONFIG_NAME).exists():
        with Path(CONFIG_NAME).open() as file:
            config = yaml.safe_load(file)
            return AppConfig.model_validate(config)
        
    return AppConfig()


def save_config(config: AppConfig) -> str:
    yamlconfig = yaml.dump(config.model_dump())
    with Path(CONFIG_NAME).open('w') as file:
        file.write(yamlconfig)
