# 打包 (dǎ bāo)
打包 (dǎ bāo) internet resources for your air-gapped environment.

:white_check_mark: GUI-based

:white_check_mark: (Reasonably) Easy Setup

Supports:
- [x]  [Pivotal Network](https://network.pivotal.io/) Stemcells and Releases
- [x]  Docker Images
- [ ]  Helm Repositories & Charts
- [ ]  Git Repositories
- [ ]  NPM Packages

# Quickstart
Make sure you have [docker](https://docs.docker.com/install/), [docker-compose](https://docs.docker.com/compose/install/) & [MC](https://docs.min.io/docs/minio-client-quickstart-guide.html).
```
# Clone Repo
git clone https://github.com/yannhowe/dabao.git

# Fill up the .env.example file and rename to .env
mv .env.example .env

# Initialise database & create admin user
docker-compose run --rm dabao-cms python /usr/src/app/manage.py makemigrations
docker-compose run --rm dabao-cms python /usr/src/app/manage.py migrate
docker-compose run --rm dabao-cms python /usr/src/app/manage.py loaddata initial_data.json
docker-compose run --rm dabao-cms python /usr/src/app/manage.py createsuperuser --email admin@dabao.com --username admin

# Get everything up!
docker-compose up -d

# Backup Database
docker-compose run --rm dabao-cms python /usr/src/app/manage.py dumpdata auth django_celery_beat cms

# set bucket permissions in MinIO
mc policy -r set download myminio/docker-images
mc policy -r set download myminio/pivnet-products

# MC Mirror the bucket to your server, thumbdrive, diode, wherever..
mc mirror --watch  myminio/docker-images/ docker-images
mc mirror --watch  myminio/pivnet-products/ pivnet-products
```

# Notes
## Pivotal API
Log in to your [pivotal profile](https://network.pivotal.io/users/dashboard/edit-profile) and generate your UAA API KEY if you don't already have one and add the UAA API KEY to the .env file

> Remember you need to accept the EULA on the website before you are allowed to download using the API!
