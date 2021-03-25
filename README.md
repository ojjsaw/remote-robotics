# Remote Robotics
OpenVINO Toolkit provides two utilities for quick AI Deployment:
1. **OpenVINO Model Server:** gRPC based Model Serving Container (similar to TFServing)
2. **OpenVINO DL Streamer:** gstreamer based pipeline elements (infer, convert, publish2mqtt) 

## Pre-req for comparison
- single FP16-INT8 pre-trained model that is already available in both approaches.
- same video file with resolution already in target model input size to ensure the data transmitted is similar (e.g. grpc resize on client, vs dlstreamer resized on server)
- ensure clients'/server all are in local docker containers on a private network


## Approach for comparison
```
/**** modelserver flow *****/

// grpc-client.py
while(!EOF)
    readFrame
    transformFrame
    network.exec ---_--img------>
                 <--resultdata--- ModelServerInference
    print currtime


/**** dlStreamer flow ****/

// streamfrmvideo.sh Generate rtp stream from video file via gstreamer

-------rtp-h264/5-stream------> gst decodeFrame
                                gst transformFrame
                                gst inference
                                gst convertresultdata
// client.py <---mqttbroker---- gst mqttpublish
print currtime


/**** Compare *****/

currTimeLast - currTimeFirst = ~totalTimeToProcessVideo (skip-1st-frame)
number of print times = number of frames processed

Outcome: X time taken e2e to process N frames (excluding overheads)
```

## Setup
```
docker pull openvino/model_server:latest
docker pull openvino/ubuntu18_data_dev:latest
docker pull eclipse-mosquitto

# download IR pre-trained from open model zoo
docker run --network host -it --rm -v $(pwd):/workdir -v ~/.Xauthority:/root/.Xauthority -v /tmp/.X11-unix/:/tmp/.X11-unix/ -e DISPLAY=$DISPLAY openvino/ubuntu18_data_dev:latest

cd /workdir/

python3 -m pip install -r grpc-client-requirements.txt

```

```
docker run --network host -d --rm -v $(pwd)/intel:/opt/ml/models/ -p 9000:9000 -p 9001:9001 openvino/model_server:latest --model_path "/opt/ml/models/vehicle-detection-adas-0002" --model_name "vehicle" --port 9000 --rest_port 9001 --log_level ERROR
```

### Example for streamfrmvideo.sh
```
gst-launch-1.0 -v ximagesrc ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5000
```

