from rest_framework.exceptions import APIException

"""
自定义异常，自定义个类，继承自APIException，并设置.status_code和.default_detail属性
"""
class CourseNotFound(APIException):
    status_code = 404
    default_detail = 'Course not found'

class BadRequest(APIException):
    status_code = 400
    default_detail = 'Parameter format error'

class PasswordError(APIException):
    status_code = 422
    default_detail = "Username or Password error"

class StudentNotFound(APIException):
    status_code = 404
    default_detail = 'Student not found'

class CannotComment(APIException):
    status_code = 403
    default_detail = 'Cannot submit comment'

class NotLogin(APIException):
    status_code = 403
    default_detail = "Forbidden, you need to login on to sport"

class EducationCrash(APIException):
    status_code = 400
    default_detail = "educational system is not available now"

class TooManyCourse(APIException):
    status_code = 403
    default_detail = "Too many courses"
