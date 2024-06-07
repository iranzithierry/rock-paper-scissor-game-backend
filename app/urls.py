from django.conf import settings
from django.urls import path, include
from base.sites import app_admin_site
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularSwaggerView,  SpectacularAPIView
from app.users.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path(settings.ADMIN_URL,  app_admin_site.urls),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


urlpatterns += [
    # api
    path("api/", include("app.api")),
    # auth
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # swagger docs
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
