# This file contains all the classes required to keep track of all the variables.
# This file contains class professor to which can store name of the professor, courses taught by that professsor.
# This file contains class classroom to which can store name of the classroom, size of that classroom.
# This file contains class course to which can store name, prefessors teaching, batch, class size, number of lectures required, lecture duration.
# This file contains class studentBatch to which can store one-hot-assignment id of a batch , courses for that batch.

# 10 Nov 2019, IIT Goa, GEC Campus, Farmagudi, Ponda, Goa, India

# Created by :-
# Raj S. Jagtap
# Neeraj Khatri
# Ujjawal Tiwari


import copy


class professor():
    def __init__(self, name):
        self.name = name
        self.courses_teaching = []

    def addCourse(self, subject):
        self.courses_teaching.append(subject)

    def getName(self):
        return copy.copy(self.name)

    def getCoursesTeaching(self):
        return copy.copy(self.courses_teaching)


class classroom():
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def getName(self):
        return copy.copy(self.name)

    def getSize(self):
        return copy.copy(self.size)


class course():
    def __init__(self, name, prof, batch, class_size, no_of_slots, duration):
        self.name = name
        self.prof = prof
        self.batch = batch
        self.class_size = class_size
        self.no_of_slots = no_of_slots
        self.duration = duration

    def getName(self):
        return copy.copy(self.name)

    def getProf(self):
        return copy.copy(self.prof)

    def getBatch(self):
        return copy.copy(self.batch)

    def getClassSize(self):
        return copy.copy(self.class_size)

    def getNoSlots(self):
        return copy.copy(self.no_of_slots)

    def getDuration(self):
        return copy.copy(self.duration)


class studentBatch():
    def __init__(self, batch_no):
        self.batch_no = batch_no
        self.courses = []

    def addCourse(self, subject):
        self.courses.append(subject)

    def getBatchNo(self):
        return copy.copy(self.batch_no)

    def getCourses(self):
        return copy.copy(self.courses)
