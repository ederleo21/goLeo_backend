from django.contrib import admin
from .models import Club, Player, Country, Position, PlayerSkill
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
admin.site.register(User)
admin.site.register(Club)
admin.site.register(Player)
admin.site.register(Country)
admin.site.register(Position)
admin.site.register(PlayerSkill)

