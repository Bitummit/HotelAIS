# Generated by Django 3.1.7 on 2021-04-03 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0016_auto_20210403_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Бронь', 'verbose_name_plural': 'Брони'},
        ),
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женщина'), ('М', 'Мужчина')], max_length=20, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('Свободен', 'Свободен'), ('Занят', 'Занят')], default='Свободен', max_length=20, verbose_name='Статус номера'),
        ),
    ]