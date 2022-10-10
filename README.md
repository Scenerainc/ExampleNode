# YoloV5 Object Detection Node (Example)

This example was posted on 10 October 2022.

It implements YoloV5 as a Node in the Scenera ecosystem using the [NodeSDK](https://github.com/Scenerainc/SceneraNodeSDK).

Version: [scenera.node](https://pypi.org/project/scenera.node/)==0.2.12

Made by Taekyu Ryu

---

## Getting Started

Clone and change working directory to the repository ;-)

### Option 1: Native python

#### Dependencies

Minimal:

- python3  
- python3-pip

> #### Setup Python virtual environment (*optional, recommended*)
>
> NOTE, on Nvidia Jetson: Virtual Environments appears to be broken *Feb 28th, 2022*
>
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
>
> python3 -m pip install -U pip wheel setuptools
> ```

### Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

> #### Note
>
> On systems like Nvidia Jetsons, some .whl binaries may not be available, thus pip would have to build the package itself, this requires a few additional tools
>
> ```bash
> sudo apt-get update && sudo apt-get install -y    \
>   gcc     cpp     build-essential
> ```
>
> ```bash
> python3 -m pip install -U pip wheel setuptools
> python3 -m pip install -U cmake cython
> ```

### Run the code

> ### Configure environment variables (*Optional*)
>
> ```bash
> export "FLASK_ENV=development"
> export "FLASK_APP=$PWD/yolov5_node/main.py"
> ```

### Launch

```bash
python3 yolov5_node/main.py
```

> Alternatively if the Environment variables have been set
>
> ```bash
> python3 -m flask run
> ```

### Option 2: [Docker CLI](https://docs.docker.com/engine/reference/run/)

#### Dependencies

- [Docker (*link for x86_64 Ubuntu systems*)](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script)

#### Build the [image](https://docs.docker.com/engine/reference/commandline/images/#extended-description) - [Docker CLI](https://docs.docker.com/engine/reference/run/)

```bash
docker build \
    -t nicescenera.azurecr.io/yolov5node:latest \
    --file="$PWD/deployment/docker/Dockerfile" \
    $PWD
```

#### Run the [container](https://www.docker.com/resources/what-container) - [Docker CLI](https://docs.docker.com/engine/reference/run/)

```bash
docker run --rm -it \
    --name=YoloV5Node \
    -e FLASK_RUN_PORT=5000 \
    -p 127.0.0.1:8080:5000 \
    nicescenera.azurecr.io/yolov5node:latest
```

#### Testing the Node

See the [NodeTests repository](https://github.com/Scenerainc/NodeTests). These tests set up a mock NodeSequencer.
