import os
import django
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from django.conf import settings

# Carrega variáveis do .env
load_dotenv()

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formula_betting.settings')
django.setup()

# Configura a Cloudinary diretamente
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

from core.models import Corrida

print("☁️ Fazendo upload das bandeiras e fotos de pista para Cloudinary...\n")

for corrida in Corrida.objects.all():
    atualizado = False

    # Corrigir bandeira
    if corrida.bandeira and not str(corrida.bandeira).startswith("https://"):
        local_path = os.path.join(settings.MEDIA_ROOT, str(corrida.bandeira))
        if os.path.exists(local_path):
            result = cloudinary.uploader.upload(
                local_path,
                folder="bandeiras_corridas",
                public_id=f"bandeira_{corrida.id}",
                overwrite=True,
                resource_type="image"
            )
            corrida.bandeira = result['secure_url']
            atualizado = True
            print(f"✔️ Bandeira enviada para {corrida.nome}")

    # Corrigir foto da pista
    if corrida.foto_pista and not str(corrida.foto_pista).startswith("https://"):
        local_path = os.path.join(settings.MEDIA_ROOT, str(corrida.foto_pista))
        if os.path.exists(local_path):
            result = cloudinary.uploader.upload(
                local_path,
                folder="fotos_pistas",
                public_id=f"foto_pista_{corrida.id}",
                overwrite=True,
                resource_type="image"
            )
            corrida.foto_pista = result['secure_url']
            atualizado = True
            print(f"✔️ Foto da pista enviada para {corrida.nome}")

    if atualizado:
        corrida.save()

print("\n✅ Upload finalizado com sucesso.")
