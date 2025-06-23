from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import (
    PublicHomeView, PublicDataHomeView, RankingEquipes,
    RankingEquipesPDFDownload, EquipeDetailView
)
from public import urls as public_urls

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', PublicHomeView.as_view(), name='home'),
    path('dados-completos/', PublicDataHomeView.as_view(), name='public_home_dados'),
    path('admin/', admin.site.urls),
    path('api/', include('core.api_urls')),

    path('public/', include(public_urls)),
    path('equipe/<slug:slug>/', EquipeDetailView.as_view(), name='equipe_detail'),

    path('api/ranking/equipes/', RankingEquipes.as_view(), name='ranking_equipes'),
    path('api/ranking/equipes/pdf', RankingEquipesPDFDownload.as_view(), name='ranking_equipes-pdf'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
