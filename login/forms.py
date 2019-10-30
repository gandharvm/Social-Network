from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime


class PlanForm(forms.Form):
    choices = (('silver', 'Silver(50/pm)'), (
        'gold', 'Gold(100/pm)'), ('platinum', 'Platinum(150/pm)'),)
    plan = forms.ChoiceField(choices=choices, required=True)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    date_of_birth = forms.DateField(
        widget=forms.widgets.DateInput(format="%m/%d/%Y"), help_text='Accepted format: mm/dd/YYYY')
    choices = (('casual', 'Casual'), (
        'premium', 'Premium'), ('commercial', 'Commercial'),)
    category = forms.ChoiceField(choices=choices, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth', 'category',
                  'password1', 'password2', )

    def clean_date_of_birth(self):
        date = self.cleaned_data['date_of_birth']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date
