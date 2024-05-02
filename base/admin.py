from django.contrib import admin

# Register your models here.
from .models import Labels, Label_tasks, Tasks, User_tasks, Dashboards, Users_Dashboards

admin.site.register(Labels)
admin.site.register(Label_tasks)
admin.site.register(Tasks)
#admin.site.register(Users)
admin.site.register(User_tasks)
admin.site.register(Dashboards)
admin.site.register(Users_Dashboards)