//headers in this package
#include <tracker_labeler.h>

tracker_labeler::tracker_labeler():it_(nh_)
{
  nh_.param<std::string>(ros::this_node::getName()+"/tracking_algorithm", tracking_algorithm_, "MEDIANFLOW");
  if(tracking_algorithm_ == "MEDIANFLOW")
  {
    tracker_ = cv::TrackerMedianFlow::create();
  }
  else if(tracking_algorithm_ == "MIL")
  {
    tracker_ = cv::TrackerMIL::create();
  }
  else if(tracking_algorithm_ == "BOOSTING")
  {
    tracker_ = cv::TrackerBoosting::create();
  }
  else if(tracking_algorithm_ == "KCF")
  {
    tracker_ = cv::TrackerKCF::create();
  }
  else
  {
    ROS_WARN_STREAM("failed to classify ~/tracking_algorithm parameter set MEDIANFLOW");
    tracker_ = cv::TrackerMedianFlow::create();
  }
  cv::Mat black_img = cv::Mat::zeros(240, 320, CV_8U);
  cv::imshow("tracker_labeler", black_img);
  cv::waitKey(3);
  cv::setMouseCallback("tracker_labeler", mouse_callback, &mouse_event_);
  image_sub_ = it_.subscribe(ros::this_node::getName()+"/image_raw", 1,&tracker_labeler::image_callback, this);
}

tracker_labeler::~tracker_labeler()
{

}

void tracker_labeler::mouse_callback(int event_type, int x, int y, int flags, void* userdata)
{
  mouse_param *ptr = static_cast<mouse_param*>(userdata);
  ptr->x = x;
  ptr->y = y;
  ptr->event = event_type;
  ptr->flags = flags;
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
  tracking_target_roi_.set_anker_point(mouse_event_);
}
