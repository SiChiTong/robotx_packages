#ifndef TRACKER_LABELER_H_INCLUDED
#define TRACKER_LABELER_H_INCLUDED

//headers in ROS
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>

//headers in opencv
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

class tracker_labeler
{
public:
  tracker_labeler();
  ~tracker_labeler();
private:
  void image_callback(const sensor_msgs::ImageConstPtr& msg);
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
};
#endif  //TRACKER_LABELER_H_INCLUDED
