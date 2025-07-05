from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from sqlalchemy.orm import Session

E = TypeVar('E')
M = TypeVar('M')
class IBaseEntityRepository(ABC, Generic[E, M]):
    @abstractmethod
    def get_by_uuid(self, uuid) -> E | None:
        """
        Gets an entity by uuid

        Args:
            uuid: The entity Uuid

        Returns:
            The entity or None
        """
        pass

    @abstractmethod
    def get_all(self) -> list[E]:
        """
        Gets a list of all entities

        Returns:
            A list of entities
        """
        pass

    @abstractmethod
    def create(self) -> E:
        """
        Creates an entity

        Returns:
            The created entity
        """
        pass

    @abstractmethod
    def update(self, uuid) -> E | None:
        """
        Updates an entity by uuid

        Args:
            uuid: The entity Uuid

        Returns:
            The entity or None
        """
        pass

    @abstractmethod
    def delete(self, uuid) -> bool:
        """
        Deletes an entity by uuid

        Args:
            uuid: The entity Uuid

        Returns:
            true if the entity was deleted successfully else false
        """
        pass

    @abstractmethod
    def _model_to_entity(self, model: M) -> E:
        pass

    @abstractmethod
    def _entity_to_model(self, entity: E) -> M:
        pass
