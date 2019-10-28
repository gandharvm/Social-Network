from django import forms


class PlanForm(forms.Form):
    choices = (('silver', 'Silver(50/pm)'), (
        'gold', 'Gold(100/pm)'), ('platinum', 'Platinum(150/pm)'),)
    plan = forms.ChoiceField(choices=choices)
