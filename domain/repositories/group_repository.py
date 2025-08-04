from abc import abstractmethod
from typing import List, Optional

from domain.entities.group import Group
from domain.repositories.base_entity_repository import BaseEntityRepository


class GroupRepository(BaseEntityRepository[Group, any]):
    """Repository interface for Group entity"""

    @abstractmethod
    def get_by_uuid(self, uuid) -> Optional[Group]:
        """
        Gets a group by its uuid

        :arg uuid: The group Uuid
        :return: The Group entity or None
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Group]:
        """
        Gets a list of all groups

        :return: A list of Group entities
        """
        pass

    @abstractmethod
    def create(self, entity: Group) -> Optional[Group]:
        """
        Creates a new group

        :arg entity: The Group entity to create
        :return: The created Group entity
        """
        pass

    @abstractmethod
    def update(self, entity: Group) -> bool:
        """
        Updates an existing group

        :arg entity: The Group entity with updated values
        :return: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, uuid) -> bool:
        """
        Deletes a group by its uuid

        :arg uuid: The group Uuid
        :return: True if the entity was successfully deleted otherwise False
        """
        pass

    @abstractmethod
    def get_by_teacher(self, teacher_uuid: str) -> List[Group]:
        """
        Get all groups taught by a specific teacher

        :param teacher_uuid: Teacher UUID
        :return: List of Group entities
        """
        pass

    @abstractmethod
    def get_by_subject(self, subject_uuid: str) -> List[Group]:
        """
        Get all groups for a specific subject

        :param subject_uuid: Subject UUID
        :return: List of Group entities
        """
        pass

    @abstractmethod
    def get_by_student(self, student_uuid: str) -> List[Group]:
        """
        Get all groups that a student is enrolled in

        :param student_uuid: Student UUID
        :return: List of Group entities
        """
        pass

    @abstractmethod
    def add_student_to_group(self, group_id: str, student_id: str) -> bool:
        """
        Add a student to a group

        :param group_id: Group UUID
        :param student_id: Student UUID
        :return: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def remove_student_from_group(self, group_id: str, student_id: str) -> bool:
        """
        Remove a student from a group

        :param group_id: Group UUID
        :param student_id: Student UUID
        :return: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def add_students_to_group(self, group_id: str, student_ids: List[str]) -> int:
        """
        Add multiple students to a group

        :param group_id: Group UUID
        :param student_ids: List of student UUIDs
        :return: Number of students successfully added
        """
        pass