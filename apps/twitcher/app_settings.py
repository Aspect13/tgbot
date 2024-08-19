from pathlib import Path

from utils import Singleton


class AppSettings(metaclass=Singleton):
    root_path = Path(__file__).absolute().parent

    def __init__(self):
        import json
        data = json.load(open(self.root_path.joinpath('creds.json'), 'r'))
        self.username = data.get('username')
        self.password = data.get('password')
