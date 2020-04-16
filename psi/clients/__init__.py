from abc import ABC


class AbstractClient(ABC):
    """
    Client running a specified PSI protocol.
    """

    def __init__(self, elements, base_url):
        """
        Args:
            elements: client set to intersect with the server set.
            base_url: server base url, will be extended with step endpoints.
        """
        self._elements = elements
        self._base_url = base_url

    def intersect(self):
        """
        Run all steps required for the specific protocol the client 
        implements.

        Returns:
            The intersection of the client and server sets.
        """
        return []
