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

std::vector<cv::Point> tracking_roi::get_anker_points()
{
  std::vector<cv::Point> anker_points = std::vector<cv::Point>(roi_params_.size());
  for(int i = 0; i < anker_points.size() ; i++)
  {
    anker_points[i].x = roi_params_[i].x;
    anker_points[i].y = roi_params_[i].y;
  }
  return anker_points;
}

boost::optional<cv::Rect2d&> tracking_roi::get_roi()
{
  if(roi_params_.size() == 2)
  {
    int top_left_x = std::min(roi_params_[0].x,roi_params_[1].x);
    int top_left_y = std::min(roi_params_[0].y,roi_params_[1].y);
    int width = std::abs(roi_params_[0].x-roi_params_[1].x);
    int height = std::abs(roi_params_[0].y-roi_params_[1].y);
    roi_ = cv::Rect2d{top_left_x, top_left_y, width, height};
    return roi_;
  }
  else
  {
    return boost::none;
  }
}
