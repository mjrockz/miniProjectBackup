from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    #studentpath
    # path('student/', views.getStudent, name="student info"),
    path('student/', views.studentsInDept, name="student info"),
    
    

    #teacherpath
    # path('teacher/', views.getTeacher, name="teacher info"),
    path('teacher/', views.teachersInDept, name="teacher info"),
    path('teacher/mystudents/', views.studentsInClass, name="studentsInClass"),
    path('teacher/rulebook/', views.rules, name="rules")
]

