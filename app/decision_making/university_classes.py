class University:
    def __init__(self, name, capacity, location, majors, min_score_by_major):
        self.name = name
        self.capacity = capacity
        self.location = location  # Location of the university (city, country)
        self.majors = majors  # List of Major objects
        self.min_score_by_major = min_score_by_major  # Min score for each major at this university
        self.enrolled_students = 0

    def __repr__(self):
        return f"{self.name} ({self.location})"

    def get_min_score_for_major(self, major_name):
        return self.min_score_by_major.get(major_name, 0)

class Major:
    def __init__(self, name, capacity, scoring_method):
        self.name = name
        self.capacity = capacity
        self.scoring_method = scoring_method  # Function that calculates scores

    def __repr__(self):
        return self.name

class Student:
    def __init__(self, name, grades, activities, location, major):
        self.name = name
        self.grades = grades
        self.activities = activities
        self.location = location
        self.major = major
        self.score = 0

    def calculate_score(self, major, university_location):
        # Call the scoring method defined for the major
        self.score = major.scoring_method(self.grades, self.activities, self.location, university_location)

    def meets_criteria(self, university):
        min_score = university.get_min_score_for_major(self.major.name)
        return self.score >= min_score

    def __repr__(self):
        return f"{self.name} (Score: {self.score}, Location: {self.location})"

# Scoring functions for each major (same as before)

def business_admin_scoring(grades, activities, student_location, university_location):
    subjects = {
        'Mathematics': grades['Mathematics'] * 0.30,
        'Economics': grades['Economics'] * 0.20,
        'Philosophy': grades['Philosophy'] * 0.10,
        'Computer Science': grades['Computer Science'] * 0.10,
        'Physics': grades['Physics'] * 0.10,
        'Chemistry': grades['Chemistry'] * 0.10
    }
    leadership_bonus = len([activity for activity in activities if activity['position'] == 'Leader']) * 0.10
    activity_bonus = len([activity for activity in activities if activity['position'] != 'Leader']) * 0.05  # Activity bonus
    location_bonus = 5 if student_location == university_location else 0
    total_score = sum(subjects.values()) + leadership_bonus + activity_bonus + location_bonus
    return total_score

def accounting_scoring(grades, activities, student_location, university_location):
    subjects = {
        'Mathematics': grades['Mathematics'] * 0.40,
        'Economics': grades['Economics'] * 0.20,
        'Philosophy': grades['Philosophy'] * 0.05,
        'Computer Science': grades['Computer Science'] * 0.05,
        'Physics': grades['Physics'] * 0.10,
        'Chemistry': grades['Chemistry'] * 0.10
    }
    leadership_bonus = len([activity for activity in activities if activity['position'] == 'Leader']) * 0.10
    activity_bonus = len([activity for activity in activities if activity['position'] != 'Leader']) * 0.05  # Activity bonus
    finance_activities_bonus = len([activity for activity in activities if 'finance' in activity['name'].lower()]) * 0.05
    location_bonus = 5 if student_location == university_location else 0
    total_score = sum(subjects.values()) + leadership_bonus + activity_bonus + finance_activities_bonus + location_bonus
    return total_score

def finance_scoring(grades, activities, student_location, university_location):
    subjects = {
        'Mathematics': grades['Mathematics'] * 0.40,
        'Economics': grades['Economics'] * 0.30,
        'Computer Science': grades['Computer Science'] * 0.10,
        'Physics': grades['Physics'] * 0.05,
        'Philosophy': grades['Philosophy'] * 0.05,
        'Chemistry': grades['Chemistry'] * 0.05
    }
    leadership_bonus = len([activity for activity in activities if activity['position'] == 'Leader']) * 0.05
    activity_bonus = len([activity for activity in activities if activity['position'] != 'Leader']) * 0.03  # Activity bonus
    finance_related_bonus = len([activity for activity in activities if 'finance' in activity['name'].lower()]) * 0.10
    location_bonus = 5 if student_location == university_location else 0
    total_score = sum(subjects.values()) + leadership_bonus + activity_bonus + finance_related_bonus + location_bonus
    return total_score

def computer_science_scoring(grades, activities, student_location, university_location):
    subjects = {
        'Mathematics': grades['Mathematics'] * 0.40,
        'Computer Science': grades['Computer Science'] * 0.30,
        'Physics': grades['Physics'] * 0.10,
        'Chemistry': grades['Chemistry'] * 0.10,
        'Economics': grades['Economics'] * 0.05,
        'Philosophy': grades['Philosophy'] * 0.05
    }
    leadership_bonus = len([activity for activity in activities if activity['position'] == 'Leader']) * 0.05
    activity_bonus = len([activity for activity in activities if activity['position'] != 'Leader']) * 0.03  # Activity bonus
    tech_related_bonus = len([activity for activity in activities if 'computer' in activity['name'].lower()]) * 0.10
    location_bonus = 5 if student_location == university_location else 0
    total_score = sum(subjects.values()) + leadership_bonus + activity_bonus + tech_related_bonus + location_bonus
    return total_score

def computer_engineering_scoring(grades, activities, student_location, university_location):
    subjects = {
        'Mathematics': grades['Mathematics'] * 0.40,
        'Computer Science': grades['Computer Science'] * 0.20,
        'Physics': grades['Physics'] * 0.20,
        'Chemistry': grades['Chemistry'] * 0.10,
        'Economics': grades['Economics'] * 0.05,
        'Philosophy': grades['Philosophy'] * 0.05
    }
    leadership_bonus = len([activity for activity in activities if activity['position'] == 'Leader']) * 0.10
    activity_bonus = len([activity for activity in activities if activity['position'] != 'Leader']) * 0.05  # Activity bonus
    location_bonus = 5 if student_location == university_location else 0
    total_score = sum(subjects.values()) + leadership_bonus + activity_bonus + location_bonus
    return total_score

def mechanics_scoring(grades, activities, student_location, university_location):
    subjects = {
        'Mathematics': grades['Mathematics'] * 0.50,
        'Physics': grades['Physics'] * 0.30,
        'Chemistry': grades['Chemistry'] * 0.10,
        'Economics': grades['Economics'] * 0.05,
        'Philosophy': grades['Philosophy'] * 0.05
    }
    leadership_bonus = len([activity for activity in activities if activity['position'] == 'Leader']) * 0.05
    activity_bonus = len([activity for activity in activities if activity['position'] != 'Leader']) * 0.03  # Activity bonus
    location_bonus = 5 if student_location == university_location else 0
    total_score = sum(subjects.values()) + leadership_bonus + activity_bonus + location_bonus
    return total_score
