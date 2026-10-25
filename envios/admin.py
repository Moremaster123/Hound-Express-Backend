from django.contrib import admin

from .models import Estatus, Guia, Usuario


class EstatusInline(admin.TabularInline):
    model = Estatus
    extra = 0


@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):
    list_display = ("trackingNumber", "recipient", "origin", "destination", "currentStatus", "updatedAt")
    list_filter = ("currentStatus",)
    search_fields = ("trackingNumber", "recipient")
    inlines = [EstatusInline]


admin.site.register(Usuario)
