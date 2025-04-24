from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),
    # Redirect root URL to API endpoint
    path("", RedirectView.as_view(url="/api/schema/swagger-ui/", permanent=False)),
    # API endpoints
    path("api/", include(("api.urls", "api"), namespace="api")),
    # API schema generation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
