from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_movie/$', views.add_movie, name='add_movie'),
    url(r'^filter/', views.show_filtered, name='filter'),
    url(r'^delete/(?P<movie_id>[0-9]+)', views.delete_movie, name='delete'),
    url(r'^mark_watched/(?P<movie_id>[0-9]+)', views.mark_watched, name='mark_watched'),
]
