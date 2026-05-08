from django.urls import path
from .views import MatchFarmerView, RouteOptimizationView, PredictDemandView, RunOptimizationTasksView, optimizer_dashboard

urlpatterns = [
    path('match/', MatchFarmerView.as_view(), name='match-farmer'),
    path('route/', RouteOptimizationView.as_view(), name='route-optimization'),
    path('predict/', PredictDemandView.as_view(), name='predict-demand'),
    path('run-tasks/', RunOptimizationTasksView.as_view(), name='run-tasks'),
    path('dashboard/', optimizer_dashboard, name='optimizer-dashboard'),
]
