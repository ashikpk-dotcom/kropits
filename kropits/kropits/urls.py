from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'ok'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/farmers/', include('farmers.urls')),
    path('api/buyers/', include('buyers.urls')),
    path('api/orders/', include('logistics.urls')),
    path('api/delivery/', include('logistics.urls')),
    path('api/optimizer/', include('optimizer.urls')),
    path('health/', health_check),
    path('', TemplateView.as_view(template_name='index.html')),
]
