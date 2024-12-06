"""
Utility code to persist/serialize segmentation masks.

:author: Kenneth Ball
:email: kenneth<dot>ball<at>geomdata<dot>com
:created: 2024 03 08
:copyright: (c) 2024, GDA
:license: All Rights Reserved, see LICENSE for more details
"""

from pathlib import Path
from typing import List, Optional

import numpy as np

from .ridge_prompts import RidgePrompts


def save_sam_automasks(file: str | Path, masks: List[dict] | List[list], **kwargs):
    """Save the output of SamAutomaskGenerator.

    :param file: path to save serialization
    :type file: str | Path
    :param masks: A list of masks, output by SamAutomaskGenerator.generate()
    :type masks: List[dict] | List[list]
    :return: None
    :rtype: None
    """
    with open(file, "wb") as f:
        np.savez_compressed(f, masks=masks, **kwargs)

    return None


def load_sam_automasks(file: str | Path):
    """Load SAM automatic masks as saved by `save_sam_automasks`.

    :param file: _description_
    :type file: str | Path
    :return: _description_
    :rtype: _type_
    """
    with open(file, "rb") as f:
        masks = np.load(f, allow_pickle=True)["masks"]

    return masks


def save_prompt_experiment(
    name: str,
    target_path: str | Path,
    mask_lists: List[list],
    prompt_counts: List[int],
    prompter: Optional[RidgePrompts | None] = None,
) -> None:
    """Save a list of lists of masks (e.g. multiple calls to `SamAutomaskGenerator.generate()`) with metadata.

    :param name: filename (without extension). Probably the image's name.
    :type name: str
    :param target_path: path to save to. Must exist.
    :type target_path: str | Path
    :param mask_lists: A list of lists of mask specs: outputs from separate calls to `SamAutomaskGenerator.generate()`
    :type mask_lists: List[list]
    :param prompt_counts: List of how many point prompts were used for auto mask generation,
        corresponding to entries in `mask_lists`.
    :type prompt_counts: List[int]
    :param prompter: The RidgePrompts object used to derive promps for ridge prompting, defaults to None
    :type prompter: Optional[RidgePrompts  |  None], optional
    :return: None
    :rtype: None
    """
    assert len(mask_lists) == len(prompt_counts)
    if prompter is not None:
        method = prompter.method
        scales = prompter.scales
    else:
        method = None
        scales = None
    metadata = [
        dict(method=method, scales=scales, prompt_count=pc) for pc in prompt_counts
    ]
    if isinstance(target_path, str):
        target_path = Path(target_path)
    filepath = target_path.joinpath(Path(name + ".npz"))
    save_sam_automasks(filepath, mask_lists, metadata=metadata)

    return None


def load_prompt_experiment(file: str | Path) -> tuple:
    """Load a file saved by `save_prompt_experiment`.

    :param file: Path to file.
    :type file: str | Path
    :return: The saved list of mask lists and associated metadata.
    :rtype: tuple
    """
    with open(file, "rb") as f:
        loaded = np.load(f, allow_pickle=True)
        mask_lists = loaded["masks"]
        metadata = loaded["metadata"]
    return mask_lists, metadata
