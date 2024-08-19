import asyncio
import logging
import sys
from asyncio import subprocess
from pathlib import Path
from importlib import import_module
from abc import abstractmethod, ABC, ABCMeta


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def purge(cls):
        del cls._instances[cls]


async def install_requirements(requirements_path: Path):
    pip_proc = await subprocess.create_subprocess_exec(
        sys.executable,
        '-m', 'pip', 'install', '-r', requirements_path,
        '--disable-pip-version-check', '-q'
    )
    await pip_proc.wait()


class BaseMixin(ABC):
    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.stem

    # @property
    # def name(self):
    #     return self.path.stem

    @property
    def requirements(self):
        return self.path.joinpath('requirements.txt')

    @property
    def package(self):
        return f'{self.path.parent.stem}.{self.name}'

    async def install_requirements(self):
        logging.info('Installing requirements for %s', self.name)
        await install_requirements(self.requirements)

    async def init(self):
        logging.info('Initializing app: [%s]', self.name)
        if self.requirements.exists():
            # asyncio.run(self.install_requirements())
            await self.install_requirements()
        logging.info('Importing [%s]', self.name)
        import_module('.app', package=self.package)
        logging.info('Initializing done: [%s]', self.name)


class TasksMixin(ABC):
    @property
    @abstractmethod
    def package(self) -> str:
        raise NotImplementedError

    @property
    def tasks(self):
        return self.path.joinpath('tasks.py')

    def init_tasks(self):
        if self.tasks.exists():
            logging.info('Initializing tasks [%s]', self.name)
            import_module('.tasks', package=self.package)
            logging.info('Tasks initialized [%s]', self.name)


class AppTG(BaseMixin, TasksMixin):
    ...

