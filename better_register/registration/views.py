from django.shortcuts import render
from django.core import serializers
import models as m
# Create your views here.


def index(request):
    return render(request, 'search.html')


def get_qury_dict(request):
    if request.method == 'GET':
        return request.GET
    elif request.method == 'POST':
        return request.POST


def serialize(obj):
    return obj.__unicode__()


def serailize_query(query):
    return map(serialize, query)


def short_render(request, query):
    """
    Since we're returning the same template this weiil cut down on retyping everything.
    :param query:
    :return:
    """
    return render(request, 'results.html', {'results': serailize_query(query)})


def instructor_by_subject(request):
    qd = get_qury_dict(request)
    subject_code = qd['sub_code'].upper()
    offerings = m.Offering.objects.filter(course__subject__code=subject_code)
    instructors = list(set(map(lambda o: "{} {}".format(o.instructor.fname, o.instructor.lname), offerings)))
    return render(request, 'results.html', {'results': instructors})


def instructor_by_score(request):
    qd = get_qury_dict(request)
    rating = float(qd['score'])
    eval_fn = m.Evaluation.objects.avg_ins_ratings
    instructors = m.Instructor.objects.search_by_evaluation(rating, eval_fn)
    return short_render(request, instructors)


def instructor_by_name(request):
    qd = get_qury_dict(request)
    fname = qd['fname']
    lname = qd['lname']

    instructors = m.Instructor.objects.filter(fname=fname, lname=lname)
    return short_render(request, instructors)


def offering_by_score(request):
    qd = get_qury_dict(request)
    score = float(qd['score'])
    eval_fn = m.Evaluation.objects.avg_offering_ratings
    offerings = m.Offering.objects.search_by_evaluation(score, eval_fn)
    return short_render(request, offerings)


def offering_by_subject(request):
    qd = get_qury_dict(request)
    subject_code = qd['sub_code']
    offerings = m.Offering.objects.filter(course__subject__code=subject_code)
    return short_render(request, offerings)


def offering_by_instructor(request):
    qd = get_qury_dict(request)
    fname = qd['fname']
    lname = qd['lname']
    offerings = m.Offering.objects.filter(instructor__fname=fname, instructor__lname=lname)
    return short_render(request, offerings)


def eval_by_score(request):
    qd = get_qury_dict(request)
    score = qd['score']
    evals = m.Evaluation.objects.by_score(score)
    return short_render(request, evals)

def evals_by_instructor(request):
    qd = get_qury_dict(request)
    fname = qd['fname']
    lname = qd['lname']
    offerings = m.Evaluation.objects.filter(instructor__fname=fname, instructor__lname=lname)
    return short_render(request, offerings)








