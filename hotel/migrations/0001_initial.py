# Generated by Django 3.1.7 on 2021-03-14 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField(verbose_name='Дата въезда')),
                ('departure_date', models.DateField(verbose_name='Дата выезда')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=75, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=75, null=True, verbose_name='Отчество')),
                ('last_name', models.CharField(max_length=75, verbose_name='Фамилия')),
                ('foreigner', models.BooleanField(verbose_name='Иностранец')),
                ('country', models.CharField(max_length=75, verbose_name='Родная страна')),
                ('passport', models.BigIntegerField(verbose_name='Паспорт')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('Ж', 'female'), ('М', 'male')], max_length=20, verbose_name='Пол')),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.booking')),
            ],
        ),
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, verbose_name='Тип')),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена в сутки')),
                ('persons', models.IntegerField(verbose_name='Количество человек')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('rooms_qty', models.IntegerField(verbose_name='Количество комнат')),
                ('desc', models.TextField(verbose_name='Описание комнат')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Номер')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('status', models.CharField(choices=[('Занят', 'Занят'), ('Свободен', 'Свободен')], max_length=20, verbose_name='Статус номера')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.roomcategory', verbose_name='Тип номера')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField(verbose_name='Дата въезда')),
                ('departure_date', models.DateField(verbose_name='Дата выезда')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.client')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.room'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]