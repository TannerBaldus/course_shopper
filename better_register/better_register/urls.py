from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'better_register.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^/','registration.views.index'),
    url(r'^ibsb', 'registration.views.instructor_by_subject'),
    url(r'^ibsc', 'registration.views.instructor_by_score'),
    url(r'^ibn', 'registration.views.instructor_by_name'),

    url(r'^obsc', 'registration.views.offering_by_score'),
    url(r'^obsb', 'registration.views.offering_by_subject'),
    url(r'^obi', 'registration.views.offering_by_instructor'),

    url(r'^ebi', 'registration.views.eval_by_instructor'),
    url(r'^ebsc', 'registration.views.eval_by_score'),

)
