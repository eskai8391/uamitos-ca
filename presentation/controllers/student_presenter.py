from application.use_cases.student_use_cases import StudentUseCases, DeleteStudentRequest, UpdateStudentRequest, RegisterStudentRequest

class StudentPresenter:
    def __init__(self, use_cases: StudentUseCases):
        self.__use_cases = use_cases

    def register(self, data: dict):
        request = RegisterStudentRequest(
            name=data["name"],
            last_name=data["last_name"],
            age=data["age"],
            email=data["email"],
            phone=data["phone"],
            address=data["address"],
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
            plain_password = data["plain_password"]
        )

        return self.__use_cases.register_student(request)