from django import forms
from .models import Tasks, Dashboards
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['task_name', 'task_description', 'task_start_date', 'task_end_date', 'task_status', 'board_id']
        labels = {
            'task_name': 'Nazwa',
            'task_description': 'Opis',
            'task_start_date': 'Data rozpoczęcia',
            'task_end_date': 'Data zakończenia',
            'task_status': 'Status',
            'board_id': 'Tablica'
        }
        widgets = {
            'task_name': forms.TextInput(attrs={'placeholder': ''}),
            'task_description': forms.TextInput(attrs={'placeholder': ''}),
            'task_start_date': forms.DateInput(attrs={'type': 'date'}),
            'task_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TabForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label='Użytkownicy')

    class Meta:
        model = Dashboards
        fields = ['dashboard_name',]
        labels = {
            'dashboard_name': 'Nazwa tablicy',


        }
        widgets = {
            'dashboard_name': forms.TextInput(attrs={'placeholder': ''}),
        }

class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data