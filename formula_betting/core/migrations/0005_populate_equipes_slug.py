from django.db import migrations
from django.utils.text import slugify

def generate_unique_slugs(apps, schema_editor):
    Equipe = apps.get_model('core', 'Equipe')
    slugs = set()
    for equipe in Equipe.objects.all():
        base_slug = slugify(equipe.nome)
        slug = base_slug
        i = 1
        while slug in slugs:
            slug = f"{base_slug}-{i}"
            i += 1
        equipe.slug = slug
        equipe.save()
        slugs.add(slug)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_equipe_slug'),
    ]

    operations = [
        migrations.RunPython(generate_unique_slugs),
    ]
