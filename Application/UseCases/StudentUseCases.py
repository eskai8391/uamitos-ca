from Domain.Entities.Student import Student
from Domain.ValueObjects import Uuid, Email, Phone, ZipCode, Password
from Domain.Repositories.IBaseEntityRepository import IBaseEntityRepository

class StudentUseCases:
    def __init__(self, repository: IBaseEntityRepository[Student]):
        self.__repository = repository

    def register_student(self, name, last_name, age, email, phone, address, city, state, zip_code, password):
        student = Student(
            uuid=Uuid.new(),
            name=name,
            last_name=last_name,
            age=int(age),
            email=Email(email),
            phone=Phone(phone),
            address=address,
            city=city,
            state=state,
            zip_code=ZipCode(zip_code),
            password=Password(password)
        )
        self.__repository.create(student)
        return student