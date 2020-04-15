from psi.protocols import Protocols
from psi.servers import AbstractServer


def client_intersect(elements, ip, port, protocol=Protocols.RSA):
    """
    Intersect client elements with remote elements on the server in a way that
    the client learns the intersection while the server learns nothing.

    Args:
        elements: client set to intersect with the server set.
        ip: ip address of the server holding the server set.
        port: port number of the server holding the server set.
        protocol: Protocol to be used to do the private set intersection.

    Returns:
        The intersection of the client and server sets.
    """
    pass


def create_server(elements, ip, port, protocol=Protocols.RSA):
    """
    Create a server for a specified protocol.

    Args:
        elements: server set to intersect with the client set.
        ip: ip address to listen to.
        port: port number to listen to.
        protocol: server's PSI protocol to use.
    """
    pass
