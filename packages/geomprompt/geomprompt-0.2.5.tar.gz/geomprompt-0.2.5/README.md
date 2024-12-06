# GeomPrompt

GeomPrompt is a tool for generating point prompts of multi-scale ridge like features for subsequent use with image segmenters like Segment Anything Model (SAM). 
GeomPrompt seeks to distribute a user-specified number of point prompts evenly across salient ridge features. 
The tool was designed to support automated segmentation of plant roots in minirhizotron and rhizotron-type images, however it can be applied to alternate tasks requiring the segmentation of "ridge-like" features. 
Local ridge-like regions are determined as a function the Hessian after applying a Gaussian filter at varying scales.

See the Documentation at http://rootshape.pages.geomdata.com/geomprompt

## Installation

If you just want to run the software, do any of these:

- For the official, stable published version, use `pip install geomprompt`
- For more advanced or customized development options, as well as developer installation instructions, see [CONTRIBUTING.md](CONTRIBUTING.md) and [DEPENDENCIES.md](DEPENDENCIES.md).

## Usage

While GeomPrompt can be utilized to generate point prompts of salient ridge (or valley) like features for general purposes, its outputs are customized to be directly utilized as prompt points for SAM. GeomPrompt's primary interface is the `geomprompt.ridges.RidgePrompts` class, which can be initialized with a target image (when initialized in this way scale space ridge test values are computed for the specific image). The initializing image can be grayscale (1-channel) or RGB (3-channel); in the latter case `RidgePrompts` uses `skimage.color.rgb2gray` to convert the image to grayscale.

```
import numpy as np
from skimage.data import coffee
from geomprompt.ridges.ridge_prompts import RidgePrompts

prompter = RidgePrompts(coffee())
ridge_prompts = prompter.get_prompts(32)
```
In the above, `prompter` returns 32 "salient" ridge prompt points. `ridge_prompts` is a dictionary with keys `batch_prompt_points`, `batch_point_lables`, and `automask_prompts`. `batch_prompt_points` interfaces with SAM's batch prompting and prompt points are in the native image coordinate space. `automask_prompts` interface with SAM's `SamAutomaticMaskGenerator` and are scaled to percentages of the image dimensions.

Prompts can be used directly with SAM assuming `segment-anything` is installed in the environment and a SAM checkpoint is accessible.
```
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

sam_checkpoint = "<path/to/sam_vit_h_4b8939.pth>"
model_type = "vit_h"
device = "cpu" # "cuda"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

sam_geom = SamAutomaticMaskGenerator(
    model=sam,
    pred_iou_thresh=0.6,
    stability_score_thresh=0.8,
    points_per_side=None,
    point_grids=ridge_prompts["automask_prompts"],
)

geom_masks = sam_geom.generate(np.array(coffee()))
```
Usage of the resulting `geom_masks` is documented in `segment-anything`. 

## Features

* pip installable
* testing suite with pytest
* documentation with sphinx
* tests and deployment integrated with gitlab CI/CD

## Credits

This package was initialized with cookiecutter and the `GDA Cookiecutter` project template.

* [GDA Cookiecutter](https://gitlab.geomdata.com/geomdata/gda-cookiecutter/)
* [example Python Boilerplate](https://gitlab.geomdata.com/geomdata/python-boilerplate)
* [Cookiecutter](https://github.com/audreyr/cookiecutter)
