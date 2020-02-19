# Base Image
FROM python:3.8

# create and set working directory
RUN mkdir /app && \
        mkdir -p /tmp/django/water_graph/media/ && \
        mkdir -p /tmp/django/water_graph/static/
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

ENV PORT=8888

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    chmod +x docker-entrypoint.sh

# install environment dependencies
RUN pip3 install --upgrade pip
RUN pip3 install gunicorn

RUN pip3 install -r requirements.txt

RUN mkdir -p /tmp/JWT && \
    cd /tmp/JWT/ && \
    git init . && \
    git pull https://github.com/flavors/django-graphql-jwt.git master && \
    python3 /tmp/JWT/setup.py sdist && \
    pip3 install /tmp/JWT/dist/django*

EXPOSE 8888
CMD /app/docker-entrypoint.sh $PORT