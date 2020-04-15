from abc import ABC


class AbstractServer(ABC):
    """
    Server running a specified PSI protocol.
    """

    def __init__(self, ip, port):
        """
        Args:
            ip: ip address to listen to
            port: port number to listen to
        """
        self._ip = ip
        self._port = port

    def start(self):
        """
        Start the server.
        """
        pass
