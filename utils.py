import uuid


class Id:
    def __init__(self) -> None:
        self._id = self.generate_id()

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())[:8]

    @property
    def id_(self):
        return self._id


class Body(str):
    def choose_body(self):
        bodies = ['седан', 'универсал', 'купе', 'хэтчбек', 'минивен', 'внедорожник', 'пикап']
        body = input('''Выберите кузов авто из следующих: 
            седан, универсал, купе, хэтчбек, минивен, внедорожник, пикап: ''').lower().strip()
        while not body in bodies:
            body = input('''Выберите кузов авто из следующих: 
            седан, универсал, купе, хэтчбек, минивен, внедорожник, пикап: ''').lower().strip()
        else: 
            return body