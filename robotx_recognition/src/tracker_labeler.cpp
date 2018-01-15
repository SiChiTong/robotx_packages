//headers in this package
#include <tracker_labeler.h>

tracker_labeler::tracker_labeler():it_(nh_)
{
  image_sub_ = it_.subscribe(ros::this_node::getName()+"/image_raw", 1,&tracker_labeler::image_callback, this);
}

tracker_labeler::~tracker_labeler()
{

}

void tracker_labeler::image_callback(const sensor_msgs::ImageConstPtr& msg)
{
  cv_bridge::CvImagePtr cv_ptr;
  try
  {
    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
  }
  catch (cv_bridge::Exception& e)
  {
    ROS_ERROR("cv_bridge exception: %s", e.what());
    return;
  }
  cv::imshow("tracker_labeler", cv_ptr->image);
  cv::waitKey(3);
}
