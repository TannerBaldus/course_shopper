from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'better_register.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$','course_search.views.index'),
    url(r'^ibsb', 'course_search.views.instructor_by_subject'),
    url(r'^ibsc', 'course_search.views.instructor_by_score'),
    url(r'^ibn', 'course_search.views.instructor_by_name'),

    url(r'^obsc', 'course_search.views.offering_by_score'),
    url(r'^obsb', 'course_search.views.offering_by_subject'),
    url(r'^obi', 'course_search.views.offering_by_instructor'),

    url(r'^ebi', 'course_search.views.eval_by_instructor'),
    url(r'^ebsc', 'course_search.views.eval_by_score'),

)
