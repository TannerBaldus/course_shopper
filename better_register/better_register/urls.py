from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'better_register.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^dbproj/search','registration.views.index'),
    url(r'^dbproj/ibsb', 'registration.views.instructor_by_subject'),
    url(r'^dbproj/ibsc', 'registration.views.instructor_by_score'),
    url(r'^dbproj/ibn', 'registration.views.instructor_by_name'),

    url(r'^dbproj/obsc', 'registration.views.offering_by_score'),
    url(r'^dbproj/obsb', 'registration.views.offering_by_subject'),
    url(r'^dbproj/obi', 'registration.views.offering_by_instructor'),

    url(r'^dbproj/ebi', 'registration.views.eval_by_instructor'),
    url(r'^dbproj/ebsc', 'registration.views.eval_by_score'),

)
