from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
# from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from unidecode import unidecode


CHOISES_TYPE_ROOM = (
    ('1-м', 'одноместный номер'),
    ('2-м 1-к',  'двухместный номер 1 кровать'),
    ('2-м 2-к', 'двухместный номер 2 кровати'),
    ('Люкс 2-м', 'Двухместный люкс'),
    ('3-м', 'Трёхместный'),
                    )

#--------------------------------------------------------
class City(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='город')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        return super(City, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={'city_slug': self.slug})

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

#--------------------------------------------------------

class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class Hotel(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    location_city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='город')
    location_strit = models.CharField(max_length=50, verbose_name='Улица')
    location_building = models.CharField(max_length=20, verbose_name='№ строения')
    short_desc = models.TextField(blank=True, max_length=250, verbose_name='краткое описание')
    description = models.TextField(verbose_name='описание')
    rating = models.IntegerField(verbose_name='рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    logo_hotel = models.ImageField(blank=True, default=None, null=True, upload_to='photos/hotels/logo/', verbose_name='главное фото')
    recomended = models.BooleanField(default=False, verbose_name='рекомендовать')
    status = models.BooleanField(default=False, verbose_name='опубликовать')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        return super(Hotel, self).save(*args, **kwargs)

    def room_count(self):
        return self.room_set.count()

    def gallery(self):
        return self.images.all()

    def get_absolute_url(self):
        return reverse('hotel_detail', kwargs={'hotel_slug': self.slug})

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class HotelMedia(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(blank=True, upload_to='photos/hotels/')


    class Meta:
        verbose_name = 'Фото отеля'
        verbose_name_plural = 'Фото отеля'


class Room(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='отель')
    logo_room = models.ImageField(blank=True, default=None, null=True, upload_to='photos/rooms/logo/',
                                  verbose_name='главное фото номера')
    room_type = models.CharField(max_length=15, blank=False, choices=CHOISES_TYPE_ROOM, verbose_name='тип номера')
    max_guest = models.IntegerField(verbose_name='максимум гостей в номер')
    bads = models.IntegerField(default=False, verbose_name='кроватей')
    baths = models.IntegerField(default=False, verbose_name='санузлов')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена за сутки')
    wifi = models.BooleanField(default=False, verbose_name='бесплатный WIFI')
    parking = models.BooleanField(default=False, verbose_name='парковочное место')

    short_desc = models.TextField(blank=True, max_length=250)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.BooleanField(default=False, verbose_name='опубликовать')


    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        return super(Room, self).save(*args, **kwargs)

    def gallery(self):
        return self.images.all()

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'hotel_slug': self.hotel_id.slug, 'room_slug': self.slug})


    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'


class RoomMedia(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(blank=True, upload_to='photos/rooms/')

    class Meta:
        verbose_name = 'Фото номера'
        verbose_name_plural = 'Фото номера'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='когда бронировали')

    def is_room_available(self):
        # Получаем все бронирования для этого номера
        bookings = Booking.objects.filter(room=self.room)

        for booking in bookings:
            # Если даты бронирования пересекаются с уже существующими бронированиями, то номер недоступен
            if (self.check_in <= booking.check_out) and (self.check_out >= booking.check_in):
                return False

        # Если ни одно бронирование не пересекается с выбранными датами, то номер доступен
        return True

    def __str__(self):
        return self.user.username


    # def delete(self, *args, **kwargs):
    #     # Проверка условий перед удалением
    #
    #     if Booking.:
    #         raise ValidationError('Бронирование не может быть отменено')
    #
    #     super().delete(*args, **kwargs)


    class Meta:
        verbose_name = 'бронь'
        verbose_name_plural = 'брони'


class Comment(models.Model):
    room = models.ForeignKey(Room, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='комментарий')
    rating = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    verbose_name='оценка от 1 до 5')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    status = models.BooleanField(default=True, verbose_name='опубликовать')

    class Meta:

        verbose_name = 'коментарий'
        verbose_name_plural = 'коментарии'