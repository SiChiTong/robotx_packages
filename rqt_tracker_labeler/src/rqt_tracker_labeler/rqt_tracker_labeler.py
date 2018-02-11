import os
import rospy
import rospkg
import rosparam

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget,QFileDialog
from python_qt_binding.QtGui import QImage

from object_class import ObjectClass
from image_dataset import ImageDataset
#from python_qt_binding import QtGui

class RqtTrackerLabelerPlugin(Plugin):
    def __init__(self, context):
        super(RqtTrackerLabelerPlugin, self).__init__(context)
        self.__working_dir = ""
        self.__object_class_datas = []
        self.__image_datasets = []
        # Give QObjects reasonable names
        self.setObjectName('RqtTrackerLabelerPlugin')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser
        parser.add_argument("-q", "--quiet", action="store_true",
                            dest="quiet",
                            help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print 'arguments: ', args
            print 'unknowns: ', unknowns

        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file which should be in the "resource" folder of this package
        ui_file = os.path.join(rospkg.RosPack().get_path('rqt_tracker_labeler'), 'resource', 'mainwindow.ui')
        # Extend the widget with all atrributes and children from UI File
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('RqtTrackerLabelerPluginUi')
        # Show _widget.windowTitle on left-top of each plugin(when it's set in _widget).
        # This is useful when you open multiple plugins aat once. Also if you open multiple
        # instances of your plugin at once, these lines add number to make it easy to
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' %d' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)
        #self._widget.cancelButton.clicked[bool].connect(self._handle_cancel_clicked)
        #self._widget.okButton.clicked[bool].connect(self._handle_ok_clicked)
        self._widget.pushButton_load_setting.clicked[bool].connect(self._handle_push_button_load_setting_clicked)
        self._widget.pushButton_load_rosbag_files.clicked[bool].connect(self._handle_load_rosbag_files_clicked)
        self._widget.pushButton_set_save_dir.clicked[bool].connect(self._set_save_dir_clicked)

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.get_value(k, v)
        pass

    def restore_settings(self, pluign_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    def _handle_push_button_load_setting_clicked(self):
        file_path = QFileDialog.getOpenFileName(None, 'Open file to load', directory=rospkg.RosPack().get_path('rqt_tracker_labeler'),
            filter="YAML File (*.yaml)")
        if file_path[0] != u'':
            paramlist = rosparam.load_file(file_path[0])
            del self.__object_class_datas[:]
            self._widget.comboBox_class_name.clear()
            object_classes = []
            for params, ns in paramlist:
                rosparam.upload_params(ns,params)
                key_values = params['rqt_tracker_labeler'].keys()
                for key_value in key_values:
                    object_classes.append(key_value)
                    #params['rqt_tracker_labeler'][key_value]
                    self.__object_class_datas.append(ObjectClass(key_value,params['rqt_tracker_labeler'][key_value]['object_id'],
                        params['rqt_tracker_labeler'][key_value]['tracking_frames']))
            self._widget.comboBox_class_name.addItems(object_classes)

    def _set_save_dir_clicked(self):
        self.__working_dir = QFileDialog.getExistingDirectory(None, 'Open file to load',
            directory=rospkg.RosPack().get_path('rqt_tracker_labeler'))

    def _handle_load_rosbag_files_clicked(self):
        file_path = QFileDialog.getOpenFileName(None, 'Open file to load', directory=os.path.expanduser('~'),filter="ROSBAG File (*.bag)")
        num_images = 0
        self.qimages = []
        self.__image_datasets.append(ImageDataset(file_path[0]))
        for image_dataset in self.__image_datasets:
            for topic_images in image_dataset.images:
                topic_qimages = []
                for image in topic_images:
                    height, width, dim = image.shape
                    topic_qimages.append(QImage(image.data, width, height, dim * width, QImage.Format_RGB888))
                    num_images = num_images + 1
                self.qimages.append(topic_images)
