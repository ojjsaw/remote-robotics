# Remote Robotics
OpenVINO Toolkit provides two utilities for quick AI Deployment:
1. **OpenVINO Model Server:** gRPC based Model Serving Container (similar to TFServing)
2. **OpenVINO DL Streamer:** gstreamer based pipeline elements (infer, convert, publish2mqtt) 

## Pre-req for comparison
- single pre-trained example model that is already available in both approaches.
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


Example for streamfrmvideo.sh
```
gst-launch-1.0 -v ximagesrc ! video/x-raw,framerate=20/1 ! videoscale ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay ! udpsink host=127.0.0.1 port=5000
```

