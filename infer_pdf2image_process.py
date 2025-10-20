import copy
import os
import uuid
from datetime import datetime
import numpy as np
from ikomia import core, dataprocess, utils
from pdf2image import convert_from_path


# --------------------
# - Class to handle the algorithm parameters
# - Inherits PyCore.CWorkflowTaskParam from Ikomia API
# --------------------
class InferPdf2imageParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # Place default value initialization here
        self.input_path = ""
        self.dpi = 200
        self.output_folder = ""
        self.first_page = ""
        self.last_page = ""
        self.thread_count = 1
        self.userpw = ""
        self.ownerpw = ""
        self.transparent = False
        self.single_file = False
        self.poppler_path = ""
        self.output_file = ""
        self.grayscale = False
        self.format = "png"
        self.img_size = ""


    def set_values(self, params):
        # Set parameters values from Ikomia Studio or API
        # Parameters values are stored as string and accessible like a python dict
        # Example : self.window_size = int(params["window_size"])
        self.input_path = params["input_path"]
        self.dpi = int(params["dpi"])
        self.output_folder = params["output_folder"]
        self.first_page = int(params["first_page"]) if params["first_page"] else ""
        self.last_page = int(params["last_page"]) if params["last_page"] else ""
        self.thread_count = int(params["thread_count"])
        self.userpw = params["userpw"]
        self.ownerpw = params["ownerpw"]
        self.transparent = utils.strtobool(params["transparent"])
        self.single_file = utils.strtobool(params["single_file"])
        self.output_file = params["output_file"]
        self.poppler_path = str(params["poppler_path"])
        self.grayscale = utils.strtobool(params["grayscale"])
        self.format = str(params["format"])
        self.img_size = int(params["img_size"]) if params["img_size"] else ""


    def get_values(self):
        # Send parameters values to Ikomia Studio or API
        # Create the specific dict structure (string container)
        params = {}
        params["input_path"] = str(self.input_path)
        params["dpi"] = str(self.dpi)
        params["output_folder"] = str(self.output_folder)
        params["first_page"] = str(self.first_page)
        params["last_page"] = str(self.last_page)
        params["thread_count"] = str(self.thread_count)
        params["userpw"] = str(self.userpw)
        params["ownerpw"] = str(self.ownerpw)
        params["transparent"] = str(self.transparent)
        params["single_file"] = str(self.single_file)
        params["output_file"] = str(self.output_file)
        params["poppler_path"] = str(self.poppler_path)
        params["grayscale"] = str(self.grayscale)
        params["format"] = str(self.format)
        params["img_size"] = str(self.img_size)
        return params


