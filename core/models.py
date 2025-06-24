from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.URLField(max_length=500, blank=True, null=True)
    cor = models.CharField(max_length=7, default='#000000')  # ex: #FF0000

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    @property
    def vitorias(self):
        return sum(p.vitorias() for p in self.pilotos.all())  # related_name 'pilotos' usado aqui

class Piloto(models.Model):
    nome = models.CharField(max_length=100)
    numero = models.IntegerField()
    equipe = models.ForeignKey('Equipe', on_delete=models.CASCADE, related_name='pilotos')

    def __str__(self):
        return f"{self.nome} #{self.numero}"
    
    def vitorias(self):
        return self.resultados.filter(posicao=1).count()

class Corrida(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    pista = models.TextField()
    caracteristicas = models.TextField(blank=True)
    bandeira = models.ImageField(upload_to='bandeiras/', blank=True, null=True)
    foto_pista = models.ImageField(upload_to='pistas/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Resultado(models.Model):
    piloto = models.ForeignKey(Piloto, related_name='resultados', on_delete=models.CASCADE)
    corrida = models.ForeignKey(Corrida, related_name='resultados', on_delete=models.CASCADE)
    posicao = models.PositiveIntegerField()

    def pontuacao(self):
        F1_POINTS = {
            1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1,
        }
        return F1_POINTS.get(self.posicao, 0)
    
    def clean(self):
        # Limitar posição entre 1 e 20
        if self.posicao < 1 or self.posicao > 22:
            raise ValidationError("A posição deve estar entre 1 e 22.")

        # Evitar piloto duplicado na mesma corrida
        if Resultado.objects.filter(corrida=self.corrida, piloto=self.piloto).exclude(pk=self.pk).exists():
            raise ValidationError("Este piloto já tem resultado nesta corrida.")

        # Evitar mesma posição duplicada na mesma corrida
        if Resultado.objects.filter(corrida=self.corrida, posicao=self.posicao).exclude(pk=self.pk).exists():
            raise ValidationError(f"A posição {self.posicao} já está ocupada nesta corrida.")

    def save(self, *args, **kwargs):
        self.clean()  # valida antes de salvar
        super().save(*args, **kwargs)
