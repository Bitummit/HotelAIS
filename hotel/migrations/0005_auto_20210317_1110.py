# Generated by Django 3.1.7 on 2021-03-17 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_auto_20210317_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.CharField(choices=[('Ж', 'Женщина'), ('М', 'Мужчина')], max_length=20, verbose_name='Пол'),
        ),
    ]
