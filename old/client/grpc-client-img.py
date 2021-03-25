import cv2, datetime, grpc
import numpy as np

from tensorflow import make_tensor_proto, make_ndarray
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

address = "{}:{}".format("127.0.0.1",9000)
width = 672
height = 384
green = (0, 255, 0)
red = (0, 0, 255)
channel = grpc.insecure_channel(address)

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

img = cv2.imread("./test.jpg").astype(np.float32)  # BGR color format, shape HWC
img = cv2.resize(img, (width,height)) # h, w of target model input
img = img.transpose(2,0,1).reshape(1,3,height,width) # change shape to NCHW

request = predict_pb2.PredictRequest()

request.model_spec.name = "personvehicle"
request.inputs["data"].CopyFrom(make_tensor_proto(img, shape=(img.shape)))

start_time = datetime.datetime.now()
result = stub.Predict(request, 10.0) # result includes a dictionary with all model outputs
end_time = datetime.datetime.now()

output = make_ndarray(result.outputs["detection_out"])
print("Response shape", output.shape)

img_out = img[0,:,:,:]
img_out = img_out.transpose(1,2,0)
curr_color = green

for i in range (0, 200):
    detection = output[:,:,i,:]
    #print("Confidence", detection[0,0,2] )
    #print("LabelID", detection[0,0,1] )

    if detection[0,0,2] > 0.5:
        x_min = int(detection[0,0,3] * width)
        y_min = int(detection[0,0,4] * height)
        x_max = int(detection[0,0,5] * width)
        y_max = int(detection[0,0,6] * height)

        info = '{:.2f} '.format(detection[0,0,2])
        if detection[0,0,1] == 1:
            curr_color = red
        elif detection[0,0,1] == 2:
            curr_color = green

        img_out = cv2.rectangle(cv2.UMat(img_out),(x_min,y_min),(x_max,y_max),curr_color,1)
        cv2.putText(img_out,info, (x_min+5,y_min+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, curr_color, 2)

duration =  '{:.2f} ms'.format((end_time - start_time).total_seconds() * 1000)       
cv2.putText(img_out,duration, (10,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
cv2.imwrite("result.jpg", img_out)



