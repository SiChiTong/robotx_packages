#!/usr/bin/env python
import rospy
import rospkg
import tensorflow as tf
from robotx_msgs.msg import VoxelChainInputs,VoxelChainInput

class voxelchain_network:
    def __init__(self):
        self.load_network(2)
        self.voxelchain_input_sub = rospy.Subscriber("~voxelchain_input", VoxelChainInputs, self.voxelchain_input_callback)
    def voxelchain_input_callback(self, msg):
        rospy.logerr("hi")
    def truncated_normal_var(self, name, shape, dtype):
        return(tf.get_variable(name=name, shape=shape, dtype=dtype, initializer=tf.truncated_normal_initializer(stddev=0.05)))
    def zero_var(self, name, shape, dtype):
        return(tf.get_variable(name=name, shape=shape, dtype=dtype, initializer=tf.constant_initializer(0.0)))
    def load_network(self,num_class):
        rospack = rospkg.RosPack()
        voxcelchaininput = VoxelChainInput()
        num_partitions = voxcelchaininput.NUMBER_OF_PARTITIONS
        self.session = tf.Session()
        self.input = tf.placeholder(tf.float32, shape=[None, num_partitions*num_partitions*num_partitions])
        self.output = tf.placeholder(tf.float32, shape=[None,num_class])
        self.input_voxcel = tf.reshape(self.input, [-1,num_partitions,num_partitions,num_partitions])
        #Conv1 layer
        with tf.variable_scope('conv1') as scope:
            # Conv_kernel is 3x3 for all 32 channels and we will create 4096 features
            self.conv1_kernel = self.truncated_normal_var(name='conv1_kernel', shape=[3, 3, 32, 512], dtype=tf.float32)
            self.conv1 = tf.nn.conv2d(self.input_voxcel, self.conv1_kernel, strides=[1, 1, 1, 1], padding='SAME')
            # Initialize and add the bias term
            self.conv1_bias = self.zero_var(name='conv1_bias', shape=[512], dtype=tf.float32)
            self.conv1_add_bias = tf.nn.bias_add(self.conv1, self.conv1_bias)
            # ReLU element wise
            self.relu_conv1 = tf.nn.relu(self.conv1_add_bias)
        #Conv2 layer
        with tf.variable_scope('conv2') as scope:
            # Conv_kernel is 3x3 for all 16 channels and we will create 512 features
            self.conv2_input = tf.reshape(self.relu_conv1, [-1,8,8,8])
            self.conv2_kernel = self.truncated_normal_var(name='conv2_kernel', shape=[3, 3, 8, 64], dtype=tf.float32)
            self.conv2 = tf.nn.conv2d(self.conv2_input, self.conv2_kernel, strides=[1, 1, 1, 1], padding='SAME')
            # Initialize and add the bias term
            self.conv2_bias = self.zero_var(name='conv2_bias', shape=[64], dtype=tf.float32)
            self.conv2_add_bias = tf.nn.bias_add(self.conv2, self.conv2_bias)
            # ReLU element wise
            self.relu_conv2 = tf.nn.relu(self.conv2_add_bias)
        #Fully Connected Layer1
        with tf.variable_scope('full1') as scope:
            # Fully connected layer will have 16 outputs.
            self.full1_input = tf.reshape(self.relu_conv2, [-1,64])
            self.full1_weight = self.truncated_normal_var(name='full1_mult', shape=[64, 16], dtype=tf.float32)
            self.full1_bias = self.zero_var(name='full1_bias', shape=[16], dtype=tf.float32)
            self.relu_full1 = tf.nn.relu(tf.add(tf.matmul(self.full1_input, self.full1_weight), self.full1_bias))
        #Fully Connected Layer2
        with tf.variable_scope('full2') as scope:
            # Fully connected layer will have 16 outputs.
            self.full2_input = tf.reshape(self.relu_full1, [-1,16])
            self.full2_weight = self.truncated_normal_var(name='full2_mult', shape=[16, num_class], dtype=tf.float32)
            self.full2_bias = self.zero_var(name='full2_bias', shape=[num_class], dtype=tf.float32)
            self.relu_full2 = tf.nn.relu(tf.add(tf.matmul(self.full2_input, self.full2_weight), self.full2_bias))
        summary_str = self.session.run(tf.global_variables_initializer())
        #summary_writer = tf.summary.FileWriter(rospack.get_path('robotx_recognition')+"/tensorflow_log", self.session.graph)
        #summary_writer.add_summary(summary_str)
        #summary_writer.flush()

if __name__ == '__main__':
    rospy.init_node('voxelchain_node', anonymous=True)
    voxelchain = voxelchain_network()
    rospy.spin()
