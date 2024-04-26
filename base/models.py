from django.db import models

# Create your models here.
class Tasks(models.Model):
    task_id=models.AutoField(primary_key=True)
    task_name=models.CharField(max_length=200)
    task_description=models.CharField(max_length=300)
    task_start_date=models.DateField()
    task_end_date=models.DateField()
    task_status=models.CharField(max_length=20)

    def __str__(self):
        return self.task_name

class Users(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_username=models.CharField(max_length=60)
    user_password=models.CharField(max_length=40)
    user_role=models.CharField(max_length=20)
    user_email=models.EmailField()

    def __str__(self):
        return self.user_username

class User_tasks(models.Model):
    user_id=models.ForeignKey('Users',on_delete=models.CASCADE)
    task_id=models.ForeignKey('Tasks',on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id + ":"+ self.task_id
class Labels(models.Model):
    label_id=models.AutoField(primary_key=True)
    label_name=models.CharField(max_length=200)

    def __str__(self):
        return self.label_name

class Label_tasks(models.Model):
    label_id=models.ForeignKey('Labels',on_delete=models.CASCADE)
    task_id=models.ForeignKey('Tasks',on_delete=models.CASCADE)

    def __str__(self):
        return self.task_id + ":" + self.label_id


