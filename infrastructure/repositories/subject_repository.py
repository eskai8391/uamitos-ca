from sqlalchemy.orm import Session

from domain.value_objects import Uuid
from domain.repositories.base_entity_repository import BaseEntityRepository
from domain.entities.subject import Subject
from infrastructure.models.subject_model import SubjectModel


class SubjectRepository(BaseEntityRepository[Subject, SubjectModel]):
    def __init__(self, db: Session):
        self.__db = db

    def get_by_uuid(self, uuid) -> Subject | None:
        model = self.__db.query(SubjectModel).filter(SubjectModel.uuid == str(uuid)).first()
        if model:
            return self._to_entity(model)
        return None
    
    def get_by_code(self, code: str) -> Subject | None:
        model = self.__db.query(SubjectModel).filter(SubjectModel.code == code).first()
        if model:
            return self._to_entity(model)
        return None

    def get_all(self) -> list[Subject]:
        models = self.__db.query(SubjectModel).all()
        return [self._to_entity(model) for model in models]
    
    def get_by_teacher(self, teacher_uuid: str) -> list[Subject]:
        models = self.__db.query(SubjectModel).filter(SubjectModel.teacher_uuid == teacher_uuid).all()
        return [self._to_entity(model) for model in models]
    
    def get_by_semester(self, semester: int) -> list[Subject]:
        models = self.__db.query(SubjectModel).filter(SubjectModel.semester == semester).all()
        return [self._to_entity(model) for model in models]

    def create(self, entity: Subject) -> Subject | None:
        model = self._to_model(entity)
        self.__db.add(model)
        self.__db.commit()
        self.__db.refresh(model)
        return self._to_entity(model)

    def update(self, entity: Subject) -> Subject | None:
        model = self.__db.query(SubjectModel).filter(SubjectModel.uuid == str(entity.uuid)).first()
        if not model:
            return None
            
        # Update fields
        model.name = entity.name
        model.code = entity.code
        model.description = entity.description
        model.credits = entity.credits
        model.semester = entity.semester
        model.teacher_uuid = entity.teacher_uuid
        
        self.__db.commit()
        self.__db.refresh(model)
        return self._to_entity(model)

    def delete(self, uuid) -> bool:
        model = self.__db.query(SubjectModel).filter(SubjectModel.uuid == str(uuid)).first()
        if not model:
            return False
        
        self.__db.delete(model)
        self.__db.commit()
        return True

    def _to_model(self, entity: Subject) -> SubjectModel:
        return SubjectModel(
            uuid=str(entity.uuid),
            name=entity.name,
            code=entity.code,
            description=entity.description,
            credits=entity.credits,
            semester=entity.semester,
            teacher_uuid=entity.teacher_uuid
        )

    def _to_entity(self, model: SubjectModel) -> Subject:
        return Subject(
            uuid=Uuid.from_str(model.uuid),
            name=model.name,
            code=model.code,
            description=model.description,
            credits=model.credits,
            semester=model.semester,
            teacher_uuid=model.teacher_uuid
        )