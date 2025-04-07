from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from club_project.utils import phone_regex
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):   
    dni = models.CharField(max_length=10, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='users/', default='https://res.cloudinary.com/djretqgrx/image/upload/v1743987303/user-default_jqhgh3.webp', blank=True, null=True)

    def __str__(self):
        return self.username

class Country(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=30, unique=True)
    code = models.CharField(verbose_name='Código', max_length=3, unique=True)
    flag = models.ImageField(verbose_name='Bandera', upload_to='country/', default='https://res.cloudinary.com/djretqgrx/image/upload/v1743987498/bandera_hasgfk.jpg', blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name

#Clubs models
class Club(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=100, unique=True)
    location = models.CharField(verbose_name='Locacion',max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Pais', related_name='clubs')
    established = models.DateField(verbose_name='Fecha de establecimiento', default=timezone.now)
    logo = models.ImageField(verbose_name='Escudo', upload_to='club/', blank=True, null=True)
    description = models.TextField(verbose_name='Descripcion',blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(verbose_name='Telefono', max_length=10, validators=[phone_regex])
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(verbose_name='Activo', default=True)

    class Meta:
        verbose_name = 'Club'
        verbose_name_plural = 'Clubes'
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name

    def delete(self):
        self.active = False
        self.save()

#Jugadores models
class Position(models.Model):
    description = models.CharField(verbose_name='Posición', max_length=30, unique=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Posición'
        verbose_name_plural = 'Posiciones'
        ordering = ['description']
        indexes = [models.Index(fields=['description'])]

    def __str__(self):
        return self.description

class Player(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name='Club', related_name='players')
    first_name = models.CharField(verbose_name='Nombre', max_length=50)
    last_name = models.CharField(verbose_name='Apellido', max_length=50)
    date_of_birth = models.DateField(verbose_name='Fecha de Nacimiento')
    nationality = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Nacionalidad', related_name='players')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, verbose_name='Posición', related_name='players', null=True)
    photo = models.ImageField(verbose_name='Foto del jugador', upload_to='players/', blank=True, null=True)
    dorsal = models.PositiveIntegerField(verbose_name='Dorsal', default=0)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(verbose_name='Telefono', max_length=10, validators=[phone_regex], blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(verbose_name='Activo', default=True)  

    class Meta:
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'
        ordering = ['last_name', 'first_name']
        indexes = [models.Index(fields=['last_name'])]

    def clean(self):
        super().clean()
        today = timezone.now().date()
        if self.date_of_birth >= today:
            raise ValidationError('La fecha de nacimiento no puede ser hoy ni una fecha futura.')

    def save(self, *args, **kwargs):
        if not self.photo:
            self.photo = 'https://res.cloudinary.com/djretqgrx/image/upload/v1743987594/player_default_qmzlls.jpg'
        super(Player, self).save(*args, **kwargs)

    def delete(self):
        self.active = False
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.club.name})"


class PlayerSkill(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, verbose_name='Jugador', related_name='skills')
    passing = models.PositiveIntegerField(verbose_name='Pase', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    shooting = models.PositiveIntegerField(verbose_name='Tiro', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    dribbling = models.PositiveIntegerField(verbose_name='Regate', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    defense = models.PositiveIntegerField(verbose_name='Defensa', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    physical = models.PositiveIntegerField(verbose_name='Físico', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    speed = models.PositiveIntegerField(verbose_name='Velocidad', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    vision = models.PositiveIntegerField(verbose_name='Visión', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    goalkeeping = models.PositiveIntegerField(verbose_name='Atajada', validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)   
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Habilidad del Jugador'
        verbose_name_plural = 'Habilidades del Jugador'

    def __str__(self):
        return f'Habilidades de {self.player.first_name} {self.player.last_name}'


