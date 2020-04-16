from abc import ABC


class AbstractServer(ABC):
    """
    Server running a specified PSI protocol.
    """

    def __init__(self, elements):
        """
        Args:
            elements: set set to intersect with the client set.
        """
        self._elements = elements
