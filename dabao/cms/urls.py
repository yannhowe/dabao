from django.urls import path
from cms.views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('dockerimage/add/', DockerImageCreate.as_view(), name='docker-image-add'),
    path('dockerimage/<int:pk>/', DockerImageUpdate.as_view(), name='docker-image-update'),
    path('dockerimage/<int:pk>/delete/', DockerImageDelete.as_view(), name='docker-image-delete'),
    path('pivotalproduct/add/', PivotalProductCreate.as_view(), name='pivotal-product-add'),
    path('pivotalproduct/<int:pk>/', PivotalProductUpdate.as_view(), name='pivotal-product-update'),
    path('pivotalproduct/<int:pk>/delete/', PivotalProductDelete.as_view(), name='pivotal-product-delete'),
]