ARG BASE_IMAGE="ubuntu:20.04"
FROM ${BASE_IMAGE} AS base

# Docker and System
ENV DEBIAN_FRONTEND="noninteractive"
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8" 
ENV PY_VER="3.10.4"

# Runtime defaults
ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="5000"
ENV FLASK_ENV="production"
ENV FLASK_APP="./main.py"

FROM base AS wheels
WORKDIR /build

COPY ./Nodes/YoloV5Node/requirements.txt .

RUN apt-get update && apt-get install -y                        \
    python3     python3-pip     python3-dev                     \
    gcc cpp     build-essential                              && \
    python3 -m pip install -U pip wheel setuptools           && \
    python3 -m pip install -U cython cmake                   && \
    python3 -m pip wheel --wheel-dir=/local/wheels/ -r requirements.txt gunicorn

FROM base AS runtime-prep

RUN apt-get update && apt-get install -y                        \
        python${PY_VER}     python3-pip     libgl1              \
        libsm6 libxrender1 libxext6                          && \
        python3 -m pip install -U pip                        && \
        apt-get upgrade -y && apt-get auto-remove -y         && \
        apt-get clean -y && rm -rf /var/lib/apt/cache

FROM runtime-prep AS final

COPY --from=wheels /build/requirements.txt .
COPY --from=wheels /local/wheels/ /tmp/wheels/

RUN /usr/bin/python3 -m pip install --prefer-binary --find-links=/tmp/wheels -r requirements.txt gunicorn && rm -rf /tmp/wheels

FROM final
WORKDIR /app

RUN rm -rf /bin/bash /bin/sh

LABEL org.Scenera.image.authors="dirk.meulenbelt@scenera.net"

COPY ./Nodes/YoloV5Node/Source /app
COPY ./Nodes/YoloV5Node/Deploy/wsgi/gunicorn_config.py /app/

EXPOSE 5000

#CMD [ "/usr/bin/python3", "-m", "flask", "run" ]
CMD [ "python3", "-m", "gunicorn", "--config", "gunicorn_config.py", "main:app" ]