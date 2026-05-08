from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_description="API Health Check",
    responses={200: openapi.Response(description="OK")}
)
@api_view(['GET'])
def api_root(request):
    return Response({
        'message': _('KROPITS API - AgriTech Logistics Platform'),
        'version': '1.0',
        'endpoints': {
            'auth': '/api/auth/',
            'farmers': '/api/farmers/',
            'buyers': '/api/buyers/',
            'orders': '/api/orders/',
            'delivery': '/api/delivery/',
            'optimizer': '/api/optimizer/',
            'health': '/health/',
        }
    })
