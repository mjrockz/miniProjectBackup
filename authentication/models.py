from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    ktu_id = models.CharField(max_length=12, default="")
    student_profile_pic = models.ImageField(upload_to="templates/student_profile_pic",blank=True)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField()
    ph = models.CharField(max_length=12, default="")
    sem = models.CharField(max_length=2, default="")
    dept = models.CharField(max_length=50, default="")
    points = models.IntegerField(default=0)
    passout_year = models.CharField(max_length=4)
    role = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    instance.student_profile.save()


# Teacher Profile
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile")
    teacher_profile_pic = models.ImageField(upload_to="templates/teacher_profile_pic",blank=True)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField()
    ph = models.CharField(max_length=12)
    sem = models.CharField(max_length=2)
    dept = models.CharField(max_length=50)
    role = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        TeacherProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_teacher_profile(sender, instance, **kwargs):
    instance.teacher_profile.save()

class Document(models.Model):
    file = models.ImageField()