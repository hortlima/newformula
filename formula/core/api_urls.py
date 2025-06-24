from rest_framework.routers import DefaultRouter
from .views import EquipeViewSet, PilotoViewSet, CorridaViewSet, ResultadoViewSet

router = DefaultRouter()
router.register(r'equipes', EquipeViewSet)
router.register(r'pilotos', PilotoViewSet)
router.register(r'corridas', CorridaViewSet)
router.register(r'resultados', ResultadoViewSet)

urlpatterns = router.urls
