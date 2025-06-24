from Domain.Entities.Student import Student
from Domain.ValueObjects import StudentUuid, Email, Phone, ZipCode, Password

class StudentUseCases:
    def __init__(self):
        self.students = []

    def register_student(self, name, last_name, age, email, phone, address, city, state, zip_code, password):
        student = Student(
            id=StudentUuid.new(),
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
        self.students.append(student)
        return student