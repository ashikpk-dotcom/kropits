from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .models import FarmerProduct
from .serializers import FarmerProductSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = FarmerProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FarmerProduct.objects.filter(farmer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FarmerProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FarmerProduct.objects.filter(farmer=self.request.user)


class AvailabilityToggleView(generics.UpdateAPIView):
    serializer_class = FarmerProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FarmerProduct.objects.filter(farmer=self.request.user)

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_available = not product.is_available
        product.save()
        return Response({
            'message': _('Availability toggled successfully'),
            'is_available': product.is_available
        })


@login_required
def farmer_dashboard(request):
    products = FarmerProduct.objects.filter(farmer=request.user)
    return render(request, 'farmers/dashboard.html', {'products': products})


@login_required
def add_product(request):
    return render(request, 'farmers/add_product.html')
