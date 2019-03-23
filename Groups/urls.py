from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns =[
    path('ViewGroups/', views.Groups),
    path('CreateGroup/', views.CreateGroup),
    path('ViewGroups/UserGroup/', views.UserGroup),
    path('ViewGroups/UserGroup/AddMember/', views.AddMember),

]