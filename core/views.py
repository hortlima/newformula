import os
from django.conf import settings
from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from collections import defaultdict
from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.views.generic import TemplateView, DetailView, ListView
from .models import Equipe, Piloto, Corrida, Resultado
from .serializers import (
    EquipeSerializer, PilotoSerializer, CorridaSerializer,
    ResultadoSerializer, ResultadosDetalhadoSerializer
)
from .permissions import IsAdminOrReadOnly


def calcular_ranking_equipes():
    """Calcula ranking de equipes somando pontos de todos os pilotos."""
    equipes = Equipe.objects.all()
    ranking = []

    for equipe in equipes:
        pontos = 0
        vitorias = equipe.vitorias
        pilotos = equipe.pilotos.all()

        for piloto in Pilotos:
            resultados = Pilotos.resultados.all()
            pontos += sum(r.pontuacao() for r in resultados)

        ranking.append({
            'equipe': equipe,
            'pontos': pontos,
            'vitorias': vitorias,
        })

    ranking.sort(key=lambda x: (-x['pontos'], -x['vitorias']))
    return ranking

class PublicHomeView(TemplateView):
    template_name = "public/data_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicione aqui os mesmos dados que você tinha no PublicHomeView
        # ou apenas coloque uma mensagem de boas-vindas simples
        context["titulo"] = "Bem-vindo ao Formula Betting"
        return context

class PublicDataHomeView(TemplateView):
    template_name = "public/dados_completos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        equipes = Equipe.objects.all()
        resultados = Resultado.objects.select_related('piloto', 'piloto__equipe', 'corrida')

        # Inicializa stats por equipe
        equipe_stats = {
            equipe.id: {
                'nome': equipe.nome,
                'logo': equipe.logo if equipe.logo else None,
                'cor': equipe.cor,
                'pontos_corrida': 0,
                'total': 0,
                'vitorias': equipe.vitorias
            } for equipe in equipes
        }

        # Soma pontos por equipe
        for resultado in resultados:
            equipe_id = resultado.piloto.equipe_id
            if equipe_id in equipe_stats:
                equipe_stats[equipe_id]['pontos_corrida'] += resultado.pontuacao()

        for stats in equipe_stats.values():
            stats['total'] = stats['pontos_corrida']

        # Ranking de equipes
        ranking_equipes = sorted(equipe_stats.values(), key=lambda x: (-x['total'], -x['vitorias']))

        # Ranking de pilotos
        pilotos = Piloto.objects.select_related('equipe').prefetch_related('resultados')
        ranking_pilotos = []
        for piloto in pilotos:
            pontos = sum(r.pontuacao() for r in piloto.resultados.all())
            ranking_pilotos.append({
                'nome': piloto.nome,
                'numero': piloto.numero,
                'equipe': piloto.equipe.nome,
                "cor": piloto.equipe.cor,
                'pontos': pontos
            })
        ranking_pilotos.sort(key=lambda x: -x['pontos'])

        # Resultados por corrida
        corridas = Corrida.objects.all().order_by('data')
        resultados_por_corrida = []
        for corrida in corridas:
            resultados_c = Resultado.objects.filter(corrida=corrida).select_related('piloto__equipe').order_by('posicao')
            lista_resultados = []
            for r in resultados_c:
                lista_resultados.append({
                    'posicao': r.posicao,
                    'piloto': r.piloto.nome,
                    'numero': r.piloto.numero,
                    'equipe': r.piloto.equipe.nome,
                    'cor': r.piloto.equipe.cor,
                    'pontuacao': r.pontuacao()
                })
            resultados_por_corrida.append({
                'corrida': corrida.nome,
                'data': corrida.data,
                'resultados': lista_resultados
            })

        context['ranking_equipes'] = ranking_equipes
        context['ranking_pilotos'] = ranking_pilotos
        context['resultados_corridas'] = resultados_por_corrida
        context['titulo'] = "Formula Betting"
        return context


class EquipeDetailView(DetailView):
    model = Equipe
    template_name = 'public/equipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipe = self.object
        pilotos = list(equipe.pilotos.all())
        resultados_raw = Resultado.objects.filter(piloto__in=pilotos).select_related('corrida', 'piloto')

        # Organizar resultados por piloto
        resultados_por_piloto = {
            piloto.id: {
                'nome': piloto.nome,
                'numero': piloto.numero,
                'resultados': [],
                'pontos': 0,
                'vitorias': 0
            } for piloto in pilotos
        }

        # Briga interna
        brigas = {}
        if len(pilotos) == 2:
            brigas = {
                f"{pilotos[0].nome} > {pilotos[1].nome}": 0,
                f"{pilotos[1].nome} > {pilotos[0].nome}": 0
            }

        for corrida in Corrida.objects.all().order_by('data'):
            corrida_resultados = list(resultados_raw.filter(corrida=corrida).order_by('posicao'))
            if len(corrida_resultados) == 2:
                p1, p2 = corrida_resultados
                if p1.posicao < p2.posicao:
                    brigas[f"{p1.piloto.nome} > {p2.piloto.nome}"] += 1
                elif p2.posicao < p1.posicao:
                    brigas[f"{p2.piloto.nome} > {p1.piloto.nome}"] += 1
            for r in corrida_resultados:
                p = resultados_por_piloto[r.piloto.id]
                p['resultados'].append({
                    'corrida': r.corrida.nome,
                    'data': r.corrida.data,
                    'posicao': r.posicao,
                    'pontos': r.pontuacao()
                })
                p['pontos'] += r.pontuacao()
                if r.posicao == 1:
                    p['vitorias'] += 1

        ranking_pilotos = sorted(resultados_por_piloto.values(), key=lambda x: -x['pontos'])

        context.update({
            'equipe': equipe,
            'ranking_pilotos': ranking_pilotos,
            'brigas': brigas
        })
        return context

