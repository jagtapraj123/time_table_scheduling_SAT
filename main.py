# This file contains logic behind the program.
# It takes input of a JSON input file, decodes it and stores in different objects.
# It creates variables and and check constraints.

# 10 Nov 2019, IIT Goa, GEC Campus, Farmagudi, Ponda, Goa, India

# Created by :-
# Raj S. Jagtap
# Neeraj Khatri
# Ujjawal Tiwari


import xlsxwriter
from z3 import *
from variables import professor, classroom, course, studentBatch
import json

with open('assign1_input.json') as json_file:
    data = json.load(json_file)
    rt = data["Room Types"]
    it = data["Institute time"]
    r = data["Classrooms"]
    c = data["Courses"]

classrooms = []
for i in r:
    classrooms.append(classroom(i[0], i[1]))


p = set()
for i in c:
    for j in i[3]:
        p.add(j)


p = list(p)
professors = []     # Adresses of professors
for i in p:
    professors.append(professor(i))


b = set()
for i in c:
    for j in i[4]:
        b.add(j)

b = list(b)

for i in range(len(b)):
    b[i] = b[i].split()


tech = set()
year = set()
branch = set()
for i in b:
    branch.add(i[0])
    tech.add(i[1])
    year.add(i[2])

branch = sorted(branch)
tech = sorted(tech)
year = sorted(year)

batches = []
for i in b:
    batches.append(studentBatch(tech.index(
        i[1])*100 + year.index(i[2])*10 + branch.index(i[0])))


courses = []
for i in c:
    temp = []
    for j in i[3]:
        temp.append(professors[p.index(j)])
        professors[p.index(j)].addCourse(i[0])
    temp2 = []
    for j in i[4]:
        temp2.append(batches[b.index(j.split())])
        batches[b.index(j.split())].addCourse(i[0])
    courses.append(course(i[0], temp, temp2, i[1], len(i[2]), i[2][0]))


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
time_avail = [8.50, 9.00, 9.50, 10.00,
              10.50, 11.00, 11.50, 12.00, 14.00, 14.50, 15.00, 15.50, 16.00, 16.50, 17.00, 17.50]
periods = [0.50, 1.00, 1.50, 2.00, 2.50, 3.00]

s = Solver()


# Creating Variables

# Creating possible timings
time_slots = {}
for p in periods:
    time_slots[str(p)] = {}
    for d in days:
        time_slots[str(p)][str(d)] = []
        for t in time_avail:
            # print(t+p)
            if ((t < 12.5 and t+p <= 12.5) or (t >= 14.0 and t+p <= 18.00)):
                time_slots[str(p)][str(d)].append(
                    str(t) + " " + str(t+p))


Acdt = {}
for c in courses:
    Acdt[str(c)] = {}
    for d in days:
        Acdt[str(c)][str(d)] = {}
        for t in time_slots[str(float(c.getDuration()))][str(d)]:
            Acdt[str(c)][str(d)][str(t)] = Bool(
                str(c) + "+" + str(d) + "+" + str(t))

# print(Acdt)

Acndt = {}
for c in courses:
    Acndt[str(c)] = {}
    for n in range(c.getNoSlots()):
        Acndt[str(c)][str(n)] = {}
        for d in days:
            Acndt[str(c)][str(n)][str(d)] = {}
            for t in time_slots[str(float(c.getDuration()))][str(d)]:
                Acndt[str(c)][str(n)][str(d)][str(t)] = Bool(
                    str(c) + "+" + str(n) + "+" + str(d) + "+" + str(t))
# print(Acndt)

Acrdt = {}
for c in courses:
    Acrdt[str(c)] = {}
    for r in classrooms:
        if r.getSize() in c.getClassSize():
            Acrdt[str(c)][str(r)] = {}
            for d in days:
                Acrdt[str(c)][str(r)][str(d)] = {}
                for t in time_slots[str(float(c.getDuration()))][str(d)]:
                    Acrdt[str(c)][str(r)][str(d)][str(t)] = Bool(
                        str(c) + "+" + str(r) + "+" + str(d) + "+" + str(t))