# --------------------
# - Class which implements the algorithm
# - Inherits PyCore.CWorkflowTask or derived from Ikomia API
# --------------------
class InferPdf2image(core.CWorkflowTask):

    def __init__(self, name, param):
        core.CWorkflowTask.__init__(self, name)
        self.add_output(dataprocess.CImageIO())

        # Create parameters object
        if param is None:
            self.set_param_object(InferPdf2imageParam())
        else:
            self.set_param_object(copy.deepcopy(param))

        self.base_dir = os.path.dirname(os.path.realpath(__file__))

    def get_progress_steps(self):
        # Function returning the number of progress steps for this algorithm
        # This is handled by the main progress bar of Ikomia Studio
        return 1

    def run(self):
        # Main function of your algorithm
        # Call begin_task_run() for initialization
        self.begin_task_run()

        param = self.get_param_object()

        if param.output_folder == "":
            date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            param.output_folder = os.path.join(
                self.base_dir, "output", date_time)
            os.makedirs(param.output_folder, exist_ok=True)

        if param.output_folder != "":
            if not os.path.exists(param.output_folder):
                os.makedirs(param.output_folder)


        if os.path.isfile(param.input_path):
            # Prepare arguments for convert_from_path
            convert_args = {
                'dpi': param.dpi,
                'thread_count': param.thread_count,
                'transparent': param.transparent,
                'single_file': param.single_file,
                'grayscale': param.grayscale,
            }

            # Only add parameters if they're not None
            if param.first_page:
                convert_args['first_page'] = param.first_page
            if param.last_page:
                convert_args['last_page'] = param.last_page
            if param.userpw:
                convert_args['userpw'] = param.userpw
            if param.ownerpw:
                convert_args['ownerpw'] = param.ownerpw
            if param.poppler_path:
                convert_args['poppler_path'] = param.poppler_path
            if param.img_size:
                convert_args['size'] = param.img_size

            output_images = convert_from_path(param.input_path, **convert_args)
        else:
            raise ValueError("Input path is not a file")

        # Set image output
        base_filename = (
            param.output_file.strip()
            if isinstance(param.output_file, str) and param.output_file.strip()
            else os.path.splitext(
                os.path.basename(param.input_path)
            )[0]
        )

        if len(output_images) > 1:
            for i, image in enumerate(output_images):
                self.add_output(dataprocess.CImageIO())
                img = np.array(image)
                output = self.get_output(i)
                output.set_image(img)
                image.save(os.path.join(
                    param.output_folder,
                    f"{base_filename}_{i}.{param.format}",
                ))
        else:
            image = np.array(output_images[0])
            output_img = self.get_output(0)
            output_img.set_image(image)
            output_images[0].save(os.path.join(
                param.output_folder,
                f"{base_filename}.{param.format}",
            ))


        # Step progress bar (Ikomia Studio):
        self.emit_step_progress()

        # Call end_task_run() to finalize process
        self.end_task_run()


# --------------------
# - Factory class to build process object
# - Inherits PyDataProcess.CTaskFactory from Ikomia API
# --------------------
class InferPdf2imageFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set algorithm information/metadata here
        self.info.name = "infer_pdf2image"
        self.info.short_description = "Convert PDF to image"
        # relative path -> as displayed in Ikomia Studio algorithm tree
        self.info.path = "Plugins/Python/Other"
        self.info.version = "1.0.0"
        # self.info.icon_path = "your path to a specific icon"
        self.info.authors = "Belval"
        self.info.article = ""
        self.info.journal = ""
        self.info.year = 2024
        self.info.license = ""

        # Ikomia API compatibility
        self.info.min_ikomia_version = "0.14.0"
        # self.info.max_ikomia_version = "0.11.1"

        # Python compatibility
        self.info.min_python_version = "3.8.0"

        # self.info.max_python_version = "3.11.0"

        # URL of documentation
        self.info.documentation_link = "https://belval.github.io/pdf2image/"

        # Code source repository
        self.info.repository = ""
        self.info.original_repository = "https://github.com/Belval/pdf2image"

        # Keywords used for search
        self.info.keywords = "PDF converter,PDF to images"

        # General type: INFER, TRAIN, DATASET or OTHER
        self.info.algo_type = core.AlgoType.OTHER

        # Algorithms tasks: CLASSIFICATION, COLORIZATION, IMAGE_CAPTIONING, IMAGE_GENERATION,
        # IMAGE_MATTING, INPAINTING, INSTANCE_SEGMENTATION, KEYPOINTS_DETECTION,
        # OBJECT_DETECTION, OBJECT_TRACKING, OCR, OPTICAL_FLOW, OTHER, PANOPTIC_SEGMENTATION,
        # SEMANTIC_SEGMENTATION or SUPER_RESOLUTION
        self.info.algo_tasks = "OTHER"

        # Min hardware config
        self.info.hardware_config.min_cpu = 4
        self.info.hardware_config.min_ram = 16
        self.info.hardware_config.gpu_required = False
        self.info.hardware_config.min_vram = 6

    def create(self, param=None):
        # Create algorithm object
        return InferPdf2image(self.info.name, param)
