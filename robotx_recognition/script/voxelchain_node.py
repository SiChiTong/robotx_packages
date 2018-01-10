#!/usr/bin/env python
import rospy
import tensorflow
from robotx_msgs.msg import VoxelChainInputs

class voxelchain_network:
    def __init__(self):
        self.voxelchain_input_sub = rospy.Subscriber("~voxelchain_input", VoxelChainInputs, self.voxelchain_input_callback)
    def voxelchain_input_callback(self,msg):
        rospy.logerr("hi")

if __name__ == '__main__':
    rospy.init_node('voxelchain_node', anonymous=True)
    voxelchain = voxelchain_network()
    rospy.spin()
