from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Tasks(models.Model):
    STATUS_CHOICES = [
        ('to do', 'To Do'),
        ('in progress', 'In Progress'),
        ('done', 'Done')
    ]

    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=200)
    task_description = models.CharField(max_length=300)
    task_start_date = models.DateField()
    task_end_date = models.DateField()
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Done')
    board_id = models.ForeignKey('Dashboards', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.task_end_date < self.task_start_date:
            raise ValidationError({
                'task_end_date': "Data zakończenia zadania nie może być wcześniejsza niż data jego rozpoczęcia."
            })
    def __str__(self):
        return self.task_name

class User_tasks(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.ForeignKey('Tasks', on_delete=models.CASCADE)

    def __int__(self):
        return self.user_id

class Labels(models.Model):
    label_id = models.AutoField(primary_key=True)
    label_name = models.CharField(max_length=200)

    def __str__(self):
        return self.label_name

class Label_tasks(models.Model):
    label_id = models.ForeignKey('Labels', on_delete=models.CASCADE)
    task_id = models.ForeignKey('Tasks', on_delete=models.CASCADE)

    def __int__(self):
        return self.task_id

class Dashboards(models.Model):
    dashboard_id = models.AutoField(primary_key=True)
    dashboard_name = models.CharField(max_length=50, error_messages={'unique': "Ta nazwa tablicy już istnieje. Wybierz inną."})
    dashboard_admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_dashboards', editable=False)
    users = models.ManyToManyField(User, through='Users_Dashboards', related_name='dashboards')

    def __str__(self):
        return f"{self.dashboard_name} - {self.dashboard_admin_id.username}"

class Users_Dashboards(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    dashboard_id = models.ForeignKey(Dashboards, on_delete=models.CASCADE)

    def __int__(self):
        return self.user_id

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    task_description = models.TextField()
    task_start_date = models.DateField()
    task_end_date = models.DateField()
    is_important = models.BooleanField(default=False)