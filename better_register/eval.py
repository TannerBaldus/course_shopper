# coding: utf-8
import registration.models as m
import registration.data_entry as de
from data import eval
y = [i.__unicode__() for i in m.Course.objects.all()]
for i in eval:
    c,n,ins,r =i
    de.create_eval(ins,c,n,r)
    
