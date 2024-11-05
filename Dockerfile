FROM nvidia/cuda:12.2.0-base-ubuntu22.04

# Configure apt-get to automatically use noninteractive settings
ENV DEBIAN_FRONTEND=noninteractive

# Install system libraries
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3.10 \
        python3.10-dev \
        python3.10-venv \
        python3-pip \
        apt-utils \
        curl \
        wget \
        vim \
        sudo \
        git \
        git-lfs \
        ffmpeg \
        libsm6 \
        libxext6 \
        python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the docker container
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .

# Copy the current directory contents into the container at /app
COPY . /app

RUN python3.10 -m pip install --upgrade pip setuptools
RUN python3.10 -m pip install --upgrade -r requirements.txt \
     && rm -rf /root/.cache/pip/*
RUN pip install zhipuai==2.0.1
RUN pip install lark
RUN pip install rembg[gpu]

# Set default values for environment variables
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8080
ENV COMFY_PATH=ComfyUI/main.py

# Run as root
USER root

# Run your application
CMD ["sh", "-c", "python3.10 ${COMFY_PATH} & python3.10 runpod_handler.py"]