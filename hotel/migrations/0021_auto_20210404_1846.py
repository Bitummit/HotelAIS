# Generated by Django 3.1.7 on 2021-04-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0020_auto_20210404_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Подтверждено', 'Подтверждено'), ('Заселено', 'Заселено'), ('Новый', 'Новый')], default='Новый', max_length=20, verbose_name='Статус'),
        ),
    ]
