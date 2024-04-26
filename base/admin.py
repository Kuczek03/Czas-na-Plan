from django.contrib import admin

# Register your models here.
from .models import Labels, Label_tasks, Tasks, Users, User_tasks

admin.site.register(Labels)
admin.site.register(Label_tasks)
admin.site.register(Tasks)
admin.site.register(Users)
admin.site.register(User_tasks)
