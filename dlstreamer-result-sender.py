from gstgva import VideoFrame
from gi.repository import Gst, GObject
import sys
import gi
import datetime
gi.require_version('Gst', '1.0')

frame_counter = 0
start_time = 0
end_time = 0

DETECT_THRESHOLD = 0.5

Gst.init(sys.argv)

def process_frame(frame: VideoFrame, threshold: float = DETECT_THRESHOLD) -> bool:
    
    global frame_counter
    global start_time
    global end_time

    # for comparison calculation
    end_time = datetime.datetime.now()
    if frame_counter == 0:
        start_time = end_time
    frame_counter += 1

    if frame_counter > 530:
        duration =  '{:.2f} sec'.format((end_time - start_time).total_seconds())       
        print("--------------------------------")
        print("| OpenVINO DLStreamer |")
        print("Total e2e processing time for VideoFile: ", duration)
        print("Num of Frames Processed: ", frame_counter - 1)
        print("Note: 1st frame is excluded in above measurements.")

    return True
