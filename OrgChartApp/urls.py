from django.urls import path, include
from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls), name="view_sets"),
    path(r"channels", views.ChannelsView.as_view()),
    path(r"consolidated-primary", views.ConsolidatedPrimaryView.as_view()),
    path(r"consolidated-secondary", views.ConsolidatedSecondaryView.as_view()),
    path(r"standalone", views.StandAloneView.as_view()),
    path(r"users", views.UsersView.as_view())
]
