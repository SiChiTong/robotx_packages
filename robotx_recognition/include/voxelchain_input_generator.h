#ifndef VOXELCHAIN_INPUT_GENERATOR_H_INCLUDED
#define VOXELCHAIN_INPUT_GENERATOR_H_INCLUDED

//headers in this package
#include <robotx_msgs/EuclideanClusters.h>
#include <robotx_msgs/VoxelChainInputs.h>

//headers in ROS
#include <ros/ros.h>

//headers in pcl
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/console/time.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/passthrough.h>
#include <pcl/features/moment_of_inertia_estimation.h>

//headers for openMP
#ifdef _OEPNMP
#include <omp.h>
#endif

class voxelchain_input_generator
{
public:
  voxelchain_input_generator();
  ~voxelchain_input_generator();
  void euclidean_clusters_callback(robotx_msgs::EuclideanClusters msg);
private:
  robotx_msgs::VoxelChainInput generate_voxel_chain_input(sensor_msgs::PointCloud2 cluster_pointcloud);
  pcl::PointCloud<pcl::PointXYZ>::Ptr get_pcl_pointcloud(sensor_msgs::PointCloud2 pointcloud_msg);
  std::array<pcl::PointXYZ,2> get_bounding_box(pcl::PointCloud<pcl::PointXYZ>::Ptr clusterd_pointcloud);
  ros::Subscriber euclidean_clusters_sub_;
  ros::Publisher voxel_chain_input_pub_;
  ros::NodeHandle nh_;
  //paremters
  int threshold_;
};
#endif  //VOXELCHAIN_INPUT_GENERATOR_H_INCLUDED
