FROM python:3.14.0rc1-alpine
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY . /usr/src/app/