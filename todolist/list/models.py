from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = (
        ('IN_PROGRESS', 'Em andamento'),
        ('COMPLETED', 'Concluída'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TaskLog(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100, default='message')

    def __str__(self):
        return self.message
