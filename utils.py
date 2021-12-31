import asyncio
import logging
import sys
from asyncio import subprocess
from pathlib import Path
from importlib import import_module


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


async def install_requirements(requirements_path: Path):
    pip_proc = await subprocess.create_subprocess_exec(sys.executable, '-m', 'pip', 'install', '-r', requirements_path)
    await pip_proc.wait()


class AppBase:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem

    @property
    def requirements(self):
        return self.path.joinpath('requirements.txt')

    @property
    def package(self):
        return f'{self.path.parent.stem}.{self.name}'

    async def install_requirements(self):
        logging.info('Installing requirements for %s', self.name)
        await install_requirements(self.requirements)

    def init(self):
        logging.info('Initializing app %s', self.name)
        if self.requirements.exists():
            asyncio.run(self.install_requirements())
        logging.info('Importing %s', self.name)
        import_module('.app', package=self.package)
        logging.info('Module initialized %s', self.name)
