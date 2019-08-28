from django.contrib import admin
from .models import DockerImage, PivotalProduct

admin.site.register([
    DockerImage, 
    PivotalProduct,
    ])