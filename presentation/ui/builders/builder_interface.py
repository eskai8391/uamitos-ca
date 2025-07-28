from abc import ABC, abstractmethod
from typing import Self, Any, TypeVar

T = TypeVar('T')  # Return type for the build method

class Builder(ABC):
    """
    Abstract builder interface that defines the common methods all builders should implement.
    This serves as the foundation for all builder classes in the application.
    """

    @abstractmethod
    def create(self) -> Self:
        """
        Creates a new instance of the builder
        :return: A new builder instance
        """
        pass

    @abstractmethod
    def build(self) -> Any:
        """
        Builds the final product
        :return: The built product
        """
        pass

    @abstractmethod
    def clone(self) -> Self:
        """
        Creates a deep copy of the builder
        :return: A cloned builder instance
        """
        pass