# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from minio import Minio
import docker
import os
import logging

from .downloaders import dabao_docker, dabao_pcf
from .uploaders import lelong_docker
from .models import DockerImage, PivotalProduct

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

if os.getenv('DRYRUN') == "False":
    dryrun = False
else:
    dryrun = True

dabao_minio_session = Minio(os.getenv('DABAO_MINIO_HOST', 'Token Not found'),
    access_key=os.getenv('DABAO_MINIO_ACCESS_KEY', 'Token Not found'),
    secret_key=os.getenv('DABAO_MINIO_SECRET_KEY', 'Token Not found'),
    secure=False)

lelong_minio_session = Minio(os.getenv('LELONG_MINIO_HOST', 'Token Not found'),
    access_key=os.getenv('LELONG_MINIO_ACCESS_KEY', 'Token Not found'),
    secret_key=os.getenv('LELONG_MINIO_SECRET_KEY', 'Token Not found'),
    secure=False)

docker_bucket_name = os.getenv('DOCKER_BUCKET_NAME', "docker-images")
docker_session = docker.from_env()
docker_session_low_level_api = docker.APIClient(base_url='unix://var/run/docker.sock')

target_docker_registry = os.getenv('LELONG_DOCKER_REGISTRY', 'Token Not found')
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
    logging.info("task_dabao_docker!")
    download_list=DockerImage.objects.values_list('image', 'tag')
    dabao_docker.download_docker_images(docker_session, dabao_minio_session, docker_bucket_name, download_list, download_destination, dryrun)

@shared_task
def task_dabao_pcf():
    logging.info("task_dabao_pcf!")
    products=PivotalProduct.objects.values_list('product', flat=True)
    dabao_pcf.download_pcf_assets(dabao_minio_session, products, download_destination, pivnet_bucket, dryrun)

@shared_task
def task_lelong_docker():
    logging.info("task_lelong_docker!")
    lelong_docker.upload_docker_images(docker_session, docker_session_low_level_api, lelong_minio_session, docker_bucket_name, target_docker_registry, dryrun)