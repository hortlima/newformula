from django.contrib import admin
from django.utils.html import format_html
from .models import Equipe, Piloto, Corrida, Resultado

admin.site.site_header = "Fórmula Betting Admin"
admin.site.site_title = "Fórmula Betting"
admin.site.index_title = "Painel de Gerenciamento"

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor_badge', 'logo_preview')
    readonly_fields = ('logo_preview',)
    search_fields = ('nome',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:50px; border-radius:6px;" />', obj.logo)
        return "-"
    logo_preview.short_description = "Prévia da Logo"

    def cor_badge(self, obj):
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:8px;">{}</span>',
            obj.cor,
            obj.cor
        )
    cor_badge.short_description = "Cor"

@admin.register(Piloto)
class PilotoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero', 'equipe_colored')
    list_filter = ('equipe',)
    search_fields = ('nome', 'numero')

    def equipe_colored(self, obj):
        cor = obj.equipe.cor if obj.equipe and obj.equipe.cor else "#ccc"
        return format_html('<span style="color:{};">{}</span>', cor, obj.equipe.nome)
    equipe_colored.short_description = "Equipe"

class ResultadoInline(admin.TabularInline):
    model = Resultado
    extra = 0
    autocomplete_fields = ['piloto']
    show_change_link = True

@admin.register(Corrida)
class CorridaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data')
    ordering = ('data',)
    inlines = [ResultadoInline]
    search_fields = ('nome',)

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('corrida', 'piloto', 'posicao', 'pontuacao')
    list_filter = ('corrida', 'piloto__equipe')
    search_fields = ('piloto__nome', 'corrida__nome')
    autocomplete_fields = ['piloto', 'corrida']
