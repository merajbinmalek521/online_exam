from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# -----------------------------------------------------
# 1. User Profile (to differentiate Admin & Candidate)
# -----------------------------------------------------
class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('candidate', 'Candidate'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    roll_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# -----------------------------------------------------
# 2. Exam Model
# -----------------------------------------------------
class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    exam_date = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    total_marks = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams_created')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.exam_name


# -----------------------------------------------------
# 3. Question Model
# -----------------------------------------------------
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    marks = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.question_text[:50]}..."


# -----------------------------------------------------
# 4. Candidate Response Model
# -----------------------------------------------------
class CandidateResponse(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.exam.exam_name}"


# -----------------------------------------------------
# 5. Result Model
# -----------------------------------------------------
class Result(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    grade = models.CharField(max_length=5, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.exam.exam_name} ({self.score})"
