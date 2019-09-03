import os
import re
import sys
import logging
from pathlib import Path
import requests
from nested_lookup import nested_lookup
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists, SignatureDoesNotMatch, NoSuchKey)


def download_pcf_assets(minioClient, products, download_destination, pivnet_bucket, dryrun):

    exclude_these_strings = []

    try:
        if not minioClient.bucket_exists(pivnet_bucket):
            try:
                minioClient.make_bucket(pivnet_bucket)
            except ResponseError as err:
                logging.info(err)
    except ResponseError as err:
        logging.info(err)

    # Get fresh token
    uaa_refresh_token = os.getenv('UAA_API_TOKEN', "Not Set")
    response = requests.post('https://network.pivotal.io/api/v2/authentication/access_tokens', data={'refresh_token':uaa_refresh_token})

    # Exit if bad token
    if not response:
        logging.info("Error: Probably a bad api token. Check your .env file and follow the instructions to see if you've added the correct UAA_API_TOKEN")
        sys.exit()

    # Available product slugs
    product_slugs = nested_lookup('slug', requests.get('https://network.pivotal.io/api/v2/products/').json())
    logging.info("available products:")
    logging.info(product_slugs)

    # Get products
    product_urls=[]
    stemcell_urls=[]

    # Get stemcells-ubuntu-xenial 250.*
    stemcells_ubuntu_xenial_release_list = requests.get("https://network.pivotal.io/api/v2/products/stemcells-ubuntu-xenial/releases", allow_redirects=True).json()
    for release in stemcells_ubuntu_xenial_release_list["releases"]:
        if "250" in release["version"]:
            #stemcell_urls.append(release["_links"]["product_files"]["href"])
            pass

    try:
        product_urls.append(stemcell_urls[0])
    except IndexError:
        logging.info("IndexError: empty list %s" % "stemcell_urls")

    # Get other products
    for product in products:
        product_url="https://network.pivotal.io/api/v2/products/" + product + "/releases/latest"
        product_urls.append(product_url)

    # Setup headers for file download
    headers={}
    headers["Authorization"]="Bearer " + response.json()['access_token']

    # Download all files in product
    for product_url in product_urls:
        r = requests.get(product_url, allow_redirects=True)

        for product_file in r.json()['product_files']:
            if any(exclusions in product_file['aws_object_key'] for exclusions in exclude_these_strings):
                logging.info("excluding %s" % product_file['aws_object_key'])
            else:
                product_path = product_file['aws_object_key']
                product_minio_path = pivnet_bucket+"/"+product_path
                product_local_path = "./downloads/"+product_minio_path
                product_directory = os.path.dirname(product_local_path) # Use the aws object key as path
                try:
                    os.makedirs(product_directory, exist_ok=True) # create any directories needed
                except FileExistsError:
                    logging.info("directory already exists %s" % product_directory)
                if dryrun:
                    logging.info("dryrun - downloading %s" % product_path)
                else: # Download files
                    if download_destination == "minio": # Check MinIO to see if already downloaded
                        try:
                            minioClient.stat_object(pivnet_bucket, product_path)
                            object_exists = True
                        except ResponseError as err:
                            logging.info(err)
                            object_exists = False
                        except NoSuchKey as err:
                            logging.info("Product not downloaded yet.")
                            object_exists = False

                    if object_exists:
                        logging.info("object exists in bucket %s - %s" % (pivnet_bucket, product_path))
                        if Path(product_minio_path).is_file():
                            # Delete from local filesystem
                            logging.info("deleting file %s" % product_local_path)
                            try:
                                os.remove(product_local_path)
                            except FileNotFoundError as err:
                                logging.info("file not found while deleting %s" % product_local_path)
                    else: # Doesn't exist in MinIO
                        if Path(product_local_path).is_file(): # Check if file already exists
                            logging.info("already downloaded %s" % product_local_path)
                        else:
                            logging.info("downloading %s" % product_path)
                            r_downloadfile = requests.get(product_file['_links']['download']['href'], headers=headers) # make get request
                            open(product_local_path, 'wb').write(r_downloadfile.content) # write to file

                    if not object_exists and download_destination == "minio": # Upload to Minio
                        logging.info("uploading to bucket %s - %s" % (pivnet_bucket, product_directory))
                        try:
                            logging.info(minioClient.fput_object(pivnet_bucket, product_path, product_local_path))
                        except ResponseError as err:
                            logging.info(err)
                        # Delete from local filesystem
                        logging.info("deleting file %s" % product_local_path)
                        try:
                            os.remove(product_local_path)
                        except FileNotFoundError as err:
                            logging.info("file not found while deleting %s" % product_local_path)