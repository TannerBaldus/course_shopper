from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'registration.views.home'),
    url(r'^ibsb', 'registration.views.instructor_by_subject'),
    url(r'^ibsc', 'registration.views.instructor_by_score'),
    url(r'^ibn', 'registration.views.instructor_by_name'),

    url(r'^obsc', 'registration.views.offering_by_score'),
    url(r'^obsb', 'registration.views.offering_by_subject'),
    url(r'^obi', 'registration.views.offering_by_instructor'),

    url(r'^ebi', 'registration.views.eval_by_instructor'),
    url(r'^ebsc', 'registration.views.eval_by_score'),
)
