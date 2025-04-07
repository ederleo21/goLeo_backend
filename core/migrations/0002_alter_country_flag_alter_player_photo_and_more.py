# Generated by Django 5.0.9 on 2025-04-07 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='flag',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/djretqgrx/image/upload/v1743987498/bandera_hasgfk.jpg', null=True, upload_to='country/', verbose_name='Bandera'),
        ),
        migrations.AlterField(
            model_name='player',
            name='photo',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/djretqgrx/image/upload/v1743987594/player_default_qmzlls.jpg', null=True, upload_to='players/', verbose_name='Foto del jugador'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='https://res.cloudinary.com/djretqgrx/image/upload/v1743987303/user-default_jqhgh3.webp', null=True, upload_to='users/'),
        ),
    ]
