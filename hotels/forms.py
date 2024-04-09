import datetime
from datetime import date
from django import forms
from django.forms import SelectDateWidget

from .models import Room, Booking, Hotel, Comment


class AddHotelForm(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = ['title', 'slug', 'location_city', 'location_strit', 'location_building', 'short_desc', 'description', 'rating', 'logo_hotel', 'recomended', 'status']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'from-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
        }

        labels = {'slug': 'URL'}


class AddRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = [
            'title',
            'slug',
            'hotel_id',
            'room_type',
            'price_per_night',
            'short_desc',
            'description',
            'status',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'from-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'room_type': forms.Select(attrs={'class': 'filter-option-inner'})

        }

        labels = {'slug': 'URL'}


class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking
        fields = [
            'check_in',
            'check_out',
        ]
        YEARS = [str(year) for year in range(date.today().year, date.today().year + 1)]
        labels = {
            'check_in': 'Дата заезда',
            'check_out': 'Дата выезда',
        }
        widgets = {
                    # 'check_in': forms.SelectDateWidget(years=range(date.today().year, date.today().year + 2),),
                    # 'check_out': forms.SelectDateWidget(years=range(date.today().year, date.today().year + 2)),
            'check_in': forms.TextInput(attrs={'type': "date", 'name': "date"}),
            'check_out': forms.TextInput(attrs={'type': "date", 'name': "date"})

            }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', 'rating')

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-one__control', 'cols': '100', 'rows': 5, 'resise': 'revert'}),
        }