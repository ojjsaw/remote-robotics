// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
#include <opencv2/opencv.hpp>   // Include OpenCV API
#include <librealsense2-net/rs_net.hpp>

int main(int argc, char * argv[]) try
{
    rs2::net_device dev("10.0.0.59:50001");
    rs2::context ctx;
    dev.add_to(ctx);

    // Declare depth colorizer for pretty visualization of depth data
    rs2::colorizer color_map;

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe(ctx);
    
    rs2::config cfg;
    cfg.enable_stream(RS2_STREAM_DEPTH);
    cfg.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
    pipe.start(cfg);

    // Start streaming with default recommended configuration
    //pipe.start();

    using namespace cv;
    const auto window_name = "Spot DEPTH";
    namedWindow(window_name, WINDOW_AUTOSIZE);

    while (waitKey(1) < 0 && getWindowProperty(window_name, WND_PROP_AUTOSIZE) >= 0)
    {
        rs2::frameset data = pipe.wait_for_frames(); // Wait for next set of frames from the camera
        rs2::frame depth = data.get_depth_frame().apply_filter(color_map);
        rs2::frame color = data.get_color_frame();

        // Query frame size (width and height)
        const int w_depth = depth.as<rs2::video_frame>().get_width();
        const int h_depth = depth.as<rs2::video_frame>().get_height();
        const int w_color = color.as<rs2::video_frame>().get_width();
        const int h_color = color.as<rs2::video_frame>().get_height();
        
        // Create OpenCV matrix of size (w,h) from the colorized depth data
        Mat depth_mat(Size(w_depth, h_depth), CV_8UC3, (void*)depth.get_data(), Mat::AUTO_STEP);
        Mat color_mat(Size(w_color, h_color), CV_8UC3, (void*)color.get_data(), Mat::AUTO_STEP);

        // Update the window with new data
        imshow(window_name, depth_mat);
        imshow("Spot RGB", color_mat);
    }

    return EXIT_SUCCESS;
}
catch (const rs2::error & e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch (const std::exception& e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}
