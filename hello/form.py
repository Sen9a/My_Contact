from django import forms
import datetime
from .models import Contact
from widgets.image_field_widget import ImageFieldWidget
from widgets.datetime_widget import DateWidget


class My_add_data_form(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {'image': ImageFieldWidget, 'date': DateWidget}

    def clean_date(self):
        data = self.cleaned_data['date']
        instanse = (datetime.date.today() - data).days/364.0
        if instanse > 120:
            raise forms.ValidationError('You already dead now')
        if instanse <= 0:
            raise forms.ValidationError('You not born yet')
        return data
