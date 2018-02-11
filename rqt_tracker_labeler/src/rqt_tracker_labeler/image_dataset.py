import rosbag
import cv2
from sensor_msgs.msg import Image
from python_qt_binding.QtWidgets import QDialog,QCheckBox,QHBoxLayout,QPushButton,QProgressBar
from python_qt_binding import QtCore
from cv_bridge import CvBridge, CvBridgeError

class ImageDataset:
    def __init__(self,rosbag_file_path):
        bag = rosbag.Bag(rosbag_file_path)
        image_msg = Image()
        topic_lists = []
        for topic, msg, t in bag.read_messages():
            if msg._get_types() == image_msg._get_types():
                if topic not in topic_lists:
                    topic_lists.append(topic)
        self.dialog = QDialog(None)
        layout = QHBoxLayout()
        self.check_box_list = []
        self.check_box_result = []
        for topic in topic_lists:
            self.check_box_list.append(QCheckBox(topic))
        for check_box in self.check_box_list:
            layout.addWidget(check_box)
        push_button = QPushButton("OK",None)
        push_button.clicked.connect(self.__button_pressed)
        layout.addWidget(push_button)
        self.dialog.setLayout(layout)
        self.dialog.exec_()
        for check_box in self.check_box_list:
            self.check_box_result.append(check_box.checkState())
        read_topic_list = []
        for i in range(len(topic_lists)):
            if self.check_box_result[i] == 2:
                read_topic_list.append(topic_lists[i])
        self.images = self.read_images(read_topic_list, rosbag_file_path)
        bag.close()

    def __button_pressed(self):
        self.dialog.close()

    def read_images(self, read_topic_list, rosbag_file_path):
        images = []
        bag = rosbag.Bag(rosbag_file_path)
        bridge = CvBridge()
        if len(read_topic_list) != 0:
            for read_topic in read_topic_list:
                topic_images = []
                for topic, msg, t in bag.read_messages(topics=read_topic):
                    img = cv2.cvtColor(bridge.imgmsg_to_cv2(msg, "bgr8"),cv2.COLOR_BGR2RGB)
                    topic_images.append(img)
                images.append(topic_images)
        bag.close()
        return images

if __name__ == '__main__':
    pass
