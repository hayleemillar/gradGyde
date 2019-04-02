import enum

class SemesterTypeEnum(enum.Enum):
	SPRING = "spring"
	SUMMER = "summer"
	FALL = "fall"
	ISP = "isp"

class UserTypeEnum(enum.Enum):
    STUDENT = "student"
    PROFESSOR = "professor"
    ADMIN = "administrator"
