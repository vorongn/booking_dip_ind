from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Hotel, Room, RoomMedia, HotelMedia, Booking, City, Comment


class RoomMediaAdmin(admin.TabularInline):
    fk_name = 'room_id'
    model = RoomMedia


class HotelMediaAdmin(admin.TabularInline):
    fk_name = 'hotel_id'
    model = HotelMedia


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelMediaAdmin, ]

    readonly_fields = ['post_photo',]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'status', 'post_photo', 'created_at', 'rating',  'room_count')
    list_display_links = ('title', )
    order = ['-created_at', 'title']
    list_per_page = 10
    # action = ['set_status', 'set_recomended']
    search_fields = ['title__startswith', ]
    list_filter = ['title', 'location_city']
    save_on_top = True


    @admin.display(description='лого')
    def post_photo(self, hotel: Hotel):
        if hotel.logo_hotel:
            return mark_safe(f"<img src='{hotel.logo_hotel.url}' width=50")
        return 'нет лого'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomMediaAdmin, ]
    list_display = ('title', 'hotel_id', 'room_type',  'status', )
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'hotel_info', 'check_in', 'check_out')

    def hotel_info(self, obj):

        return obj.room.hotel_id if obj.room else None

    hotel_info.short_description = 'Отель'


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'room', 'hotel_info',  'rating', 'created_date', 'status']
    list_filter = ['status', 'created_date', 'rating' ]
    search_fields = ['user', 'text']

    def hotel_info(self, obj):

        return obj.room.hotel_id if obj.room else None

    hotel_info.short_description = 'Отель'