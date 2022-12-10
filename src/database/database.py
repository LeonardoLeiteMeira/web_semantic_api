from models.singleton import Singleton

class Database(metaclass=Singleton):
    def __init__(self):
        self.client = "lib('localhost', 000)"