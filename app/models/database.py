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
class Universities:
    university_id: int
    name: str
    location: str
    created_at: Optional[datetime] = None

@dataclass
class Major:
    major_id: int
    name: str
    created_at: Optional[datetime] = None

@dataclass
class UniversityMajor:
    id: int
    university_id: int  # References University.university_id
    major_id: int  # References Major.major_id
    maxCapacity: int
    minimumScore: int
    created_at: Optional[datetime] = None

@dataclass
class Student:
    id: int
    first_name: str
    last_name: str
    email: str
    password_hash: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    university_id: Optional[int] = None  # References University.university_id
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
    created_at: Optional[datetime] = None

@dataclass
class StudentActivity:
    student_id: int  # References Student.id
    activity_id: int  # References Activity.id