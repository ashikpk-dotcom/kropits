from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .matching import match_farmer_to_buyer, predict_demand
from .routing import optimize_delivery_routes
from .tasks import optimize_routes_task, predict_demand_task, auto_assign_delivery_task
from buyers.models import BuyerRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class MatchFarmerView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        buyer_request_id = request.data.get('buyer_request_id')
        if not buyer_request_id:
            return Response({'error': _('Buyer request ID required')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            buyer_request = BuyerRequest.objects.get(id=buyer_request_id)
        except BuyerRequest.DoesNotExist:
            return Response({'error': _('Buyer request not found')}, status=status.HTTP_404_NOT_FOUND)

        matches = match_farmer_to_buyer(buyer_request)
        return Response({'matches': matches})


class RouteOptimizationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        deliveries = request.data.get('deliveries', [])
        if not deliveries:
            return Response({'error': _('Deliveries data required')}, status=status.HTTP_400_BAD_REQUEST)

        routes = optimize_delivery_routes(deliveries)
        return Response({'routes': routes})


class PredictDemandView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        category = request.data.get('category')
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')

        if not all([category, lat, lon]):
            return Response({'error': _('Category, latitude, and longitude required')}, status=status.HTTP_400_BAD_REQUEST)

        prediction = predict_demand(category, (lon, lat))
        return Response(prediction)


class RunOptimizationTasksView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        optimize_routes_task.delay()
        auto_assign_delivery_task.delay()
        return Response({'message': _('Optimization tasks started')})


@login_required
def optimizer_dashboard(request):
    return render(request, 'optimizer/dashboard.html')
