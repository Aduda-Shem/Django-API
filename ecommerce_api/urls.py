from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from ecommerce.views.authentication import oauth_openid_callback

# Define schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
        description="Ecommerce APIs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

# Define urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('o/callback/', oauth_openid_callback, name='oauth_callback'),
    path('api/', include('ecommerce.ecom_urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
