//headers in this package
#include <tracking_roi.h>
#include <ros/ros.h>

tracking_roi::tracking_roi()
{
  is_mouse_pressed_ = false;
  roi_params_ = boost::circular_buffer<mouse_param>(2);
}

tracking_roi::~tracking_roi()
{

}

void tracking_roi::clear_roi()
{
  roi_ = cv::Rect2d();
  roi_params_.clear();
  ROS_INFO_STREAM("clear tracking ROI");
}

void tracking_roi::set_anker_point(mouse_param mouse_event)
{
  if(mouse_event.event == cv::EVENT_LBUTTONDOWN)
  {
    is_mouse_pressed_ = true;
  }
  if(mouse_event.event == cv::EVENT_LBUTTONUP)
  {
    if(is_mouse_pressed_ == true)
    {
      if(mouse_event.flags == cv::EVENT_FLAG_LBUTTON)
      {
        roi_params_.push_back(mouse_event);
      }
      if(mouse_event.flags == (cv::EVENT_FLAG_SHIFTKEY+cv::EVENT_FLAG_LBUTTON))
      {
        clear_roi();
      }
    }
    is_mouse_pressed_ = false;
  }
}

boost::optional<cv::Rect2d&> tracking_roi::get_roi()
{
  if(roi_params_.size() == 2)
  {
    return roi_;
  }
  else
  {
    return boost::none;
  }
}
