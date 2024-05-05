from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Tasks(models.Model):
    task_id=models.AutoField(primary_key=True)
    task_name=models.CharField(max_length=200)
    task_description=models.CharField(max_length=300)
    task_start_date=models.DateField()
    task_end_date=models.DateField()
    task_status=models.CharField(max_length=20)
    board_id=models.ForeignKey('Dashboards', on_delete=models.CASCADE, null=True)

    def __str__(self):                                                                                                                                                     
        return self.task_name

# class Users(models.Model):
#     user_id=models.AutoField(primary_key=True)
#     user_username=models.CharField(max_length=60)
#     user_password=models.CharField(max_length=40)
#     user_role=models.CharField(max_length=20)
#     user_email=models.EmailField()
#
#     def __str__(self):
#         return self.user_username

class User_tasks(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    task_id=models.ForeignKey('Tasks',on_delete=models.CASCADE)

    def __int__(self):
        return self.user_id
class Labels(models.Model):
    label_id=models.AutoField(primary_key=True)
    label_name=models.CharField(max_length=200)

    def __str__(self):
        return self.label_name

class Label_tasks(models.Model):
    label_id=models.ForeignKey('Labels',on_delete=models.CASCADE)
    task_id=models.ForeignKey('Tasks',on_delete=models.CASCADE)

    def __int__(self):
        return self.task_id

class Dashboards(models.Model):
    dashboard_id=models.AutoField(primary_key=True)
    dashboard_name=models.CharField(max_length=200)
    dashboard_admin_id=models.ForeignKey(User,on_delete=models.DO_NOTHING,db_column='admin_id')

    def __str__(self):
        return self.dashboard_name

class Users_Dashboards(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    dashboard_id=models.ForeignKey('Dashboards',on_delete=models.CASCADE)

    def __int__(self):
        return self.user_id