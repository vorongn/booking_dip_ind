from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template import context
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, \
    DetailView, FormView, CreateView, UpdateView
from .forms import AddHotelForm, AddRoomForm, BookingForm, CommentForm

from .models import Hotel, Room, HotelMedia, RoomMedia, City, Booking

from django.views.decorators.http import require_POST


def index(request):
    hotels = Hotel.published.all()

    data = {
        'title': 'Главная',
        'hotels': hotels,
        'cat_selected': 0,
    }
    return render(request, 'hotels/index.html', context=data)


def show_category(request, city_slug):
    category = get_object_or_404(City, slug=city_slug)
    hotels = Hotel.objects.filter(location_city=category.pk)
    data = {

        'title': f'Отели города: {category.title}',
        'hotels': hotels,
        'cat_selected': category.pk,
    }
    return render(request, 'hotels/index.html', context=data)


class HotelsHome(TemplateView):
    template_name = 'hotels/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        return context


class AddHotel(LoginRequiredMixin, CreateView):
    form_class = AddHotelForm
    # model = Hotel
    # fields = '__all__'
    template_name = 'hotels/add_hotel.html'
    # success_url = reverse_lazy('home')
    extra_context = {

        'title': 'Добавить отель',
    }

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdateHotel(UpdateView):
    model = Hotel
    fields = ['title', 'logo_hotel', 'short_desc', 'description',
              'rating', 'location_city', 'location_strit',
              'location_building', 'recomended', ]
    template_name = 'hotels/add_hotel.html'
    success_url = reverse_lazy('home')
    extra_context = {

        'title': 'Редактировать отель',
    }


# -------------------------------------------------------------------
class AddRoom(LoginRequiredMixin, CreateView):
    form_class = AddRoomForm
    template_name = 'hotels/add_room.html'
    # success_url = reverse_lazy('home')
    extra_context = {

        'title': 'Добавить номер',
    }

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdateRoom(UpdateView):
    model = Room
    fields = ['title', 'hotel_id', 'room_type', 'price_per_night', 'short_desc', 'description', 'status']
    template_name = 'hotels/add_room.html'
    success_url = reverse_lazy('home')
    extra_context = {

        'title': 'Редактировать номер',
    }





class HotelsList(ListView):
    city = City.objects.all()
    # model = Hotel
    title = 'Отели'
    # hotels = Hotel.objects.filter(status=True)
    template_name = 'hotels/hotels_list.html'
    context_object_name = 'hotels'
    paginate_by = 6

    extra_context = {
        # 'hotels': hotels,

        'title': title,
        'paginate_by': paginate_by,
        'city_select': 0,
    }

    def get_queryset(self):
        return Hotel.published.all()


def hotel_detail(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    rooms = Room.published.filter(hotel_id=hotel.pk)
    photos = HotelMedia.objects.filter(hotel_id=hotel.pk)

    date = {
        'title': hotel.title,
        'hotel': hotel,
        'rooms': rooms,
        'photos': photos,
    }

    return render(request, 'hotels/hotel_detail.html', date)


# @login_required(login_url='/users/login/')
def room_detail(request, hotel_slug, room_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    room = get_object_or_404(Room, slug=room_slug)
    photos = RoomMedia.objects.filter(room_id=room.pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()
            return render(request, 'hotels/book_room.html', {'room': room, 'hotel': hotel})
    else:
        form = BookingForm()

    if request.method == 'POST':
        form3 = CommentForm(request.POST)
        if form3.is_valid():
            comment = form3.save(commit=False)
            comment.room = room
            comment.author = request.user
            comment.save()
            return redirect('room_detail', hotel_slug, room_slug)
    else:
        form3 = CommentForm()

    date = {
        'room': room,
        'hotel': hotel,
        'title': room.title,
        'room_type': room.room_type,
        'price_per_night': room.price_per_night,
        'description': room.description,
        'created_at': room.created_at,
        'updated_at': room.updated_at,
        'photos': photos,

        'form': form,
        'form3': form3,

    }


    return render(request, 'hotels/room_detail.html', date)


def room_detail_book(request, room, hotel, user):
    title = 'Успешно забронировали номер'
    # user = get_object_or_404(User, slug=hotel.pk)
    hotel = get_object_or_404(Hotel, slug=hotel.pk)
    room = get_object_or_404(Room, slug=room.pk)

    date = {
        'title': title,
        'hotel': hotel,
        'room': room,
   }

    return render(request, 'hotels/book_room.html', date)


def get_my_book(request):
    book = Booking.objects.filter(user=request.user.pk)
    date = {
        'book': book,

    }
    return render(request, 'hotels/my_book.html', date)

# def available_rooms(request):
#     rooms = Room.objects.filter(is_booked=False)
#     return render(request, 'available_rooms.html', {'rooms': rooms})


# def book_room(request, room_id):
#     room = Room.objects.get(id=room_id)
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.room = room
#             booking.save()
#             return redirect('success_page')  # Перенаправление на страницу успеха
#     else:
#         form = BookingForm()
#     return render(request, 'hotels/book_room.html', {'form': form, 'room': room})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')



# @login_required(login_url='/users/login/')
def about(request):
    data = {
        'title': 'О компании',
    }
    return render(request, 'hotels/about.html', context=data)


def contact(request):
    data = {
        'title': 'Обратная связь',

    }
    return render(request, 'hotels/contact.html', context=data)


