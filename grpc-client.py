import cv2, datetime, grpc
import numpy as np
from tensorflow import make_tensor_proto, make_ndarray
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

address = "{}:{}".format("127.0.0.1",9000)
video_file = "test.mp4"
width = 672
height = 384
green = (0, 255, 0)
frame_counter = 0
start_time = 0
end_time = 0

channel = grpc.insecure_channel(address)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
request = predict_pb2.PredictRequest()
request.model_spec.name = "vehicle"

cap = cv2.VideoCapture(video_file)

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == False:
        break

    img = frame.astype(np.float32)  # BGR color format, shape HWC
    img = cv2.resize(img, (width,height)) # h, w of target model input
    img = img.transpose(2,0,1).reshape(1,3,height,width) # change shape to NCHW

    request.inputs["data"].CopyFrom(make_tensor_proto(img, shape=(img.shape)))
    result = stub.Predict(request, 10.0) # result includes a dictionary with all model outputs

    # for comparison calculation
    end_time = datetime.datetime.now()
    if frame_counter == 0:
        start_time = end_time
    frame_counter += 1

    # display section for debugging only
    # output = make_ndarray(result.outputs["detection_out"])
    # img_out = frame
    # for i in range (0, 200):
    #     detection = output[:,:,i,:]
    #     if detection[0,0,2] > 0.1: #threshold
    #         x_min = int(detection[0,0,3] * width)
    #         y_min = int(detection[0,0,4] * height)
    #         x_max = int(detection[0,0,5] * width)
    #         y_max = int(detection[0,0,6] * height)
    #         info = '{:.2f} '.format(detection[0,0,2])
    #         if detection[0,0,1] == 1:
    #             img_out = cv2.rectangle(cv2.UMat(img_out),(x_min,y_min),(x_max,y_max),green,1)
    #             cv2.putText(img_out,info, (x_min+5,y_min+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 2) 
    # cv2.imshow('frame',img_out)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break    

duration =  '{:.2f} sec'.format((end_time - start_time).total_seconds())       
print("--------------------------------")
print("| OpenVINO Model Server - gRPC |")
print("Total e2e processing time for VideoFile: ", duration)
print("Num of Frames Processed: ", frame_counter - 1)
print("Note: 1st frame is excluded in above measurements.")

cap.release()
cv2.destroyAllWindows()