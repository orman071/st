from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^popular/$', views.popular, name='popular'),
    url(r'^question/(?P<pk>\d+)/$', views.show, name='show'),
    url(r'^ask/$', views.create_question, name='create_question'),
    url(r'^answer/$', views.create_answer),
    url(r'^login/$', views.auth_login),
    url(r'^signup/$', views.signup),
]
