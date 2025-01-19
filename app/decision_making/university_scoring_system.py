# university_scoring_system.py

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
    location_bonus = 1 if student_location == university_location else 0
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
    location_bonus = 1 if student_location == university_location else 0
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
    location_bonus = 1 if student_location == university_location else 0
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
    location_bonus = 1 if student_location == university_location else 0
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
    location_bonus = 1 if student_location == university_location else 0
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
    location_bonus = 1 if student_location == university_location else 0
    total_score = sum(subjects.values()) + leadership_bonus + activity_bonus + location_bonus
    return total_score