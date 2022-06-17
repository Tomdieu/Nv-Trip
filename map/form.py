from attr import fields
from django import forms
from .models import UserBookPlace
import re
from django.core.exceptions import ValidationError

class UserBookPlaceForm(forms.ModelForm):
    
    class Meta:
        model = UserBookPlace
        fields = '__all__'
        exclude = ['user','origin','destination','accept']

    def clean_price(self):
        data = self.cleaned_data['price']
        ptn = re.compile(r'^(\d)*$')
        if not ptn.match(data):
            raise ValidationError(["The Price Must Be An Integer"])
        mtn = int(data)
        if mtn < 100:
            raise ValidationError("The Price Must Be >= 100 ")
        return data

    def save(self,commit=False):
        booked = super().save(commit=False)
        if commit:
            booked.save()

        return booked