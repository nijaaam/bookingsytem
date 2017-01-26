from django import forms
from bksys.models import *
import datetime

class DateTimeForm(forms.Form):
    date = forms.DateField(input_formats=[
        '%Y-%m-%d',      
        '%m/%d/%Y',
         '%m/%d/%y',
         '%d-%m-%Y',
    ])
    time = forms.TimeField(input_formats=['%H:%M'])

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            self.cleaned_data['date'] = datetime.date.today()
            return datetime.date.today()
        return date

    def clean_time(self):
        time = self.cleaned_data['time']
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        if time < datetime.time(hour,minute,0):
            return datetime.time(hour,minute,0)
        return time
            
class SignUpForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()

    def save(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        return users.objects.create_user(name,email)