class RankingPilotos(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pilotos = Piloto.objects.prefetch_related('resultados', 'equipe')
        data = []

        for piloto in pilotos:
            pontos = sum(r.pontuacao() for r in piloto.resultados.all())
            data.append({
                "id": piloto.id,
                "nome": piloto.nome,
                "numero": piloto.numero,
                "equipe": piloto.equipe.nome,
                "pontuacao": pontos
            })

        data.sort(key=lambda x: -x['pontuacao'])
        return Response(data)

class RankingPilotos(TemplateView):
    template_name = 'ranking/pilotos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pilotos = Piloto.objects.all()
        ranking = []

        for piloto in pilotos:
            total = sum([r.pontuacao() for r in piloto.resultados.all()])
            ranking.append({
                'piloto': piloto,
                'total_pontos': total
            })

        context['ranking'] = sorted(ranking, key=lambda x: x['total_pontos'], reverse=True)
        return context

class RankingEquipes(TemplateView):
    template_name = "ranking/equipes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipes = Equipe.objects.all()
        resultados = Resultado.objects.select_related('piloto', 'piloto__equipe')

        equipe_stats = {
            equipe.id: {
                'nome': equipe.nome,
                'logo': equipe.logo if equipe.logo else None,
                'cor': equipe.cor,
                'pontos': 0,
                'vitorias': equipe.vitorias,
            } for equipe in equipes
        }

        for resultado in resultados:
            equipe_id = resultado.piloto.equipe_id
            if equipe_id in equipe_stats:
                equipe_stats[equipe_id]['pontos'] += resultado.pontuacao()

        ranking = sorted(equipe_stats.values(), key=lambda x: (-x['pontos'], -x['vitorias']))

        context['ranking_equipes'] = ranking
        context['titulo'] = "Ranking de Equipes"
        return context

class EquipeViewSet(viewsets.ModelViewSet):
    queryset = Equipe.objects.all()
    serializer_class = EquipeSerializer
    permission_classes = [IsAdminOrReadOnly]


class PilotoViewSet(viewsets.ModelViewSet):
    queryset = Piloto.objects.all()
    serializer_class = PilotoSerializer
    permission_classes = [IsAdminOrReadOnly]

class CorridaViewSet(viewsets.ModelViewSet):
    queryset = Corrida.objects.all()
    serializer_class = CorridaSerializer

class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer
    permission_classes = [IsAdminOrReadOnly]


class CorridaListHTMLView(ListView):
    model = Corrida
    template_name = 'corridas/lista_corridas.html'
    context_object_name = 'corridas'


class CorridaDetailHTMLView(DetailView):
    model = Corrida
    template_name = 'corridas/detalhe_corrida.html'
    context_object_name = 'corrida'

    # Se quiser pode personalizar o queryset ou adicionar contexto extra:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        corrida = self.get_object()
        context['corrida'] = corrida
        context['resultados'] = corrida.resultados.order_by('posicao')
        return context

class ResultadoCreateView(generics.CreateAPIView):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer
    permission_classes = [permissions.IsAdminUser]


class ResultadosPorCorridaView(generics.ListAPIView):
    serializer_class = ResultadosDetalhadoSerializer

    def get_queryset(self):
        corrida_id = self.kwargs['corrida_id']
        return Resultado.objects.filter(corrida_id=corrida_id).order_by('posicao')

class RankingEquipesPDFDownload(View):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        ranking = calcular_ranking_equipes()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="ranking_equipes.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, height - 50, "Ranking de Equipes")

        y = height - 80
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Posição")
        p.drawString(120, y, "Equipe")
        p.drawString(400, y, "Pontuação")

        y -= 20
        p.setFont("Helvetica", 12)

        for idx, item in enumerate(ranking, start=1):
            if y < 100:
                p.showPage()
                y = height - 50

            p.drawString(50, y, str(idx))
            p.drawString(120, y, item['equipe'].nome)
            p.drawString(400, y, str(item['pontos']))

            # Exibir logo se houver
            equipe_obj = item['equipe']
            if equipe_obj.logo:
                logo_path = os.path.join(settings.MEDIA_ROOT, equipe_obj.logo.name)
                if os.path.exists(logo_path):
                    p.drawImage(ImageReader(logo_path), 450, y - 15, width=30, height=30, preserveAspectRatio=True)

            y -= 40

        p.showPage()
        p.save()

        return response


def PilotosPDFView(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="pilotos.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    pilotos = Piloto.objects.select_related("equipe").order_by("numero")
    y = 800

    p.drawString(100, y, "Lista de Pilotos")
    y -= 30

    for piloto in pilotos:
        texto = f"#{piloto.numero} - {piloto.nome} ({piloto.equipe.nome})"
        p.drawString(100, y, texto)
        y -= 20
        if y < 100:
            p.showPage()
            y = 800
            p.setFont("Helvetica", 12)

    p.showPage()
    p.save()
    return response
