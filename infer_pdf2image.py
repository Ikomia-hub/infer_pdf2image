from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits PyDataProcess.CPluginProcessInterface from Ikomia API
# --------------------
class IkomiaPlugin(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def get_process_factory(self):
        # Instantiate algorithm object
        from infer_pdf2image.infer_pdf2image_process import InferPdf2imageFactory
        return InferPdf2imageFactory()

    def get_widget_factory(self):
        # Instantiate associated widget object
        from infer_pdf2image.infer_pdf2image_widget import InferPdf2imageWidgetFactory
        return InferPdf2imageWidgetFactory()
