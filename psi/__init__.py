from psi.protocols import Protocols
from psi.servers import AbstractServer
from psi.clients import AbstractClient


def client_intersect(elements, base_url, protocol=Protocols.RSA):
    """
    Intersect client elements with remote elements on the server in a way that
    the client learns the intersection while the server learns nothing.

    Args:
        elements: client set to intersect with the server set.
        base_url: server base url, will be extended with step endpoints.
        protocol: Protocol to be used to do the private set intersection.

    Returns:
        The intersection of the client and server sets.
    """
    client = create_client(elements, base_url, protocol)
    return client.intersect()


def create_server(elements, protocol=Protocols.RSA):
    """
    Create a server for a specified protocol.

    Args:
        elements: server set to intersect with the client set.
        protocol: server's PSI protocol to use.

    Returns:
        A Server instance.
    """
    # Return specific server based on the protocol
    return AbstractServer(elements)


def create_client(elements, base_url, protocol=Protocols.RSA):
    """
    Create a client for a specified protocol.

    Args:
        elements: client set to intersect with the server set.
        base_url: server base url, will be extended with step endpoints.
        protocol: client's PSI protocol to use.

    Returns:
        A Client instance.
    """
    # Return specific client based on the protocol
    return AbstractClient(elements, base_url)