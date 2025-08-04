import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from domain.entities.group import Group
from domain.value_objects import Uuid
from domain.repositories.group_repository import GroupRepository as GroupRepositoryInterface
from infrastructure.models.group_model import GroupModel, group_students


class GroupRepository(GroupRepositoryInterface):
    """Implementation of GroupRepository interface for database operations"""
    
    def __init__(self, db_session: Session):
        """Initialize repository with database session"""
        self._db_session = db_session
        self._logger = logging.getLogger(__name__)
    
    def create(self, entity: Group) -> Optional[Group]:
        """
        Create a new group
        
        :param entity: Group entity to create
        :return: Created Group entity or None if failed
        """
        try:
            group_model = GroupModel(
                uuid=str(entity.uuid),
                name=entity.name,
                subject_uuid=entity.subject_uuid,
                teacher_uuid=entity.teacher_uuid,
                day_of_week=entity.day_of_week,
                start_time=entity.start_time,
                end_time=entity.end_time,
                room=entity.room,
                max_students=entity.max_students,
                semester=entity.semester
            )
            
            self._db_session.add(group_model)
            self._db_session.commit()
            
            # Add all students to the group
            if entity.students_uuids:
                self.add_students_to_group(str(entity.uuid), entity.students_uuids)
                
            return entity
        except Exception as e:
            self._logger.error(f"Error creating group: {e}")
            self._db_session.rollback()
            return None
    
    def get_by_uuid(self, uuid) -> Optional[Group]:
        """
        Gets a group by its uuid
        
        :param uuid: The group Uuid
        :return: The Group entity or None if not found
        """
        try:
            group_model = self._db_session.query(GroupModel).filter(GroupModel.uuid == uuid).first()
            
            if not group_model:
                return None
                
            # Get all students in this group
            student_ids = [
                student_id[0] for student_id in self._db_session.query(group_students.c.student_uuid)
                .filter(group_students.c.group_uuid == uuid)
                .all()
            ]
            
            return Group(
                uuid=Uuid(group_model.uuid),
                name=group_model.name,
                subject_uuid=group_model.subject_uuid,
                teacher_uuid=group_model.teacher_uuid,
                day_of_week=group_model.day_of_week,
                start_time=group_model.start_time,
                end_time=group_model.end_time,
                room=group_model.room,
                max_students=group_model.max_students,
                semester=group_model.semester,
                students_uuids=student_ids
            )
        except Exception as e:
            self._logger.error(f"Error getting group by UUID: {e}")
            return None
    
    def update(self, entity: Group) -> bool:
        """
        Update an existing group
        
        :param entity: Group entity with updated values
        :return: True if successful, False otherwise
        """
        try:
            group_model = self._db_session.query(GroupModel).filter(GroupModel.uuid == str(entity.uuid)).first()
            
            if not group_model:
                return False
                
            # Update group model attributes
            group_model.name = entity.name
            group_model.subject_uuid = entity.subject_uuid
            group_model.teacher_uuid = entity.teacher_uuid
            group_model.day_of_week = entity.day_of_week
            group_model.start_time = entity.start_time
            group_model.end_time = entity.end_time
            group_model.room = entity.room
            group_model.max_students = entity.max_students
            group_model.semester = entity.semester
            
            self._db_session.commit()
            
            # Update students in the group
            if entity.students_uuids is not None:
                # Remove all existing students
                self._db_session.query(group_students).filter(group_students.c.group_uuid == str(entity.uuid)).delete()
                
                # Add the new students
                self.add_students_to_group(str(entity.uuid), entity.students_uuids)
            
            return True
        except Exception as e:
            self._logger.error(f"Error updating group: {e}")
            self._db_session.rollback()
            return False
    
    def delete(self, uuid) -> bool:
        """
        Delete a group
        
        :param uuid: Group UUID
        :return: True if successful, False otherwise
        """
        try:
            # First remove all student associations
            self._db_session.query(group_students).filter(group_students.c.group_uuid == uuid).delete()
            
            # Then delete the group
            result = self._db_session.query(GroupModel).filter(GroupModel.uuid == uuid).delete()
            self._db_session.commit()
            
            return result > 0
        except Exception as e:
            self._logger.error(f"Error deleting group: {e}")
            self._db_session.rollback()
            return False
    
    def get_all(self) -> List[Group]:
        """
        Get all groups
        
        :return: List of Group entities
        """
        try:
            group_models = self._db_session.query(GroupModel).all()
            return [self.get_by_uuid(group_model.uuid) for group_model in group_models]
        except Exception as e:
            self._logger.error(f"Error getting all groups: {e}")
            return []
    
    def get_by_teacher(self, teacher_uuid: str) -> List[Group]:
        """
        Get all groups taught by a specific teacher
        
        :param teacher_uuid: Teacher UUID
        :return: List of Group entities
        """
        try:
            group_models = self._db_session.query(GroupModel).filter(GroupModel.teacher_uuid == teacher_uuid).all()
            return [self.get_by_uuid(group_model.uuid) for group_model in group_models]
        except Exception as e:
            self._logger.error(f"Error getting groups by teacher: {e}")
            return []
    
    def get_by_subject(self, subject_uuid: str) -> List[Group]:
        """
        Get all groups for a specific subject
        
        :param subject_uuid: Subject UUID
        :return: List of Group entities
        """
        try:
            group_models = self._db_session.query(GroupModel).filter(GroupModel.subject_uuid == subject_uuid).all()
            return [self.get_by_uuid(group_model.uuid) for group_model in group_models]
        except Exception as e:
            self._logger.error(f"Error getting groups by subject: {e}")
            return []
    
    def get_by_student(self, student_uuid: str) -> List[Group]:
        """
        Get all groups that a student is enrolled in
        
        :param student_uuid: Student UUID
        :return: List of Group entities
        """
        try:
            group_ids = [
                group_id[0] for group_id in self._db_session.query(group_students.c.group_uuid)
                .filter(group_students.c.student_uuid == student_uuid)
                .all()
            ]
            
            return [self.get_by_uuid(group_id) for group_id in group_ids]
        except Exception as e:
            self._logger.error(f"Error getting groups by student: {e}")
            return []
    
    def add_student_to_group(self, group_id: str, student_id: str) -> bool:
        """
        Add a student to a group
        
        :param group_id: Group UUID
        :param student_id: Student UUID
        :return: True if successful, False otherwise
        """
        try:
            # Check if the group exists and has capacity
            group = self.get_by_uuid(group_id)
            if not group:
                return False
                
            # Check if student is already in the group
            is_already_enrolled = self._db_session.query(func.count()).filter(
                group_students.c.group_uuid == group_id,
                group_students.c.student_uuid == student_id
            ).scalar() > 0
            
            if is_already_enrolled:
                return True  # Already enrolled, consider it a success
                
            # Check if the group has reached max capacity
            current_enrollment = self._db_session.query(func.count()).filter(
                group_students.c.group_uuid == group_id
            ).scalar()
            
            if current_enrollment >= group.max_students:
                return False  # Group is full
            
            # Add student to group
            self._db_session.execute(
                group_students.insert().values(
                    group_uuid=group_id,
                    student_uuid=student_id
                )
            )
            self._db_session.commit()
            return True
        except Exception as e:
            self._logger.error(f"Error adding student to group: {e}")
            self._db_session.rollback()
            return False
    
    def remove_student_from_group(self, group_id: str, student_id: str) -> bool:
        """
        Remove a student from a group
        
        :param group_id: Group UUID
        :param student_id: Student UUID
        :return: True if successful, False otherwise
        """
        try:
            result = self._db_session.query(group_students).filter(
                group_students.c.group_uuid == group_id,
                group_students.c.student_uuid == student_id
            ).delete()
            
            self._db_session.commit()
            return result > 0
        except Exception as e:
            self._logger.error(f"Error removing student from group: {e}")
            self._db_session.rollback()
            return False
    
    def add_students_to_group(self, group_id: str, student_ids: List[str]) -> int:
        """
        Add multiple students to a group
        
        :param group_id: Group UUID
        :param student_ids: List of student UUIDs
        :return: Number of students successfully added
        """
        success_count = 0
        for student_id in student_ids:
            if self.add_student_to_group(group_id, student_id):
                success_count += 1
                
        return success_count
    
    def _to_entity(self, model) -> Group:
        """
        Converts a model to a Group entity
        
        :param model: The GroupModel to be converted
        :return: Group entity
        """
        # Get all students in this group
        student_ids = [
            student_id[0] for student_id in self._db_session.query(group_students.c.student_uuid)
            .filter(group_students.c.group_uuid == model.uuid)
            .all()
        ]
        
        return Group(
            uuid=Uuid(model.uuid),
            name=model.name,
            subject_uuid=model.subject_uuid,
            teacher_uuid=model.teacher_uuid,
            day_of_week=model.day_of_week,
            start_time=model.start_time,
            end_time=model.end_time,
            room=model.room,
            max_students=model.max_students,
            semester=model.semester,
            students_uuids=student_ids
        )
    
    def _to_model(self, entity: Group) -> GroupModel:
        """
        Converts a Group entity to a GroupModel
        
        :param entity: The Group entity to be converted
        :return: GroupModel
        """
        return GroupModel(
            uuid=str(entity.uuid),
            name=entity.name,
            subject_uuid=entity.subject_uuid,
            teacher_uuid=entity.teacher_uuid,
            day_of_week=entity.day_of_week,
            start_time=entity.start_time,
            end_time=entity.end_time,
            room=entity.room,
            max_students=entity.max_students,
            semester=entity.semester
        )