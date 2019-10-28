from django import forms


class PlanForm(forms.Form):
    choices = (('Silver(50/pm)', 'silver'), ('Gold(100/pm)',
                                             'gold'), ('Platinum(150/pm)', 'platinum'),)
    plan = forms.ChoiceField(choices=choices)
