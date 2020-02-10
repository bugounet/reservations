# Generated by Django 2.2.9 on 2020-01-24 20:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='owner',
            field=models.ForeignKey(help_text='User owning this', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='resource',
            field=models.ForeignKey(help_text='Booked resource.', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='resources.Resource', verbose_name='Resource'),
        ),
    ]
