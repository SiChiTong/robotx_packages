//headers in this package
#include <tracker_labeler.h>

//headers for ros
#include <ros/ros.h>

int main(int argc, char *argv[])
{
  ros::init(argc, argv, "tracker_labeler_node");
  tracker_labeler labeler;
  ros::spin();
  return 0;
}
