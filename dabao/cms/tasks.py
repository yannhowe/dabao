# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from minio import Minio
import docker
import os
import logging

from .downloaders import dabao_docker, dabao_pcf
from .models import DockerImage, PivotalProduct

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

if os.getenv('DRYRUN') == "False":
    dryrun = False
else:
    dryrun = True

minio_session = Minio(os.getenv('MINIO_HOST', 'Token Not found'),
    access_key=os.getenv('MINIO_ACCESS_KEY', 'Token Not found'),
    secret_key=os.getenv('MINIO_SECRET_KEY', 'Token Not found'),
    secure=False)

docker_bucket_name = os.getenv('DOCKER_BUCKET_NAME', "docker-images")
docker_session = docker.from_env()
docker_session.login(username=os.getenv('DOCKERHUB_USERNAME', 'Token Not found'), password=os.getenv('DOCKERHUB_PASSWORD', 'Token Not found'), reauth=True)

download_destination = os.getenv('DOWNLOAD_DESTINATION', "local")
pivnet_bucket = os.getenv('PIVNET_BUCKET_NAME', "pivnet-products")
exclude_these_strings = [
'light-bosh-stemcell-', 
'azure', 
'openstack', 
'vcloud', 
'.txt', 
'for GCP', 
'for Openstack', 
'for AWS', 
'for Azure', 
'-aws-', 
'-gcp-',
]

@shared_task
def task_dabao_docker():
    print("task_dabao_docker!")
    download_list=DockerImage.objects.values_list('image', 'tag')
    dabao_docker.download_docker_images(docker_session, minio_session, docker_bucket_name, download_list, download_destination)

@shared_task
def task_dabao_pcf():
    print("task_dabao_pcf!")
    products=PivotalProduct.objects.values_list('product', flat=True)
    dabao_pcf.download_pcf_assets(minio_session, products, download_destination, pivnet_bucket, dryrun)