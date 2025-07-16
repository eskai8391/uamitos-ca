from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    """
    Defines a password hash algorithm
    """

    @abstractmethod
    def hash_password(self, plain_value: str) -> str:
        """
        Generate a hash of the plain value

        :arg plain_value: The plain value to hash

        :return: The hashed value
        """
        pass

    @abstractmethod
    def verify_password(self, plain_value: str, hashed_value: str) -> bool:
        """
        Verifies a hash of the plain value

        :arg plain_value: The plain value to compare against
        :arg hashed_value: The hashed value to compare against

        :return: True if the hashed value matches the plain value otherwise False
        """
        pass