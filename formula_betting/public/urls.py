from django.urls import path
from core.views import (
    PublicHomeView, RankingPilotos, RankingEquipes,
    ResultadoCreateView, CorridaListHTMLView,
    CorridaDetailHTMLView, ResultadosPorCorridaView
)

urlpatterns = [
    path('', PublicHomeView.as_view(), name='public_home'),
    path('ranking/pilotos/', RankingPilotos.as_view(), name='ranking_pilotos'),
    path('ranking/equipes/', RankingEquipes.as_view(), name='ranking_equipes'),
    path('resultados/', ResultadoCreateView.as_view(), name='criar_resultado'),
    path('corridas/', CorridaListHTMLView.as_view(), name='lista_corridas'),
    path('corridas-html/<int:pk>/', CorridaDetailHTMLView.as_view(), name='corrida_detail_html'),
    path('corridas/<int:corrida_id>/Resultados/', ResultadosPorCorridaView.as_view(), name='resultados_por_corrida'),
]
