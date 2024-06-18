from django.db import models
from apps.core.models import Course, User

class Assigment(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Assigment"
        verbose_name_plural = "Assigments"

    def __str__(self):
        return self.name


class Entry(models.Model):
    script = models.TextField()
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assigment = models.ForeignKey(Assigment, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Entry")
        verbose_name_plural = ("Entries")

    def __str__(self):
        return f"Entry of {self.student} for {self.assigment}"