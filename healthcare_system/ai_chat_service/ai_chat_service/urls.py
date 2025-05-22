from django.urls import path, include
from django.http import HttpResponse
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AI Chat Service API",
        default_version='v1',
        description="API for AI Chat Service",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def home(request):
    return HttpResponse("Welcome to AI Chat Service! Use /api/ai_chat/ for API endpoints.")

urlpatterns = [
    path('', home, name='home'),
    path('api/ai_chat/', include('ai_chat.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]