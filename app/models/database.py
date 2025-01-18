from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Admin:
    id: int
    username: str
    password_hash: str
    email: str
    created_at: datetime

@dataclass
class University:
    id: int
    name: str
    minscore : int
    location: Optional[str] = None
    admin_id: Optional[int] = None  # References Admin.id
    created_at: Optional[datetime] = None

@dataclass
class Major:
    id: int
    name: str
    university_id: int  # References University.id
    created_at: Optional[datetime] = None

@dataclass
class Student:
    id: int
    first_name: str
    last_name: str
    email: str
    password_hash: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    university_id: Optional[int] = None  # References University.id
    location: Optional[str] = None
    leadership_position: Optional[bool] = False
    created_at: Optional[datetime] = None

@dataclass
class Grade:
    id: int
    student_id: int  # References Student.id
    course_name: str
    grade_value: float
    semester: Optional[str] = None
    created_at: Optional[datetime] = None

@dataclass
class Activity:
    id: int
    activity_name: str
    activity_date: Optional[datetime] = None
    description: Optional[str] = None

@dataclass
class StudentActivity:
    student_id: int  # References Student.id
    activity_id: int  # References Activity.id