"""Run Segment Anything model using geomtric or grid prompting."""
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image
from segment_anything import SamAutomaticMaskGenerator

from .io import save_prompt_experiment
from .ridge_prompts import RidgePrompts


def geom_prompt_and_segment(
    cim: np.ndarray | Image.Image,
    scales: list[int],
    pcounts: list[int],
    model,
    pred_iou: float,
    stability_thresh: float,
    save_exp: bool = False,
    save_name: Optional[str | Path] = None,
):
    """Compute Ridge prompts and run Sam Automatic Mask Generator.

    :param cim: Image to segment
    :type cim: PIL.Image
    :param scales: Scales at which to run RidgePrompts
    :type scales: list[int]
    :param pcounts: Number of prompt points to generate
    :type pcounts: list[int]
    :param model: Loaded Sam model checkpoint
    :type model: _type_
    :param pred_iou: Exclude masks with a predicted score from the model is lower than this threshold.
    :type pred_iou: float
    :param stability_thresh: Exclude masks with a stability score lower than this threshold
    :type stability_thresh: float
    :param save_exp: Whether to save experiment result to a file.
    :type save_exp: bool
    :param save_name: Name of save file.
    :type save_name: str | Path
    :return: _description_
    :rtype: _type_
    """
    prompter = RidgePrompts(cim, scales=scales, method="sq-pcd", threads=8)
    geom_prompts = []
    for count in pcounts:
        geom_prompts.append(prompter.get_prompts(ridge_prompt_count=count))

    geom_masks_collect = []
    for prompt, count in zip(geom_prompts, pcounts):
        sam_geom = SamAutomaticMaskGenerator(
            model=model,
            pred_iou_thresh=pred_iou,
            stability_score_thresh=stability_thresh,
            points_per_side=None,
            point_grids=prompt["automask_prompts"],
        )
        geom_masks = sam_geom.generate(np.array(cim))
        geom_masks_collect.append(geom_masks)

        if save_exp:
            save_prompt_experiment(
                name=save_name + str(count),
                target_path="../data/outputs",
                mask_lists=[geom_masks],
                prompt_counts=[count],
            )

    return geom_masks_collect


def grid_prompt_and_segment(
    cim: np.ndarray | Image.Image,
    scales: list[int],
    pcounts: list[int],
    model,
    pred_iou: float,
    stability_thresh: float,
    save_exp: bool = False,
    save_name: Optional[str | Path] = None,
):
    """Run Sam Automatic Mask Generator with default grid prompts.

    :param cim: Image to segment
    :type cim: PIL.Image
    :param scales: Scales at which to run RidgePrompts
    :type scales: list[int]
    :param pcounts: Number of prompt points to generate
    :type pcounts: list[int]
    :param model: Loaded Sam model checkpoint
    :type model: _type_
    :param pred_iou: Exclude masks with a predicted score from the model is lower than this threshold.
    :type pred_iou: float
    :param stability_thresh: Exclude masks with a stability score lower than this threshold
    :type stability_thresh: float
    :param save_exp: Whether to save experiment result to a file.
    :type save_exp: bool
    :param save_name: Name of save file.
    :type save_name: str | Path
    :return: _description_
    :rtype: _type_
    """
    grid_masks_collect = []
    for scale, count in zip(scales, pcounts):
        sam_grid = SamAutomaticMaskGenerator(
            model=model,
            pred_iou_thresh=pred_iou,
            stability_score_thresh=stability_thresh,
            points_per_side=scale,
        )

        grid_masks = sam_grid.generate(np.array(cim))
        grid_masks_collect.append(grid_masks)

        if save_exp:
            save_prompt_experiment(
                name=save_name + str(count),
                target_path="../data/outputs",
                mask_lists=[grid_masks],
                prompt_counts=[count],
            )

    return grid_masks_collect
