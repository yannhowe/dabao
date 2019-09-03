from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists, SignatureDoesNotMatch, NoSuchKey)

import docker
from docker.errors import APIError, ImageNotFound

import os
from pathlib import Path
import logging

import time

def download_docker_images(docker_session, minio_session, docker_bucket_name, download_list, download_destination):

    docker_images_to_download = []
    try:
        minio_session.make_bucket(docker_bucket_name)
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        logging.info("Docker bucket already exists in minIO - %s" , docker_bucket_name)
    except ResponseError as err:
        raise

    # Build list of images to pull
    for docker_image in download_list:
        docker_image_name = docker_image[0]
        docker_image_tag = docker_image[1]
        # Pull list of tags for this docker image and save to minio
        if docker_image_tag:
            tags = docker_image_tag.split(',')
            for tag in tags:
                docker_image_to_download = docker_image_name + ':' + tag.strip()
                docker_images_to_download.append(docker_image_to_download)
        else:
            docker_images_to_download.append(docker_image_name)
        
    logging.info("docker_images_to_download: %s" % docker_images_to_download)
        
    for docker_image_to_download in docker_images_to_download:
        docker_image_filename = docker_image_to_download.replace(':', '_') + '.tar'
        docker_image_minio_path = docker_bucket_name+"/"+docker_image_filename
        docker_image_local_path = "./downloads/"+docker_image_minio_path
        docker_image_local_directory = os.path.dirname(docker_image_local_path) # Use the aws object key as path

        if download_destination == "minio": # Check MinIO to see if already downloaded
            try:
                minio_session.stat_object(docker_bucket_name, docker_image_filename)
                object_exists = True
            except ResponseError as err:
                logging.error(err)
                object_exists = False
            except NoSuchKey as err:
                logging.info("Product not downloaded yet")
                object_exists = False

        if object_exists:
            logging.info("object exists in bucket %s - %s" % (docker_bucket_name, docker_image_filename))
            
            if Path(docker_image_local_path).is_file():
                # Delete from local filesystem
                logging.info("deleting file %s" % docker_image_local_path)
                try:
                    os.remove(docker_image_local_path)
                except FileNotFoundError as err:
                    logging.info("file not found while deleting %s" % docker_image_local_path)

        else: # Doesn't exist in MinIO
            if Path(docker_image_local_path).is_file():
                # Delete from local filesystem
                logging.info("deleting file %s" % docker_image_local_path)
                try:
                    os.remove(docker_image_local_path)
                except FileNotFoundError as err:
                    logging.error("file not found while deleting %s" % docker_image_local_path)
            
            # Pull image to system
            logging.info("Pulling %s" % docker_image_to_download)
            try:
                docker_session.images.pull(docker_image_to_download)
            except (ImageNotFound, APIError) as err:
                logging.error("Problem pulling image: %s - %s" % (docker_image_to_download , err))
                continue

            try:
                os.makedirs(docker_image_local_directory, exist_ok=True) # create any directories needed
            except FileExistsError:
                logging.info("directory already exists %s" % docker_image_local_directory)
            
            logging.info("saving image to: %s" % docker_image_local_path)
            f = open(docker_image_local_path, 'wb')
            for chunk in docker_session.images.get(docker_image_to_download).save():
                f.write(chunk)
            file_size = os.fstat(f.fileno()).st_size
            f.close()

            # Upload docker image to minIO
            try:
                file_data = open(docker_image_local_path, 'rb')
                file_stat = os.stat(docker_image_local_path)

                logging.info("upload to minIO - %s" , docker_image_local_path)
                logging.info(minio_session.put_object(docker_bucket_name, docker_image_filename, file_data, file_stat.st_size))

                logging.info("Deleting %s" % docker_image_local_path)
                os.remove(docker_image_local_path)
            except (ResponseError, SignatureDoesNotMatch) as err:
                logging.info("upload docker to minIO failed - %s" , docker_image_local_path)
                logging.error(err)