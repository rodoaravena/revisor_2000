from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from datetime import datetime
import random, string, json
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    rut= models.CharField(max_length= 9, unique = True, db_index=True)
    first_name = models.CharField(max_length= 50, db_index=True)
    last_name = models.CharField(max_length= 50, db_index=True)
    email = models.EmailField(max_length=255, unique=False, db_index=True)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length= 25, db_index=True)
    passworddos = models.CharField(max_length= 25, db_index=True)



    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['username']


    objects = UserManager()

    def __str__(self):
        return self.rut

   
class Course(models.Model):
    def generate_code():
        letters = string.ascii_lowercase
        r =  ''.join(random.choice(letters) for i in range(4))
        return f"{datetime.year}{datetime.month}{r}"
    
    c = generate_code()
    code = models.CharField(primary_key=True, max_length=50, default=c)
    name = models.CharField(max_length=50, default=f"Curso {c}")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = ("Course")
        verbose_name_plural = ("Courses")

    def __str__(self):
        return self.name


class ListCourse(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("ListCourse")
        verbose_name_plural = ("ListCourses")

    def __str__(self):
        return f"{self.student.first_name} in {self.course.name}"
