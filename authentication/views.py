from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, auth
from django.core import serializers
from django.contrib.auth import logout

# from backend.upload.models import Certificate

from .models import Document, StudentProfile, TeacherProfile



# Register User
@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        semester = request.POST.get("semester")
        department = request.POST.get("department")
        points = request.POST.get("points")
        passoutYear = request.POST.get("passoutYear")
        role = request.POST.get("role")

        if password == confirmPassword:
            if role == "student":
                User.objects.create_user(username=username, password=password)
                user = User.objects.get(username=username)
                user.student_profile.name = name
                user.student_profile.email = email
                user.student_profile.ph = phone
                user.student_profile.sem = semester
                user.student_profile.dept = department
                user.student_profile.points = points
                user.student_profile.passout_year = passoutYear
                user.student_profile.role = role
                user.teacher_profile.role = "not"
                user.save()
                return HttpResponse("Student added")

            if role == "teacher":
                User.objects.create_user(username=username, password=password)
                user = User.objects.get(username=username)
                user.teacher_profile.name = name
                user.teacher_profile.email = email
                user.teacher_profile.ph = phone
                user.teacher_profile.sem = semester
                user.student_profile.dept = department
                user.teacher_profile.role = role
                user.student_profile.role = "not"
                user.save()
                return HttpResponse("Teacher added")

        else:
            return HttpResponse("Password Mismatch")
        # return HttpResponse(username, password)
    else:
        return HttpResponse("Not POST")

# Login User
@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.teacher_profile.role == "teacher":
                current_user = request.user.teacher_profile
                if current_user:
                    whole = serializers.serialize("json", [current_user.user])
                    user = current_user.user.username
                    dp = current_user.teacher_profile_pic
                    name = current_user.name
                    email = current_user.email
                    phone = current_user.ph
                    semester = current_user.sem
                    department = current_user.dept
                    role = current_user.role
                    data = {
                        "whole": whole,
                        "user": user,
                        "dp": dp,
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "semester": semester,
                        "department": department,
                        "role": role,
                    }
                    return render (request, 'teacherTemplate/base.html', { 'data':data})
        
                return render(request, 'teacherTemplate/base.html', {user: user})  # Redirect to teacher dashboard URL or view
            
            elif user.student_profile.role == "student":
                current_user = StudentProfile.objects.get(user=request.user)
                if current_user:
                    whole = serializers.serialize("json", [current_user.user])
                    user = current_user.user.username
                    name = current_user.name
                    email = current_user.email
                    phone = current_user.ph
                    semester = current_user.sem
                    department = current_user.dept
                    points = current_user.points
                    passoutYear = current_user.passout_year
                    role = current_user.role
                    data = {
                        "whole": whole,
                        "user": user,
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "semester": semester,
                        "department": department,
                        "points": points,
                        "passoutYear": passoutYear,
                        "role": role,
                        "css" : "display: flex; justify-content: center; align-items: center; width: 90%;  height: 90%; border-radius: 50%; background: radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(rgb(108, 105, 255) 10%, rgb(204, 175, 224) 0);"
                    }
                    return render (request, 'studentTemplate/studentLanding.html', {'data': data})
            
                return render(request, 'studentTemplate/studentLanding.html', {user: user})  # Redirect to student dashboard URL or view
            else:
                return render(request, 'login.html', {'error': 'Invalid user role.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})

    else:
        return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return HttpResponse("User logged out")

# Frontend APIs
def getStudent(request):
    if request.method == "GET":
        current_user = StudentProfile.objects.get(user=request.user)
        if current_user:
            whole = serializers.serialize("json", [current_user.user])
            user = current_user.user.username
            name = current_user.name
            email = current_user.email
            phone = current_user.ph
            semester = current_user.sem
            department = current_user.dept
            points = current_user.points
            passoutYear = current_user.passout_year
            role = current_user.role

            data = {
                "whole": whole,
                "user": user,
                "name": name,
                "email": email,
                "phone": phone,
                "semester": semester,
                "department": department,
                "points": points,
                "passoutYear": passoutYear,
                "role": role,
            }
            return render (request, 'student_dashboard.html', data)
        else:
            return HttpResponse("User not logged In")
        
# def home(request):
#     return render(request,'admin_home.html')

def getTeacher(request):
    if request.method == "GET":
        current_user = request.user.teacher_profile
        if current_user:
            whole = serializers.serialize("json", [current_user.user])
            user = current_user.user.username
            name = current_user.name
            email = current_user.email
            phone = current_user.ph
            semester = current_user.sem
            department = current_user.dept
            role = current_user.role

            data = {
                "whole": whole,
                "user": user,
                "name": name,
                "email": email,
                "phone": phone,
                "semester": semester,
                "department": department,
                "role": role,
            }
            return render (request, 'teacher_dashboard.html', data)
        else:
            return HttpResponse("User not logged In")

def studentsInClass(request):
    student_list  = StudentProfile.objects.all()
    return render(request, 'teacherTemplate/mystudents.html', { 'student_list':student_list } )

def teachersInDept(request):
    current_user = request.user.teacher_profile
    if current_user:
        whole = serializers.serialize("json", [current_user.user])
        user = current_user.user.username
        name = current_user.name
        email = current_user.email
        phone = current_user.ph
        semester = current_user.sem
        department = current_user.dept
        role = current_user.role
        data = {
            "whole": whole,
            "user": user,
            "name": name,
            "email": email,
            "phone": phone,
            "semester": semester,
            "department": department,
            "role": role,
        }
        print(data)
        return render (request, 'teacherTemplate/base.html', { 'data':data})
    else:
        return HttpResponse("User not logged In")

def studentsInDept(request):
    current_user = StudentProfile.objects.get(user=request.user)
    if current_user:
        whole = serializers.serialize("json", [current_user.user])
        user = current_user.user.username
        name = current_user.name
        email = current_user.email
        phone = current_user.ph
        semester = current_user.sem
        department = current_user.dept
        points = current_user.points
        passoutYear = current_user.passout_year
        role = current_user.role
        data = {
            "whole": whole,
            "user": user,
            "name": name,
            "email": email,
            "phone": phone,
            "semester": semester,
            "department": department,
            "points": points,
            "passoutYear": passoutYear,
            "role": role,
        }
        return render (request, 'studentTemplate/studentLanding.html', {'data': data})
    else:
        return HttpResponse("User not logged In")
    

def Document_save(request):
    if request.method == "POST":
        if request.user.student_profile.role == 'student':
            file = request.FILES.get("file")
            print(file)
            # Add certificate to db
            Certificate.objects.create(owner=request.user.student_profile.user, file=file)
            return HttpResponse("file added")
    return render (request, "uploadFile.html")

def rules(request):
    return render(request, 'teacherTemplate/rules.html' )


