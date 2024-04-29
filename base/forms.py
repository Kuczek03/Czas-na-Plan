from django import forms
from .models import Tasks

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