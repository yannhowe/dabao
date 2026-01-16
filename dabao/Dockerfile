FROM python:3.14.2-alpine
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY . /usr/src/app/