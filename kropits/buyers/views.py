from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .models import BuyerRequest
from .serializers import BuyerRequestSerializer, NearbyFarmerSerializer
from farmers.models import FarmerProduct
from accounts.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class BuyerRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = BuyerRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BuyerRequest.objects.filter(buyer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


class BuyerRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BuyerRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BuyerRequest.objects.filter(buyer=self.request.user)


class NearbyFarmersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer = request.user
        if not buyer.location:
            return Response({'error': _('Buyer location not set')}, status=status.HTTP_400_BAD_REQUEST)

        nearby_products = FarmerProduct.objects.filter(
            is_available=True
        ).select_related('farmer')[:20]

        results = []
        for product in nearby_products:
            results.append({
                'farmer_id': product.farmer.id,
                'farmer_name': product.farmer.get_full_name(),
                'product_id': product.id,
                'product_name': product.name,
                'distance': 0,
                'quantity': product.quantity,
                'price_per_unit': product.price_per_unit,
            })

        serializer = NearbyFarmerSerializer(results, many=True)
        return Response(serializer.data)


@login_required
def buyer_dashboard(request):
    requests = BuyerRequest.objects.filter(buyer=request.user)
    return render(request, 'buyers/dashboard.html', {'requests': requests})
