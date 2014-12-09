# coding: utf-8
from data import  offerings, instructors, locations, courses
from models import Location
import data_entry as de



evals = [
    ('ARCH', 201, 'Steve Engel', 3),
    ('ARCH', 381, 'Shannon Doyle', 4),
    ('CIS', 210, 'Michal Young', 5 ),
    ('CIS', 451, 'Chris Wilson', 5),
    ('FR', 101, 'Constance Dickey', 4),
    ('FR', 201, 'Constance Dickey', 3),
    ('BA', 101, 'Anthony Tridbit', 1),
    ('BA', 215, 'April Haynes', 2),
    ('BI', 211, 'Vince Lombardi', 4),
    ('SPAN', 101, 'Inaki Gonzalo', 3),
    ('SPAN', 201, 'Inaki Gonzalo', 3),
    ('HIST', 121, 'Matt Dennis', 2),
    ('HIST', 201, 'Matt Dennis', 2),
    ('PHYS', 251, 'Eric Torrence', 4),
    ('PHYS', 252, 'Eric Torrence', 4),
    ('MATH', 231, 'Boris Botanvick', 2),
    ('MATH', 315, 'Sasha Pochinski', 3),
    ('ART', 115, 'Tyrras Warren', 2),
    ('ART', 116, 'Tyrras Warren', 4),
    ('CIS', 315, 'Chris Wilson', 5),
    ('CIS', 315, 'Andrezj P', 2)
]

def make_ins():
    for i in instructors:
        de.create_instructor(i)

def make_offer():
    cr = 4.00
    for i in offerings:
        c,n,b,r,d,ins = i
        print b,r
        de.create_offering(c,n,cr,r,b,d,ins)

def make_loc():
    for l in locations:
        Location.objects.create(building=l[0], room=l[1])

def make_c():
    for i in courses:
        c,n,t =i
        print c
        de.create_course(c,n,t)

def make_evals():
    for i in evals:
        c,n,i,mr =i
        de.create_eval(i,c,n,mr)



