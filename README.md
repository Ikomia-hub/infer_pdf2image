<div align="center">
  <img src="images/icon.png" alt="Algorithm icon">
  <h1 align="center">infer_pdf2image</h1>
</div>
<br />
<p align="center">
    <a href="https://github.com/Ikomia-hub/infer_pdf2image">
        <img alt="Stars" src="https://img.shields.io/github/stars/Ikomia-hub/infer_pdf2image">
    </a>
    <a href="https://app.ikomia.ai/hub/">
        <img alt="Website" src="https://img.shields.io/website/http/app.ikomia.ai/en.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Ikomia-hub/infer_pdf2image/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/Ikomia-hub/infer_pdf2image.svg?color=blue">
    </a>    
    <br>
    <a href="https://discord.com/invite/82Tnw9UGGc">
        <img alt="Discord community" src="https://img.shields.io/badge/Discord-white?style=social&logo=discord">
    </a> 
</p>

Convert each page of a PDF into images using [pdf2image](https://belval.github.io/pdf2image/) (Poppler backend). 

- **What it does**: Loads a `.pdf` file and produces one image per page, returning images as task outputs and saving them to disk.
- **Why use it**: Batch-convert PDFs into `png`, `jpg`, `tiff`, etc., with control over DPI, page range, grayscale, transparency, and more.

## :gear: Prerequisites (Poppler)

This algorithm relies on Poppler. If Poppler is not on your system `PATH`, you must provide its location via the `poppler_path` parameter.

- Windows: Install Poppler from the [Poppler for Windows releases](https://github.com/oschwartz10612/poppler-windows/releases/) and set `poppler_path` to the `bin` folder (e.g., `C:/Users/me/Tools/poppler-XX/bin`).
- macOS: `brew install poppler`
- Linux: Use your package manager (e.g., `sudo apt install poppler-utils`).

If you encounter `PDFInfoNotInstalledError` or `PDFPageCountError`, ensure Poppler is installed and reachable.

## :rocket: Use with Ikomia API

#### 1) Install Ikomia API and Python dependency

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2) Create your workflow and run

```python
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="infer_pdf2image", auto_connect=True)

# Set parameters (all values are strings)
algo.set_parameters({
    "input_path": "path/to/document.pdf",
    "dpi": "200",                  # 50-1200
    "output_folder": "",           # leave empty for auto timestamped folder
    "output_file": "",             # base name without extension; default = pdf name
    "first_page": "",              # leave empty for auto
    "last_page": "",               # leave empty for auto
    "thread_count": "1",
    "userpw": "",                  # PDF password (user)
    "ownerpw": "",                 # PDF password (owner)
    "transparent": "False",        # for formats that support alpha
    "single_file": "False",        # forwarded to pdf2image
    "grayscale": "False",
    "format": "png",               # png|jpg|jpeg|tiff|ppm|bmp
    "img_size": "",               # integer height in px; empty = auto
    "poppler_path": ""            # set on Windows if Poppler not in PATH
})

# Run the workflow
wf.run()
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.

- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).
- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Parameters

- **input_path** (str): Path to the input PDF file. Required.
- **dpi** (int as string, default `200`): Rendering resolution (50–1200).
- **output_folder** (str, default empty): Destination folder. Empty uses `infer_pdf2image/output/<timestamp>/`.
- **output_file** (str, default empty): Base filename (without extension). Empty uses the PDF base name.
- **first_page** (int as string, default empty): First page to render. Empty = auto.
- **last_page** (int as string, default empty): Last page to render. Empty = auto.
- **thread_count** (int as string, default `1`): Number of rendering threads.
- **userpw** (str): PDF user password if required.
- **ownerpw** (str): PDF owner password if required.
- **transparent** (bool as string, default `False`): Enable alpha channel when supported.
- **single_file** (bool as string, default `False`): Uses the -singlefile option from pdftoppm/pdftocairo.
- **grayscale** (bool as string, default `False`): Render pages in grayscale.
- **format** (str, default `png`): One of `png`, `jpg`, `jpeg`, `tiff`, `ppm`, `bmp`.
- **img_size** (int as string, default empty): Target max dimension in pixels (see pdf2image `size`). Empty = auto.
- **poppler_path** (str, default empty): Path to Poppler `bin` (Windows), or leave empty if Poppler is on `PATH`.

## :mag: Explore algorithm outputs

Every algorithm produces specific outputs, yet they can be explored them the same way using the Ikomia API. For a more in-depth understanding of managing algorithm outputs, please refer to the [documentation](https://ikomia-dev.github.io/python-api-documentation/advanced_guide/IO_management.html).

```python
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="infer_pdf2image", auto_connect=True)

# Configure and run
algo.set_parameters({
    "input_path": "path/to/document.pdf"
})
wf.run()

# Iterate over outputs
for output in algo.get_outputs():
    # Print information
    print(output)
    # Export it to JSON
    output.to_json()
```

## :fast_forward: Notes and tips

- If you process multi-page PDFs, the node returns one image output per page and saves them as `base_<index>.<ext>`.
- On Windows, set `poppler_path` if Poppler is not added to your `PATH` environment variable.
