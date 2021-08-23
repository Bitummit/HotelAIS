from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    GENDER = {
        ('М', 'Мужчина'),
        ('Ж', 'Женщина')
    }
    client_id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=75, verbose_name="Имя")
    patronymic = models.CharField(max_length=75, verbose_name="Отчество", null=True)
    last_name = models.CharField(max_length=75, verbose_name="Фамилия")
    country = models.CharField(max_length=75, verbose_name="Родная страна")
    passport = models.BigIntegerField(verbose_name="Паспорт")
    birthday = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(max_length=20, choices=GENDER, verbose_name="Пол")

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class RoomCategory(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="Тип")
    price_per_day = models.DecimalField(max_digits=7, verbose_name="Цена в сутки", decimal_places=2)
    persons = models.IntegerField(verbose_name="Количество человек")
    image = models.ImageField(verbose_name="Изображение")
    free_rooms = models.IntegerField(verbose_name="Свободные номера", default=0)
    desc = models.TextField(verbose_name="Описание номера")

    def __str__(self):
        return self.category_name


class Room(models.Model):
    STATUS_FREE = 'Свободен'
    STATUS_BUSY = 'Занят'

    ROOM_STATUS = {
        (STATUS_FREE, 'Свободен'),
        (STATUS_BUSY, 'Занят')
    }

    number = models.IntegerField(primary_key=True, unique=True, verbose_name="Номер")
    type = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, verbose_name="Тип номера")
    status = models.CharField(max_length=20, choices=ROOM_STATUS, verbose_name="Статус номера", default=STATUS_FREE)

    def __str__(self):
        return str(self.number)


class Order(models.Model):
    entry_date = models.DateField(verbose_name="Дата въезда")
    departure_date = models.DateField(verbose_name="Дата выезда")
    price = models.DecimalField(max_digits=12, verbose_name="Цена", decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    persons = models.IntegerField(verbose_name='Количество гостей', default=1)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    active = models.BooleanField(default=1)


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=75, verbose_name="Имя", default="")
    patronymic = models.CharField(max_length=75, verbose_name="Отчество", null=True)
    last_name = models.CharField(max_length=75, verbose_name="Фамилия", default="")
    position = models.CharField(max_length=100,  verbose_name="Должность", default="")
    salary = models.DecimalField(max_digits=12, verbose_name="Зарплата", decimal_places=2, default=0)
    passport = models.BigIntegerField(verbose_name="Паспорт", default=0)
    phone = models.CharField(max_length=15, verbose_name='Телефон', default="")


class ClientUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=75, verbose_name="Имя")
    patronymic = models.CharField(max_length=75, verbose_name="Отчество", null=True)
    last_name = models.CharField(max_length=75, verbose_name="Фамилия")
    phone = models.CharField(max_length=15, verbose_name='Телефон')


class Booking(models.Model):
    STATUS_NEW = 'Новый'
    STATUS_CONFIRM = 'Подтвержден'
    STATUS_SETTLING = 'Заселено'

    BOOKING_STATUS = {
        (STATUS_NEW, 'Новый'),
        (STATUS_CONFIRM, 'Подтвержден'),
        (STATUS_SETTLING, 'Заселено'),
    }
    entry_date = models.DateField(verbose_name="Дата въезда")
    departure_date = models.DateField(verbose_name="Дата выезда")
    price = models.DecimalField(max_digits=12, verbose_name="Цена", decimal_places=2)
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, verbose_name="Статус", default=STATUS_NEW)
    persons = models.IntegerField(verbose_name='Количество гостей', default=1)

