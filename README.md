# remote-robotics

## Run openvino dev container.
```
docker run -it --rm -v $(pwd):/workdir openvino/ubuntu18_dev:latest
```

## Download model
```
 /opt/intel/openvino/deployment_tools/tools/model_downloader/downloader.py --name pedestrian-and-vehicle-detector-adas-0001
```

## Organize for model server
- `mv FP16 1` | `rm -r FP16-IN8` | `rm -r FP32`


## Run model server
```
docker run --network host -d --rm -v $(pwd)/intel:/opt/ml/models/ -p 9000:9000 -p 9001:9001 openvino/model_server:latest --model_path "/opt/ml/models/pedestrian-and-vehicle-detector-adas-0001" --model_name "personvehicle" --port 9000 --rest_port 9001 --log_level DEBUG
```

## Client dev env.
```
docker run --network host -it --rm -v $(pwd):/workdir python:3.8-slim-buster /bin/bash
python -m pip install -r requirements.txt

apt-get update
apt-get install -y libgl1-mesa-dev
apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
```

# Run client commands
```
python3 get_serving_meta.py --grpc_port 9000 --model_name personvehicle --model_version 1
```