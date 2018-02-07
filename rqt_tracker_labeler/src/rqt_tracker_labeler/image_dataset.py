import rosbag
import cv2
from sensor_msgs.msg import Image
from python_qt_binding.QtWidgets import QDialog,QCheckBox,QHBoxLayout,QPushButton
from python_qt_binding import QtCore

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
        for topic in topic_lists:
            self.check_box_list.append(QCheckBox(topic))
        for check_box in self.check_box_list:
            layout.addWidget(check_box)
        push_button = QPushButton("OK",None)
        push_button.clicked.connect(self.__button_pressed)
        layout.addWidget(push_button)
        self.dialog.setLayout(layout)
        self.dialog.exec_()
        bag.close()

    def __button_pressed(self):
        self.dialog.destroy()

    def __checked(self, int):
        print "hi"

if __name__ == '__main__':
    pass
