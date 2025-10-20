from ikomia import core, dataprocess
from ikomia.utils import pyqtutils, qtconversion
from infer_pdf2image.infer_pdf2image_process import InferPdf2imageParam

from PyQt5.QtWidgets import *

# pylint: disable=import-error,no-member

# PyQt GUI framework
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QLabel, QComboBox


# --------------------
# - Class which implements widget associated with the algorithm
# - Inherits PyCore.CWorkflowTaskWidget from Ikomia API
# --------------------
class InferPdf2imageWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = InferPdf2imageParam()
        else:
            self.parameters = param

        # Create layout : QGridLayout by default
        self.grid_layout = QGridLayout()

        # Input PDF path
        self.edit_input_path = pyqtutils.append_browse_file(self.grid_layout,
                                                              label="Input PDF path",
                                                              file_filter="*.pdf",
                                                              path=self.parameters.input_path,
                                                              )

        # Output folder
        self.edit_output_folder = pyqtutils.append_browse_file(self.grid_layout,
                                                              label="Output folder",
                                                              file_filter="",
                                                              path=self.parameters.output_folder,
                                                              mode=QFileDialog.Directory)
        # self.edit_output_folder = pyqtutils.append_edit(
        #     self.grid_layout, "Output folder", self.parameters.output_folder)

        # Output base filename (without extension)
        self.edit_output_file = pyqtutils.append_edit(
            self.grid_layout, "Output base name", self.parameters.output_file)

        # DPI
        self.spin_dpi = pyqtutils.append_spin(
            self.grid_layout, "DPI", self.parameters.dpi, min=50, max=1200)

        # First / Last page (0 = auto)
        self.spin_first_page = pyqtutils.append_spin(
            self.grid_layout, "First page (0=auto)", int(self.parameters.first_page) if str(self.parameters.first_page).isdigit() else 0, min=0, max=100000)
        self.spin_last_page = pyqtutils.append_spin(
            self.grid_layout, "Last page (0=auto)", int(self.parameters.last_page) if str(self.parameters.last_page).isdigit() else 0, min=0, max=100000)

        # Thread count
        self.spin_thread_count = pyqtutils.append_spin(
            self.grid_layout, "Thread count", self.parameters.thread_count, min=1, max=64)

        # User / Owner password
        self.edit_userpw = pyqtutils.append_edit(
            self.grid_layout, "User password", self.parameters.userpw)
        self.edit_ownerpw = pyqtutils.append_edit(
            self.grid_layout, "Owner password", self.parameters.ownerpw)
        # Hide password text in UI
        try:
            self.edit_userpw.setEchoMode(QLineEdit.Password)
            self.edit_ownerpw.setEchoMode(QLineEdit.Password)
        except AttributeError:
            pass

        #Transparent, Single file, Grayscale
        self.check_transparent = pyqtutils.append_check(
            self.grid_layout, "Transparent", self.parameters.transparent)
        self.check_single_file = pyqtutils.append_check(
            self.grid_layout, "Single file output", self.parameters.single_file)
        self.check_grayscale = pyqtutils.append_check(
            self.grid_layout, "Grayscale", self.parameters.grayscale)

        # Poppler path
        self.edit_poppler_path = pyqtutils.append_edit(
            self.grid_layout, "Poppler path", self.parameters.poppler_path)

        # Image format selector
        row = self.grid_layout.rowCount()
        self.grid_layout.addWidget(QLabel("Image format"), row, 0)
        self.combo_format = QComboBox()
        self.combo_format.addItems(["png", "jpg", "jpeg", "tiff", "ppm", "bmp"])
        try:
            current_format = str(self.parameters.format) if self.parameters.format else "png"
            index = self.combo_format.findText(current_format)
            if index >= 0:
                self.combo_format.setCurrentIndex(index)
        except AttributeError:
            pass
        self.grid_layout.addWidget(self.combo_format, row, 1)

        # Image size (0 = auto)
        self.spin_img_size = pyqtutils.append_spin(
            self.grid_layout, "Image size (px, 0=auto)", int(self.parameters.img_size) if str(self.parameters.img_size).isdigit() else 0, min=0, max=20000)

        # PyQt -> Qt wrapping
        layout_ptr = qtconversion.PyQtToQt(self.grid_layout)

        # Set widget layout
        self.set_layout(layout_ptr)

    def on_apply(self):
        # Apply button clicked slot

        # Get parameters from widget
        self.parameters.input_path = self.edit_input_path.path
        self.parameters.output_folder = self.edit_output_folder.path
        self.parameters.output_file = self.edit_output_file.text()

        self.parameters.dpi = self.spin_dpi.value()
        self.parameters.thread_count = self.spin_thread_count.value()

        first_page_val = self.spin_first_page.value()
        last_page_val = self.spin_last_page.value()
        self.parameters.first_page = first_page_val if first_page_val > 0 else ""
        self.parameters.last_page = last_page_val if last_page_val > 0 else ""

        self.parameters.userpw = self.edit_userpw.text()
        self.parameters.ownerpw = self.edit_ownerpw.text()

        self.parameters.transparent = self.check_transparent.isChecked()
        self.parameters.single_file = self.check_single_file.isChecked()
        self.parameters.grayscale = self.check_grayscale.isChecked()

        self.parameters.poppler_path = self.edit_poppler_path.text()

        self.parameters.format = self.combo_format.currentText()

        img_size_val = self.spin_img_size.value()
        self.parameters.img_size = img_size_val if img_size_val > 0 else ""

        # Send signal to launch the algorithm main function
        self.emit_apply(self.parameters)


# --------------------
# - Factory class to build algorithm widget object
# - Inherits PyDataProcess.CWidgetFactory from Ikomia API
# --------------------
class InferPdf2imageWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the algorithm name attribute -> it must be the same as the one declared in the algorithm factory class
        self.name = "infer_pdf2image"

    def create(self, param):
        # Create widget object
        return InferPdf2imageWidget(param, None)
