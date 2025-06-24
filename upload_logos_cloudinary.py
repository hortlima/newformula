import os
import django
import requests

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formula_betting.settings')
django.setup()

from core.models import Equipe

FALHAS = []

print("🔍 Verificando logos no Cloudinary...\n")

for equipe in Equipe.objects.all():
    if not equipe.logo:
        print(f"🚫 {equipe.nome} sem logo.")
        continue

    url = equipe.logo
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {equipe.nome} → OK")
        else:
            print(f"❌ {equipe.nome} → Status {response.status_code}")
            FALHAS.append((equipe.nome, url, response.status_code))
    except Exception as e:
        print(f"⚠️ {equipe.nome} → Erro: {e}")
        FALHAS.append((equipe.nome, url, str(e)))

print("\n📋 Resultado final:")
if not FALHAS:
    print("🎉 Todas as logos foram validadas com sucesso!")
else:
    for nome, url, erro in FALHAS:
        print(f"- {nome}: {erro} → {url}")


