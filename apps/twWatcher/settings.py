from pathlib import Path

from utils import Singleton


class Settings(metaclass=Singleton):
    root_path = Path(__file__).absolute().parent

    @property
    def cookie_file(self):
        return self.root_path.joinpath(f'cookies_{self.username}.pkl'.lower())

    def __init__(self):
        import json
        data = json.load(open(self.root_path.joinpath('creds.json'), 'r'))
        self.username = data.get('username')
        self.password = data.get('password')
