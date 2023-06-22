from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from . models import Certificate
from django.db.models import Sum
from django.core import serializers



# Image processing
import pytesseract as tess
from PIL import Image

# Create your views here.
    
@csrf_exempt
def upload(request):

    if request.method == "GET":
        return render(request, 'studentTemplate/uploadFile.html')
       
@csrf_exempt
def fileUpload(request):
    
    points = 0
    # user = request.user
    if request.method == "POST":
        if request.user.student_profile.role == 'student':
            file = request.FILES.get("files")
            print(file)
            # Add certificate to db
            Certificate.objects.create(owner=request.user.student_profile.user, file=file)

            # Get last uploaded file
            filtered_set = Certificate.objects.filter(owner = request.user.student_profile.user)
            last_uploaded = filtered_set.latest('updated_at') # Last uploaded Entry
            img_url = ".{}".format(last_uploaded.file.url)
            img = Image.open(img_url) # Image for processing
            text = tess.image_to_string(img) # Extracted text
            category = ["Internship", "Sports", "Arts"] # Check category

            # check for category
            for each in category:
                # print(request.user.student_profile.name)
                if each.lower() in text.lower():
                    last_uploaded.points = 10
                    last_uploaded.save()
                    aggregate_set = Certificate.objects.filter(owner = last_uploaded.owner)
                    total = aggregate_set.aggregate(Sum('points'))['points__sum']
                    request.user.student_profile.points = total
                    request.user.save()
                    return HttpResponse(total)
                else:
                    print("Word not found")
            return HttpResponse("File added")
            # return redirect(request,"studentTemplate/studentLanding.html")
        
        elif request.user.teacher_profile.role == 'teacher':
            return HttpResponse("You can't upload {}, beacause you are a {}.".format(request.user.username, request.user.teacher_profile.role))

# Frontend APIs
def getStudentCertificate(request):
    if request.method == "GET":
        current_user = request.user.student_profile
        if current_user:
            username = current_user.user.username
            data = []
            filtered_row = Certificate.objects.filter(owner = username)
            print(data)
            return render(request, "studentTemplate/certFolder.html", {'filtered_row':filtered_row})
        
def getCertified(request):
    if request.method == "GET":
        current_user = request.user.student_profile
        if current_user:
            username = current_user.user.username
            data = []
            filtered_row = Certificate.objects.filter(owner = username)
            print(data)
            return render(request, "teacherTemplate/certficateView.html", {'filtered_row':filtered_row})