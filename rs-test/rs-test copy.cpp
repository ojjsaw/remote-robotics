#include <librealsense2/rs.hpp>
#include <librealsense2/hpp/rs_internal.hpp>
#include <iostream>
#include <librealsense2-net/rs_net.hpp>

int main()
{
    rs2::net_device dev("10.0.0.59");

    rs2::context ctx;
    dev.add_to(ctx);
    
    std::cout << "hello from librealsense - " << RS2_API_VERSION_STR << std::endl;
    std::cout << "You have " << ctx.query_devices().size() << " RealSense devices connected" << std::endl;

    return 0;
}