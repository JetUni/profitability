'''Url routes for the Profit app'''
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/add', views.add_job, name='add_job'),
    path('jobs/<int:pk>', views.edit_job, name='edit_job'),
]
