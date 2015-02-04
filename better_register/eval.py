# coding: utf-8
import course_search.models as m
import course_search.data_entry as de
from data import eval
y = [i.__unicode__() for i in m.Course.objects.all()]
for i in eval:
    c,n,ins,r =i
    de.create_eval(ins,c,n,r)
    
