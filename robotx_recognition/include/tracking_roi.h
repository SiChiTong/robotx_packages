#ifndef TRACKING_ROI_H_INCLUDED
#define TRACKING_ROI_H_INCLUDED

//headers in this package
#include <mouse_param.h>

//headers in opencv
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/tracking/tracker.hpp>

//headers in boost
#include <boost/optional.hpp>
#include <boost/circular_buffer.hpp>

class tracking_roi
{
public:
  tracking_roi();
  ~tracking_roi();
  void clear_roi();
  boost::optional<cv::Rect2d&> get_roi();
  void set_anker_point(mouse_param mouse_event);
private:
  cv::Rect2d roi_;
  volatile bool is_mouse_pressed_;
  boost::circular_buffer<mouse_param> roi_params_;
};
#endif  //TRACKING_ROI_H_INCLUDED
