from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import DockerImage, PivotalProduct

# Create your views here.
class DashboardView(ListView):

    model = DockerImage
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Docker
        try:
            docker_image_list = DockerImage.objects.order_by('image')
        except DockerImage.DoesNotExist:
            docker_image_list = None

        context['docker_image_list'] = docker_image_list
        
        # Pivotal
        try:
            pivotal_product_list = PivotalProduct.objects.order_by('product')
        except PivotalProduct.DoesNotExist:
            pivotal_product_list = None

        context['pivotal_product_list'] = pivotal_product_list

        return context
    
class DabaoView(TemplateView):

    template_name = "dabao.html"


class DockerImageCreate(CreateView):
    model = DockerImage
    fields = ['image', 'tag']
    success_url = reverse_lazy('dashboard')

class DockerImageUpdate(UpdateView):
    model = DockerImage
    fields = ['image', 'tag']
    success_url = reverse_lazy('dashboard')

class DockerImageDelete(DeleteView):
    model = DockerImage
    success_url = reverse_lazy('dashboard')


class PivotalProductCreate(CreateView):
    model = PivotalProduct
    fields = ['product']
    success_url = reverse_lazy('dashboard')

class PivotalProductUpdate(UpdateView):
    model = PivotalProduct
    fields = ['product']
    success_url = reverse_lazy('dashboard')

class PivotalProductDelete(DeleteView):
    model = PivotalProduct
    success_url = reverse_lazy('dashboard')