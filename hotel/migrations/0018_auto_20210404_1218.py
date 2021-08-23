# Generated by Django 3.1.7 on 2021-04-04 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0017_auto_20210403_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'verbose_name': 'Бронь', 'verbose_name_plural': 'Брони'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заселение', 'verbose_name_plural': 'Заселения'},
        ),
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Подтвержден', 'Подтвержден'), ('Новый', 'Новый')], default='Новый', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.CharField(choices=[('М', 'Мужчина'), ('Ж', 'Женщина')], max_length=20, verbose_name='Пол'),
        ),
    ]
