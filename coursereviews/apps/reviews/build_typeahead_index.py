import json
from django.conf import settings
from reviews.models import Course, Professor

def get_course_tokens(course):
    """Return an array of single word tokens, given a course object."""
    tokens = []

    # Code
    code = course.code.split(' ')[0]
    tokens.append(code)

    # Department
    dept_name_array = course.dept.name.replace("of ", "").replace("and ", "").replace("& ", "").split(" ")
    tokens.extend(dept_name_array)

    # Title
    title_array = course.title.replace("to ", "").replace("of ", "").replace("in ", "").split(" ")
    tokens.extend(title_array)

    return tokens

def get_professor_tokens(professor):
    """Returns and array of single word tokens, given a professor object."""
    tokens = []

    # Name
    tokens.append(professor.first)
    tokens.append(professor.last)

    # Department
    dept_name_array = professor.dept.name.replace("of ", "").replace("and ", "").replace("& ", "").split(" ")
    tokens.extend(dept_name_array)

    # Email
    tokens.append(professor.email)

    return tokens

def build_course_index():
    courses = Course.objects.all()
    course_index = map(lambda course: {
        "name": course.title,
        "value": course.lookup,
        "tokens": get_course_tokens(course)
        }, courses)

    return json.dumps(course_index)

def build_professor_index():
    professors = Professor.objects.all()
    professor_index = map(lambda professor: {
        "name": professor.__unicode__(),
        "value": professor.lookup,
        "tokens": get_professor_tokens(professor)
        }, professors)

    return json.dumps(professor_index)

def build_indices():
    file_path = settings.DJANGO_ROOT + "/static/reviews/"

    course_file = open(file_path + "courses.json", "w")
    course_file.write(build_course_index())
    course_file.close()

    professor_file = open(file_path + "professors.json", "w")
    professor_file.write(build_professor_index())
    professor_file.close()