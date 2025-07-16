from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

E = TypeVar('E')
M = TypeVar('M')
class BaseEntityRepository(ABC, Generic[E, M]):
    @abstractmethod
    def get_by_uuid(self, uuid) -> E | None:
        """
        Gets an entity by its uuid

        :arg uuid: The entity Uuid

        :return: The entity or None
        """
        pass

    @abstractmethod
    def get_all(self) -> list[E]:
        """
        Gets a list of all entities

        :return: A list of entities
        """
        pass

    @abstractmethod
    def create(self, entity: E) -> E | None:
        """
        Creates an entity

        :return: The created entity
        """
        pass

    @abstractmethod
    def update(self, uuid) -> E | None:
        """
        Updates an entity by its uuid

        :arg uuid: The entity Uuid

        :return: The entity or None
        """
        pass

    @abstractmethod
    def delete(self, uuid) -> bool:
        """
        Deletes an entity by its uuid

        :arg uuid: The entity Uuid

        :return: True if the entity was successfully deleted otherwise False
        """
        pass

    @abstractmethod
    def _to_entity(self, model: M) -> E:
        """
        Converts a model to an entity

        :arg model: The model to be converted to an entity

        :return: The converted model
        """
        pass

    @abstractmethod
    def _to_model(self, entity: E) -> M:
        """
        Converts an entity to a model

        :arg entity: The entity to be converted to a model

        :return: The converted entity
        """
        pass
