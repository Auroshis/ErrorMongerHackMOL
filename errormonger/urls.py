from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views #django's builtin solution for signup, login, logout
from core import views

urlpatterns = [
  path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('register/', views.register, name="register"),
    # URL for search option
    path('problems/search/', views.search, name = 'search'),
    # URL for deleting a problem - when you click on delete in problem section
    path('problems/<int:pk>/', views.delete_problem, name='delete_problem'),
    # URL for deleting a solution - when you click on delete in solution section
    path('delete_solution/<int:pk>/', views.delete_solution, name='delete_solution'),
    # URL for getting list of solutions to a specific problem 
    path('solution_list/<int:pk>/', views.solution_list, name='solution_list'),
    # URL for getting list of most recent problems
    path('recent_problem_list/', views.recent_problem_list , name='recent_problem_list'),
    # URL for getting the list of most freuent problems 
    path('common_problem_list/', views.common_problem_list, name='common_problem_list'),
    # URL for adding new problems
    path('add_problem/', views.add_problem, name='add_problem'),
    # URL for fetching add new problem page
    path('new_problem/', views.new_problem, name='new_problem'),
    # URL for landing to add solution page
    path('new_solution/<int:pk>/', views.new_solution, name='new_solution'),
    # URL for adding new solution 
    path('add_solution/', views.add_solution, name='add_solution'),
]