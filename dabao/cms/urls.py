from django.urls import path
from cms.views import DashboardView, DabaoView

urlpatterns = [
    path('', DashboardView.as_view()),
]