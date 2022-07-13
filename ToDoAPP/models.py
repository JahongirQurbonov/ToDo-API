from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    todo_id = models.IntegerField()
    todo = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    schedule_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


