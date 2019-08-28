from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import DockerImage, PivotalProduct

# Create your views here.
class DashboardView(ListView):

    model = DockerImage
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Docker
        try:
            docker_image_list = DockerImage.objects.all()
        except DockerImage.DoesNotExist:
            docker_image_list = None

        context['docker_image_list'] = docker_image_list
        
        # Pivotal
        try:
            pivotal_product_list = PivotalProduct.objects.all()
        except PivotalProduct.DoesNotExist:
            pivotal_product_list = None

        context['pivotal_product_list'] = pivotal_product_list

        return context
 
class DabaoView(TemplateView):

    template_name = "dabao.html"

    