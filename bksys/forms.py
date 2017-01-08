from django import forms
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

    
