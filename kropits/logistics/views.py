from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .models import Order, DeliveryPartner, DeliveryAssignment
from .serializers import OrderSerializer, DeliveryPartnerSerializer, DeliveryAssignmentSerializer, ProofUploadSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        buyer_request_id = request.data.get('buyer_request')
        if not buyer_request_id:
            return Response({'error': _('Buyer request ID required')}, status=status.HTTP_400_BAD_REQUEST)

        from buyers.models import BuyerRequest
        try:
            buyer_request = BuyerRequest.objects.get(id=buyer_request_id, buyer=request.user)
        except BuyerRequest.DoesNotExist:
            return Response({'error': _('Invalid buyer request')}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            buyer_request=buyer_request,
            total_amount=buyer_request.offered_price * buyer_request.quantity_requested,
            delivery_address=buyer_request.delivery_address,
            delivery_location=buyer_request.delivery_location,
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderStatusView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer_request__buyer=self.request.user)


class AvailableDeliveryPartnersView(generics.ListAPIView):
    serializer_class = DeliveryPartnerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryPartner.objects.filter(is_available=True)


class DeliveryAssignView(generics.CreateAPIView):
    serializer_class = DeliveryAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order')
        partner_id = request.data.get('delivery_partner')

        try:
            order = Order.objects.get(id=order_id, status='confirmed')
            partner = DeliveryPartner.objects.get(id=partner_id, is_available=True)
        except (Order.DoesNotExist, DeliveryPartner.DoesNotExist):
            return Response({'error': _('Invalid order or partner')}, status=status.HTTP_400_BAD_REQUEST)

        assignment = DeliveryAssignment.objects.create(
            order=order,
            delivery_partner=partner,
            pickup_location=order.buyer_request.product.farmer.location,
        )
        order.status = 'assigned'
        order.save()
        partner.is_available = False
        partner.save()

        return Response(DeliveryAssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)


class ProofUploadView(generics.UpdateAPIView):
    serializer_class = ProofUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryAssignment.objects.filter(delivery_partner__user=self.request.user)


@login_required
def orders_dashboard(request):
    if request.user.role == 'buyer':
        orders = Order.objects.filter(buyer_request__buyer=request.user)
    elif request.user.role == 'farmer':
        orders = Order.objects.filter(buyer_request__product__farmer=request.user)
    else:
        orders = Order.objects.all()
    return render(request, 'logistics/orders_dashboard.html', {'orders': orders})
