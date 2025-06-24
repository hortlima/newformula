from rest_framework import serializers
from .models import Equipe, Piloto, Corrida, Resultado

class EquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipe
        fields = '__all__'

class PilotoSerializer(serializers.ModelSerializer):
    equipe = serializers.StringRelatedField()

    class Meta:
        model = Piloto
        fields = ['nome', 'numero', 'equipe']

class ResultadoSerializer(serializers.ModelSerializer):
    piloto = serializers.StringRelatedField()
    equipe = serializers.StringRelatedField()

    class Meta:
        model = Resultado
        fields = ['posicao', 'numero', 'piloto', 'equipe', 'pontuacao']

class CorridaSerializer(serializers.ModelSerializer):
    resultados = ResultadoSerializer(many=True, read_only=True)

    class Meta:
        model = Corrida
        fields = '__all__'

class ResultadosDetalhadoSerializer(serializers.ModelSerializer):
    piloto = serializers.CharField(source='piloto.nome')
    numero = serializers.IntegerField(source='piloto.numero')
    equipe = serializers.CharField(source='piloto.equipe.nome')
    pontos = serializers.SerializerMethodField()

    class Meta:
        model = Resultado
        fields = ['piloto', 'equipe', 'posicao', 'pontos']
    
    def get_pontos(self, obj):
        return obj.pontuacao()

    def get_pontuacao(self, obj):
        return obj.pontuacao()
