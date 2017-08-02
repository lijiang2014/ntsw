from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index , name = "index" ),
    url(r'^new/$' ,views.new  , name="newissue"),
    url(r'^(?P<issue_id>[0-9]+)/$' ,views.result  , name="getissue"),
]