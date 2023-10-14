from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    firstname = models.CharField(null=False, max_length=255)
    number = models.IntegerField(null=False)
    email = models.EmailField(null=False)
    problems = models.TextField(null=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    PRIORITY_CHOICES = [
        ('Низкий', 'Низкий'),
        ('Средний', 'Средний'),
        ('Высокий', 'Высокий'),

    ]
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Низкий',
    )

    STATUS_CHOICES = [
        ('NEW', 'NEW'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Confirmed', 'Confirmed'),

    ]

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='NEW',
    )
    assigned_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING , related_name='assigned_problems')
    resolved_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING ,related_name='resolved_problems')


    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'

class Action(models.Model):
    action = models.CharField(max_length=255, null=True, default="")
    user_name = models.ForeignKey(Problem, on_delete=models.CASCADE, null=False, related_name='action')