# print(Acrdt)

Acpdt = {}
for c in courses:
    Acpdt[str(c)] = {}
    for p in professors:
        if p in c.getProf():
            Acpdt[str(c)][str(p)] = {}
            for d in days:
                Acpdt[str(c)][str(p)][str(d)] = {}
                for t in time_slots[str(float(c.getDuration()))][str(d)]:
                    Acpdt[str(c)][str(p)][str(d)][str(t)] = Bool(
                        str(c) + "+" + str(p) + "+" + str(d) + "+" + str(t))

# print(Acpdt[str(courses[1])])

Acbdt = {}
for c in courses:
    Acbdt[str(c)] = {}
    for b in batches:
        if b in c.getBatch():
            Acbdt[str(c)][str(b)] = {}
            for d in days:
                Acbdt[str(c)][str(b)][str(d)] = {}
                for t in time_slots[str(float(c.getDuration()))][str(d)]:
                    Acbdt[str(c)][str(b)][str(d)][str(t)] = Bool(
                        str(c) + "+" + str(b) + "+" + str(d) + "+" + str(t))

# print(Acbdt)

# Constraint
#
# All classes scheduled same number of times as required.

# 1
# All classes scheduled at least as many required.

const1 = []
for c in courses:
    temp = []
    for n in range(c.getNoSlots()):
        temp2 = []
        for d in days:
            for t in time_slots[str(float(c.getDuration()))][str(d)]:
                temp2.append(Acndt[str(c)][str(n)][str(d)][str(t)])
        temp.append(Or(temp2))
    const1.append(And(temp))
all_courses_atleast_once = And(const1)

# 2
# All classes scheduled at most as many required.

const2 = []
for c in [courses[0]]:
    temp = []
    for n in range(c.getNoSlots()):
        temp2 = []
        for d in days:
            for t in time_slots[str(float(c.getDuration()))][str(d)]:
                temp2.append(Acndt[str(c)][str(n)][str(d)][str(t)])

        temp3 = []
        for v1 in range(len(temp2)):
            for v2 in range(v1+1, len(temp2)):
                temp3.append(And(temp2[v1], temp2[v2]))
        temp.append(Not(Or(temp3)))
    const2.append(And(temp))
all_courses_atmost_once = And(const2)

# 3
# No course has more than one lecture in one day.

const3 = []
for d in days:
    temp_courses = []
    for c in courses:
        temp_nt = []
        for n in range(c.getNoSlots()):
            for t in time_slots[str(float(c.getDuration()))][str(d)]:
                temp_nt.append(Acndt[str(c)][str(n)][str(d)][str(t)])
        temp_combi = []
        for t1 in range(len(temp_nt)):
            for t2 in range(t1+1, len(temp_nt)):
                temp_combi.append(And(temp_nt[t1], temp_nt[t2]))
        temp_courses.append(Not(Or(temp_combi)))
    const3.append(And(temp_courses))
all_courses_atmost_once_a_day = And(const3)

# 4
# No classroom has more than one lecture at the same time.


def checkOverlap(t1, t2):
    if t1 == t2:
        # print(t1, t2)
        return True
    else:
        t1 = list(map(float, t1.split()))
        t2 = list(map(float, t2.split()))
        if ((float(t1[0]) < float(t2[1])) or (float(t2[0]) < float(t1[1]))):
            # print(t1, t2)
            return True
        else:
            return False


const4 = []
for c1, r_d_t in Acrdt.items():
    for r1, d_t in r_d_t.items():
        for d, t_val in d_t.items():
            for t1, val in t_val.items():
                temp_c2 = []
                for c2, rooms_d_t in Acrdt.items():
                    if c1 is not c2:
                        if r1 in rooms_d_t.keys():
                            for t2, val2 in rooms_d_t[r1][d].items():
                                if checkOverlap(t1, t2):
                                    temp_c2.append(val2)
                const4.append(Implies(val, Not(Or(temp_c2))))

