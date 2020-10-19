from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('aboutme/', views.index, name='index'),
    path('loginPage/', views.loginPage, name='loginPage'),
    path('register/', views.register, name='register'),
    path('recipe/', views.recipe_view, name='recipe_view'),
    path('selection/', views.selection, name='selection'),
    path('', views.ingredients, name='ingredients'),
    path('dsgvo/', views.dsgvo, name='dsgvo'),
    path('statistics/', views.statistics, name='statistics'),
    path('logout/', views.logoutUser, name='logout'),
]