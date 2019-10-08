from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists, SignatureDoesNotMatch, NoSuchKey)

import docker
from docker.errors import APIError, ImageNotFound

import os
from pathlib import Path
import logging

import time

def upload_docker_images(docker_session, docker_session_low_level_api, minio_session, docker_bucket_name, target_docker_registry, dryrun):

    # Get list of images from MinIO, for images do
    objects = minio_session.list_objects_v2(docker_bucket_name, recursive=True)

    if objects:
        for obj in objects:
            if dryrun:
                logging.info("dryrun - downloading, tagging and uploading %s" % obj.object_name)
            else:
                logging.info("downloading %s" % obj.object_name)
                # Get image from Minio
                if not os.path.isdir('./tmp/'):
                    os.mkdir('./tmp/')

                try:
                    image = obj.object_name.split('_')[0].replace('+','/') + ":" + obj.object_name.split('_')[1].replace('.tar','')
                    logging.info("Working with image: %s" % image) 
                except ResponseError as err:
                    logging.error(err) 

                try:
                    data = minio_session.get_object(docker_bucket_name, obj.object_name)
                    with open("./tmp/"+obj.object_name, 'wb') as file_data:
                        for d in data.stream(32*1024):
                            file_data.write(d)
                except ResponseError as err:
                    logging.error(err) 

                # Load image to host
                logging.info("docker load %s" % obj.object_name)
                with open("./tmp/"+obj.object_name, 'rb') as file_data:
                    docker_session.images.load(file_data)

                # Push image to target registry
                logging.info("docker push %s" % image)
                docker_session_low_level_api.login(registry="https://"+os.getenv('LELONG_DOCKER_REGISTRY', 'Token Not found'), username=os.getenv('LELONG_DOCKER_USER', 'Token Not found'), password=os.getenv('LELONG_DOCKER_PASSWORD', 'Token Not found'), reauth=True)
                logging.info(docker_session_low_level_api.tag(image, target_docker_registry+"/"+image))
                logging.info(docker_session_low_level_api.push(target_docker_registry+"/"+image))
    else:
        logging.info("No docker images to upload")