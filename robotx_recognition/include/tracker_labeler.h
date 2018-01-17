#ifndef TRACKER_LABELER_H_INCLUDED
#define TRACKER_LABELER_H_INCLUDED

//headers in this package
#include <mouse_param.h>
#include <tracking_roi.h>

//headers in ROS
#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>

//headers in opencv
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/tracking/tracker.hpp>

class tracker_labeler
{
public:
  tracker_labeler();
  ~tracker_labeler();
private:
  void image_callback(const sensor_msgs::ImageConstPtr& msg);
  static void mouse_callback(int event_type, int x, int y, int flags, void* userdata);
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  //tracker and parameters
  cv::Ptr<cv::Tracker> tracker_;
  std::string tracking_algorithm_;
  tracking_roi tracking_target_roi_;
  //mouse callback ant parameters
  mouse_param mouse_event_;
};
#endif  //TRACKER_LABELER_H_INCLUDED
