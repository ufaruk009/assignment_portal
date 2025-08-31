from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Assignment(models.Model):
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'lecturer'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    submitted_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} → {self.assignment.title}"
