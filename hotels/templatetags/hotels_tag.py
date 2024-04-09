from django import template
from datetime import datetime
import hotels.views as views
from hotels.models import Hotel, Room, City

register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.simple_tag
def get_dopmenu():
    return dopmenu


@register.inclusion_tag('hotels/hotels_detail.html')
def show_hotels(hotel_selected=0):
    hotels = Hotel.objects.all()
    return {'hotels': hotels, 'hotel_selected': hotel_selected}


# @register.inclusion_tag('hotels/list_city.html')
# def show_cities(city_select=0):
#     cities = City.objects.all()
#     return {'cities': cities, 'city_select': city_select}



@register.inclusion_tag('hotels/list_categories.html')
def show_categories(cat_selected=0):
    cats = City.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}



