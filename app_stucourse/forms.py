from django import forms
from .models import Enrollment

class DateInput(forms.DateInput):
    input_type = 'date'

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date']
        widgets = {
            'enrollment_date': DateInput(),
        }
