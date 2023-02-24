class User:
    """
    Represents a user, holds name, socket client and IP address
    """
    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        """
        Sets the username
        :param name: str
        """
        self.name = name

    def __repr__(self):
        return f'User({self.addr}, {self.name})'