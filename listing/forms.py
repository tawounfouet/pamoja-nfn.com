import json

from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import Listing
# BusinessHours

# class ListingForm(forms.ModelForm):
#     class Meta:
#         model = Listing
#         fields = ['tags', ...] 
#         widgets = {
#             'tags': forms.SelectMultiple(
#                 attrs={'style': 'width: 90%; height: 100px;'}
#             ),
#         }


class ListingForm1(ModelForm):
    class Meta:
        model = Listing
        #fields = '__all__'
        # location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='listings', null=True)

        fields = ['title', 'description', 'category', 'subcategory']



class JSONWidget(forms.Textarea):
    def format_value(self, value):
        if value is None:
            return ""
        return json.dumps(value, indent=2)

from django import forms
import json
from .models import Listing, Location, Category, SubCategory

# class JSONWidget(forms.Textarea):
#     def format_value(self, value):
#         if value is None:
#             return ""
#         return json.dumps(value, indent=2)

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'profile',
            'category',
            'subcategory',
            'type',
            'title',  # Changed from listing_title to title
            'company_name',
            'description',
            'location',
            #'logo',
            #'website_url',
            #'business_hours',
            #'tags'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Changed from listing_title to title
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            # 'business_hours': JSONWidget(attrs={
            #     'class': 'form-control',
            #     'rows': 4
            # }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': True
            }),
        }


# class BusinessHoursForm(forms.ModelForm):
#     class Meta:
#         model = BusinessHours
#         fields = [
#             'monday_open', 'monday_close', 'monday_closed',
#             'tuesday_open', 'tuesday_close', 'tuesday_closed',
#             'wednesday_open', 'wednesday_close', 'wednesday_closed',
#             'thursday_open', 'thursday_close', 'thursday_closed',
#             'friday_open', 'friday_close', 'friday_closed',
#             'saturday_open', 'saturday_close', 'saturday_closed',
#             'sunday_open', 'sunday_close', 'sunday_closed',
#         ]
#         widgets = {
#             'monday_open': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'monday_close': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'tuesday_open': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'tuesday_close': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'wednesday_open': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'wednesday_close': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'thursday_open': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'thursday_close': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'friday_open': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'friday_close': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'saturday_open': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'saturday_close': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'sunday_open': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#             'sunday_close': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
#         for day in days:
#             is_closed = cleaned_data.get(f'{day}_closed')
#             opening = cleaned_data.get(f'{day}_open')
#             closing = cleaned_data.get(f'{day}_close')
            
#             if not is_closed and (not opening or not closing):
#                 raise forms.ValidationError(f"Please specify both opening and closing times for {day} or mark it as closed")
#             if opening and closing and opening >= closing:
#                 raise forms.ValidationError(f"Closing time must be later than opening time for {day}")

# BusinessHoursFormSet = inlineformset_factory(
#     Listing,
#     BusinessHours,
#     form=BusinessHoursForm,
#     can_delete=False,
#     max_num=1,
#     extra=1
# )