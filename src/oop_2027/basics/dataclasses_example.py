from datetime import datetime
from math import ceil

from pydantic import BaseModel




class Course(BaseModel):
    id: int
    name: str
    ects: float
    lecuter: Lecturer

class Lecturer(BaseModel):
    pesel: int
    name: str
    date_of_birth: datetime


def round_ects_up(course: Course):
    course.ects = ceil(course.ects)





if __name__ == '__main__':
    gg = Lecturer(pesel=1234567890, name='Jan', date_of_birth='2000-01-01T00:00:00')
    c1 = Course(id=1, name='Python', ects=4.0, lecuter=gg)
    c2 = Course(id=2, name='Java', ects=3.0, lecuter=gg)

    print(c1.name)

    ww = c1.model_dump_json()
    print(ww, type(ww))

    dd = c1.model_dump()
    print(dd, type(dd))

    cx1 = Course.model_validate_json(ww)
    print(c1 == cx1) # same content, different instances

    cd1 = Course.model_validate(dd)
    print(c1 == cd1)


    cx1.name = 'C++'
    print(c1 == cx1)  # True ? False ?
    print(id(c1), id(cx1)) # different instances

    c3 = c1 # c3 is an alias to c1 ... changing c3 changes c1
    c3.name = 'C#'
    print(c1 == c3) # True ? False ?

    print(id(c1), id(c3)) # same instances



    print(type(c1.ects))
    c1.ects = 4.5
    round_ects_up(c1)
    print(c1)
    print(type(c1.ects)) #meh... int again





