from django.urls import path
from . import views

urlpatterns =[
    path('index/',views.index, name='index'),
    path('Logout/', views.logout),
    path('Login/', views.login),
    path('CreateGroup/', views.CreateGroup, name='CreateGroup'),
    path('ViewGroups/UserGroup/AddMember/', views.AddMember),
    path('ViewGroups/UserGroup/AddBill/', views.AddBill),
    path('ViewGroups/UserGroup/', views.UserGroup,name='UserGroup'),
]