from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Tournament, League, Cup, Participation, Match, PlayerParticipation

class ParticipationAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    def delete_model(self, request, obj):
        raise ValidationError("No se permite eliminar un registro de participación directamente.")

    def delete_queryset(self, request, queryset):
        raise ValidationError("No se permite eliminar registros de participación directamente.")

admin.site.register([Tournament, League, Cup, Match, PlayerParticipation])
admin.site.register(Participation, ParticipationAdmin)



