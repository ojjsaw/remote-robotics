# remote-robotics

## Run openvino dev container to download model.
```
docker run --network host -it --rm -v $(pwd):/workdir openvino/ubuntu18_dev:latest
cd /workdir/
 /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name pedestrian-and-vehicle-detector-adas-0001
```

## Organize for model server
- `mv FP16-IN8 1` | `rm -r FP16` | `rm -r FP32`


## Run model server
```
docker run --network host -d --rm -v $(pwd)/intel:/opt/ml/models/ -p 9000:9000 -p 9001:9001 openvino/model_server:latest --model_path "/opt/ml/models/pedestrian-and-vehicle-detector-adas-0001" --model_name "personvehicle" --port 9000 --rest_port 9001 --log_level ERROR
```
- "DEBUG"/"INFO"/"ERROR" https://github.com/openvinotoolkit/model_server/blob/main/docs/docker_container.md
- `--cpuset-cpus 0,1,2,3` and other params
- https://github.com/openvinotoolkit/model_server/blob/main/docs/performance_tuning.md 

## Client dev env.
```
docker run --network host -it --rm -v $(pwd):/workdir devclient:grpc /bin/bash
```


# Run client commands
```
python3 get_serving_meta.py --grpc_port 9000 --model_name personvehicle --model_version 1
python3 grpc-client-img.py

```

## Parallel multi model
https://github.com/openvinotoolkit/model_server/blob/main/docs/combined_model_dag.md 

## Build client docker image
```
cd client/
docker build -f Dockerfile.client -t devclient:grpc .
```
**Note:** For WSL2 docker build errors run once,  `sudo hwclock --hctosys`


## Client Dev Envr. manual
```
docker run --network host -it --rm -v $(pwd):/workdir python:3.8-slim-buster /bin/bash
cd /workdir/client
python -m pip install -r requirements.txt

apt-get update
apt-get install -y libgl1-mesa-dev
apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
```

# DLStreamer

```
docker run --network host -it --rm -v $(pwd):/workdir openvino/ubuntu18_data_dev:latest
cd /workdir/
```

```
docker run --network host -d --rm --name dlstreamer_mqtt -p 1883:1883 -p 9001:9001 eclipse-mosquitto
docker exec -it dlstreamer_mqtt sh
mosquitto_sub -h localhost -t dlstreamer
```

```
# in data dev openvino container
./metapublish.sh https://github.com/intel-iot-devkit/sample-videos/raw/master/head-pose-face-detection-female-and-male.mp4 mqtt
```