not_more_than_1_courses_in_classroom = And(const4)

# 5
# No professors can have more than one lecture

const5 = []
for c1, p_d_t in Acpdt.items():
    for p1, d_t in p_d_t.items():
        for d, t_val in d_t.items():
            for t1, val in t_val.items():
                temp_c2 = []
                for c2, profs_d_t in Acpdt.items():
                    if c1 is not c2:
                        if p1 in profs_d_t.keys():
                            for t2, val2 in profs_d_t[p1][d].items():
                                if checkOverlap(t1, t2):
                                    temp_c2.append(val2)
                const5.append(Implies(val, Not(Or(temp_c2))))

not_more_than_1_courses_per_prof = And(const5)

# 6
# No student batches can have more than one lecture

const6 = []
for c1, b_d_t in Acbdt.items():
    for b1, d_t in b_d_t.items():
        for d, t_val in d_t.items():
            for t1, val in t_val.items():
                temp_c2 = []
                for c2, batch_d_t in Acbdt.items():
                    if c1 is not c2:
                        if b1 in batch_d_t.keys():
                            for t2, val2 in batch_d_t[b1][d].items():
                                if checkOverlap(t1, t2):
                                    temp_c2.append(val2)
                const6.append(Implies(val, Not(Or(temp_c2))))

not_more_than_1_courses_per_batch = And(const6)

# Validation Checks
# Linking all variables
#
# Linking Acndt and Acdt.
temp_courses = []
for c in courses:
    temp_days = []
    for d in days:
        temp_t = []
        for t in time_slots[str(float(c.getDuration()))][str(d)]:
            temp_num = []
            for n in range(c.getNoSlots()):
                temp_num.append(Acndt[str(c)][str(n)][str(d)][str(t)])

            # p --> q
            temp_t.append(Implies(Or(temp_num), Acdt[str(c)][str(d)][str(t)]))
            temp_t.append(
                Implies(Not(Or(temp_num)), Not(Acdt[str(c)][str(d)][str(t)])))      # not p --> not q
        temp_days.append(And(temp_t))
    temp_courses.append(And(temp_days))
val_Acndt_Acdt = And(temp_courses)


# Linking Acrdt and Acdt
temp_courses = []
for c in courses:
    temp_days = []
    for d in days:
        temp_t = []
        for t in time_slots[str(float(c.getDuration()))][str(d)]:
            temp_rooms = []
            for r in classrooms:
                if r.getSize() in c.getClassSize():
                    temp_rooms.append(Acrdt[str(c)][str(r)][str(d)][str(t)])
            temp_t.append(
                Implies(Or(temp_rooms), Acdt[str(c)][str(d)][str(t)]))
            temp_t.append(
                Implies(Not(Or(temp_rooms)), Not(Acdt[str(c)][str(d)][str(t)])))
        temp_days.append(And(temp_t))
    temp_courses.append(And(temp_days))
val_Acrdt_Acdt = And(temp_courses)


# Linking Acpdt and Acdt
temp = []
temp2 = []
for c in courses:
    for d in days:
        for t in time_slots[str(float(c.getDuration()))][str(d)]:
            temp_prof = []
            for p in professors:
                if p in c.getProf():
                    temp_prof.append(Acpdt[str(c)][str(p)][str(d)][str(t)])
            temp.append(Implies(Acdt[str(c)][str(d)][str(t)], And(temp_prof)))
            temp2.append(Implies(Or(temp_prof), Acdt[str(c)][str(d)][str(t)]))

val_Acpdt_Acdt = And(And(temp), And(temp2))


