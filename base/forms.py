from django import forms
from .models import Tasks, Dashboards

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = '__all__'

        labels = {
            'task_id': 'Task ID',
            'task_name': 'Task Name',
            'task_description': 'Task Description',
            'task_start_date': 'Task Start Date',
            'task_end_date': 'Task End Date',
            'task_status': 'Task Status',

        }

        widgets ={

            'task_id': forms.NumberInput(attrs={'placeholder': ''}),
            'task_name': forms.TextInput(attrs={'placeholder': ''}),
            'task_description': forms.TextInput(attrs={'placeholder': ''}),
            'task_start_date' : forms.DateInput(attrs={'placeholder': ''}),
            'task_end_date': forms.DateInput(attrs={'placeholder': ''})
        }
class TabForm(forms.ModelForm):
    class Meta:
        model = Dashboards
        fields = '__all__'
        labels = {
            'dashboard_name': 'Dashboard Name',
        }

        widgets ={
            'dashboard_name': forms.TextInput(attrs={'placeholder': ''})
        }