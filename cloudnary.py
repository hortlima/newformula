import os
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formula_betting.settings')

import django
django.setup()

import cloudinary
import cloudinary.uploader
from django.core.files.base import ContentFile
import requests
from core.models import Equipe

# Config Cloudinary
cloudinary.config( 
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.environ.get('CLOUDINARY_API_KEY'), 
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

for equipe in Equipe.objects.all():
    if equipe.logo and not str(equipe.logo).startswith('http'):
        try:
            upload_result = cloudinary.uploader.upload(equipe.logo.path, folder='logos_equipes')
            equipe.logo = upload_result['secure_url']
            equipe.save()
            print(f"✅ Logo atualizado: {equipe.nome}")
        except Exception as e:
            print(f"❌ Erro com {equipe.nome}: {e}")
    else:
        print(f"ℹ️ Ignorado (já em Cloudinary): {equipe.nome}")