# Linking Acbdt and Acdt
temp = []
temp2 = []
for c in courses:
    temp_days = []
    for d in days:
        temp_t = []
        for t in time_slots[str(float(c.getDuration()))][str(d)]:
            temp_batch = []
            for b in batches:
                if b in c.getBatch():
                    temp_batch.append(Acbdt[str(c)][str(b)][str(d)][str(t)])
            temp.append(Implies(Acdt[str(c)][str(d)][str(t)], And(temp_batch)))
            temp2.append(Implies(Or(temp_batch), Acdt[str(c)][str(d)][str(t)]))

val_Acbdt_Acdt = And(And(temp), And(temp2))


s.add(all_courses_atleast_once)
s.add(all_courses_atmost_once)
s.add(all_courses_atmost_once_a_day)
s.add(not_more_than_1_courses_in_classroom)
s.add(not_more_than_1_courses_per_prof)
s.add(not_more_than_1_courses_per_batch)
s.add(val_Acndt_Acdt)
s.add(val_Acrdt_Acdt)
s.add(val_Acpdt_Acdt)
s.add(val_Acbdt_Acdt)
isSat = s.check()
print(isSat)
if isSat != sat:
    print("There cannot be timetable to satisfy all the constraint")
else:
    assigns = s.model()
    assignments = []
    for i in assigns:
        if assigns[i]:
            temp = str(i)
            assignments.append(temp.split("+"))

    time_table = {}
    tt_days = days
    tt_timings = ["8:30 - 9:00",
                  "9:00 - 9:30",
                  "9:30 - 10:00",
                  "10:00 - 10:30",
                  "10:30 - 11:00",
                  "11:00 - 11:30",
                  "11:30 - 12:00",
                  "12:00 - 12:30",
                  "14:00 - 14:30",
                  "14:30 - 15:00",
                  "15:00 - 15:30",
                  "15:30 - 16:00",
                  "16:00 - 16:30",
                  "16:30 - 17:00",
                  "17:00 - 17:30",
                  "17:30 - 18:00"]

    tt_classrooms = []
    for r in classrooms:
        tt_classrooms.append(r.getName())

    for tt_d in tt_days:
        time_table[str(tt_d)] = {}
        for tt_time in tt_timings:
            time_table[str(tt_d)][str(tt_time)] = {}
            for r in tt_classrooms:
                time_table[str(tt_d)][str(tt_time)][str(r)] = " "

    only_classrooms = []
    for a in assignments:
        for r in classrooms:
            if str(r) in a:
                only_classrooms.append(a)
    print("Assignments", only_classrooms)

    time_avail_splitted = {}
    time_avail_splitted["s"] = []
    time_avail_splitted["e"] = []
    for t in time_slots["0.5"]["Monday"]:
        time_avail_splitted["s"].append(t.split()[0])
        time_avail_splitted["e"].append(t.split()[1])

    for a in only_classrooms:
        temp = a[3].split()
        # temp[0] start, temp[1] end
        starting = time_avail_splitted["s"].index(temp[0])
        ending = time_avail_splitted["e"].index(temp[1])
        for c in courses:
            for r in classrooms:
                if ((str(r) in a) and (str(c) in a)):
                    for i in range(starting, ending+1):
                        time_table[str(a[2])][str(tt_timings[i])
                                              ][str(r.getName())] = c.getName()

    print("Time Table",time_table)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('TimeTable.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "IIT Goa")
    worksheet.write(1, 0, "Time Table")
    worksheet.write(2, 0, "Days")
    worksheet.write(2, 1, "Classrooms")
    for col in range(len(tt_timings)):
        worksheet.write(2, 2+col, tt_timings[col])

    i = 0
    for d in tt_days:
        worksheet.write(3+i, 0, d)
        for r in tt_classrooms:
            worksheet.write(3+i, 1, r)
            i += 1

    for d in range(len(tt_days)):
        for r in range(len(tt_classrooms)):
            for tt_time in range(len(tt_timings)):
                worksheet.write(d*len(tt_classrooms) + r + 3, tt_time + 2, time_table[str(
                        tt_days[d])][str(tt_timings[tt_time])][str(tt_classrooms[r])])
                

    workbook.close()
