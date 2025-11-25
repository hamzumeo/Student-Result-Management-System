from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    student_class = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.CharField(max_length=100)
    marks = models.FloatField()

    def __str__(self):
        return f'{self.student.name} - {self.subject}'
