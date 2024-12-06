"""
A method to derive ridge point prompts from 2d images.

:author: Kenneth Ball
:email: kenneth<dot>ball<at>geomdata<dot>com
:created: 2024 02 22
:copyright: (c) 2024, GDA
:license: All Rights Reserved, see LICENSE for more details
"""

from typing import Iterable, Optional
from warnings import warn

import numpy as np
from PIL import Image
from scipy.ndimage import convolve
from skimage.color import rgb2gray
from skimage.measure import label, regionprops

from .ridge_detect import scale_space_ridge

distance_kernel = (
    np.array(
        [
            [np.sqrt(2), 1, np.sqrt(2)],
            [1, 0, 1],
            [np.sqrt(2), 1, np.sqrt(2)],
        ]
    )
    / 2
)


def salience(rp) -> float:
    """Determine salience of a ridge like curve.

    :param rp: a scikit-image regionprops object.
    :type rp: _type_
    :return: salience value
    :rtype: float
    """
    dk = distance_kernel
    # a fast approximation of a discretized path integral.
    ds = convolve(np.sum(rp.image, 2).astype(int), dk, mode="constant") * np.sum(
        rp.image, 2
    )
    return np.sum(ds * np.sqrt(np.sum(rp.intensity_image, 2)))


class RidgePrompts:

    """Generate SAM prompts from ridge-like features."""

    def __init__(
        self,
        image: Optional[np.ndarray | Image.Image] = None,
        scales: Optional[Iterable[float]] = None,
        method: str = "sq-pcd",
        pool: bool = True,
        threads: int = 3,
        chunksize: int = 1,
        windowsize: int = 400,
    ) -> None:
        """Initialize class to generate ridge prompts.

        If initialized with image and scales then ridge- and valley-like points will be detected
        and stored as an attribute.

        :param image: _description_, defaults to None
        :type image: Optional[np.ndarray  |  Image.Image], optional
        :param scales: _description_, defaults to None
        :type scales: Optional[Iterable[float]], optional
        :param method: _description_, defaults to "sq-pcd"
        :type method: str, optional
        :param pool: _description_, defaults to True
        :type pool: bool, optional
        :param threads: _description_, defaults to 3
        :type threads: int, optional
        :param chunksize: _description_, defaults to 1
        :type chunksize: int, optional
        :param windowsize: _description_, defaults to 400
        :type windowsize: int, optional
        """
        self.method = method
        self.pool = pool
        self.threads = threads
        self.chunksize = chunksize
        self.windowsize = windowsize
        self.image = image
        self.scales = scales

        self.set_image_and_scales(image, scales)

    def set_image_and_scales(
        self,
        image: Optional[np.ndarray | Image.Image] = None,
        scales: Optional[Iterable[float]] = None,
    ) -> None:
        """Load an image and set of scales and compute local ridge-like points at various scales.

        :param image: _description_, defaults to None
        :type image: Optional[np.ndarray  |  Image.Image], optional
        :param scales: _description_, defaults to None
        :type scales: Optional[Iterable[float]], optional
        :return: _description_
        :rtype: _type_
        """
        if image is None:
            self.image = None
            self.scales = None
            return
        if isinstance(image, Image.Image):
            # image = np.array(image.convert('L'))
            image = np.array(image)
        else:
            try:
                # try to stick to image types we and skimage know about.
                assert image.dtype == np.uint8 or (
                    image.dtype == float and (np.max(image) <= 1 and np.min(image) >= 0)
                )
            except AssertionError:
                warn(
                    "Image not set, expecting numpy array image to be either uint8 or float within [-1, 1]."
                )
                return None
        if len(image.shape) > 2:
            self.image = rgb2gray(image)
        if scales is None:
            max_scale = np.min(self.image.shape[:2]) / 2
            min_scale = 1
            scale_resolution = 1.0
            scales = (
                np.arange(
                    np.ceil(np.sqrt(min_scale)),
                    np.ceil(np.sqrt(max_scale)),
                    scale_resolution,
                )
                ** 2
            )
            self.scales = scales
        else:
            self.scales = scales

        self.ridge_tensor, self.valley_tensor = self._run_scale_space_ridge()

        return None

    def _run_scale_space_ridge(self):
        """Call scale space ridge detector and zero out bondary effects.

        :return: _description_
        :rtype: _type_
        """
        ridge_tensor, valley_tensor, _ = scale_space_ridge(
            gray=self.image,
            scales=self.scales,
            method=self.method,
            pool=self.pool,
            threads=self.threads,
            chunksize=self.chunksize,
            windowsize=self.windowsize,
        )

        ridge_tensor = ridge_tensor
        valley_tensor = valley_tensor

        # set any ridge detections at boundaries (boundary width relative to scale)
        # to zero to avoid boundary effects.
        for tensor in [ridge_tensor, valley_tensor]:
            for ss, scale in enumerate(self.scales):
                bound = max([int(np.ceil(self.scale_to_width(scale) * 1.25)), 1])
                for ii in range(2):
                    tensor[0:bound, :, ss] = 0
                    tensor[(tensor.shape[0] - bound) :, :, ss] = 0
                    tensor[:, 0:bound, ss] = 0
                    tensor[:, (tensor.shape[1] - bound) :, ss] = 0

        return ridge_tensor, valley_tensor

    def get_prompts(
        self,
        ridge_prompt_count: Optional[int] = 256,
        valley_prompt_count: Optional[int] = None,
        test_quantile_filter: Optional[float] = 0.25,
        min_component_size: int = 3,
        random_seed: Optional[int] = None,
    ) -> dict:
        """Parse scale-space ridge features into ridge-like feature point prompts for SAM.

        :param ridge_prompt_count: Desired number of ridge point prompts, defaults to 256
        :type ridge_prompt_count: Optional[int], optional
        :param valley_prompt_count: Desired number of valley point prompts, defaults to None
        :type valley_prompt_count: Optional[int], optional
        :param test_quantile_filter: A quantile filter to ignore smaller ridge test values, defaults to 0.80
        :type test_quantile_filter: Optional[float], optional
        :param min_component_size: A filter on the minimum size of connected ridge/valley curve components,
            defaults to None
        :type min_component_size: int
        :return: a dict holding prompts+labels to use for batching in SAM predict and also point prompts
            to be used in SAM SamAutomaticMaskGenerator.
        :rtype: dict
        """
        if test_quantile_filter is None:
            test_quantile_filter = 0.0
        use_ridge = False
        use_valley = False
        if ridge_prompt_count is not None and ridge_prompt_count > 0:
            use_ridge = True
        if valley_prompt_count is not None and valley_prompt_count > 0:
            use_valley = True

        if use_ridge:
            r_prompts = self._get_prompts(
                self.ridge_tensor,
                prompt_count=ridge_prompt_count,
                test_quantile_filter=test_quantile_filter,
                min_component_size=min_component_size,
                random_seed=random_seed,
            )
        if use_valley:
            v_prompts = self._get_prompts(
                self.valley_tensor,
                prompt_count=valley_prompt_count,
                test_quantile_filter=test_quantile_filter,
                min_component_size=min_component_size,
                random_seed=random_seed,
            )
        if use_ridge and use_valley:
            return dict(
                batch_point_prompts=r_prompts["batch_point_prompts"]
                + v_prompts["batch_point_prompts"],
                batch_point_labels=v_prompts["batch_point_labels"]
                + v_prompts["batch_point_labels"],
                automask_prompts=[
                    np.concatenate(
                        [
                            r_prompts["automask_prompts"],
                            v_prompts["automask_prompts"],
                        ],
                        axis=0,
                    )
                ],
            )
        elif use_ridge:
            r_prompts["automask_prompts"] = [r_prompts["automask_prompts"]]
            return r_prompts
        elif use_valley:
            v_prompts["automask_prompts"] = [v_prompts["automask_prompts"]]
            return v_prompts
        else:
            return dict(
                batch_point_prompts=[],
                batch_point_labels=[],
                automask_prompts=[np.array([])],
            )

    @staticmethod
    def _get_prompts(
        ridge_tensor: np.ndarray,
        prompt_count: Optional[int] = 256,
        connected_component_factor: float = 10,
        min_component_size: int = 3,
        test_quantile_filter: float = 0.25,
        random_seed: Optional[int] = None,
    ):
        """Parse scale-space ridge features into ridge-like feature point prompts for SAM.

        :param ridge_tensor: tensor of ridge (or valley) like features from `scale_space_ridge`.
        :type ridge_tensor: np.ndarray
        :param prompt_count: target number of point prompts to generate according to a salient
            ridge line sorting criterion. If provided and not None, connected_component_factor and
            min_component_size are ignored.
        :type prompt_count: Optional[int], optional
        :param connected_component_factor: reductive factor for point selection, defaults to 10.
            Only used if prompt_count is None.
        :type connected_component_factor: int, optional
        :param min_component_size: minimum size of ridge curves, defaults to 20.
            Only used if prompt_count is None
        :type min_component_size: int, optional
        :param test_quantile_filter: A quantile filter to ignore smaller ridge test values,
            defaults to 0.25
        :type test_quantile_filter: float
        :param random_seed: random seed for point prompt selector, defaults to None.
        :type random_seed: int
        :return: _description_
        :rtype: _type_
        """
        rng = np.random.default_rng(random_seed)
        if test_quantile_filter > 0.0:
            rtens = label(
                ridge_tensor
                > np.quantile(ridge_tensor[ridge_tensor > 0], test_quantile_filter)
            )
        else:
            rtens = label(ridge_tensor > 0.0)
        points = []
        batch_point_prompts = []
        batch_point_labels = []
        if prompt_count is not None:
            rps = regionprops(rtens, ridge_tensor)
            rps = [rp for rp in rps if rp.area >= min_component_size]
            sal_rp = np.array([salience(rp) for rp in rps])
            prompts_per_curve = np.ceil(sal_rp / np.sum(sal_rp) * prompt_count).astype(
                int
            )

            # in the unlikely event that the prompts desired for a curve section is greater than the
            # actual area, reduce the prompts to generate for that curve.
            areas = np.array([rp.area for rp in rps])
            excessive_prompts = np.argwhere(prompts_per_curve > areas).transpose()[0]
            for ii in excessive_prompts:
                prompts_per_curve[ii] = areas[ii]

            prompts_left = prompt_count
            for ii in np.argsort(sal_rp)[::-1]:
                rp = rps[ii]
                n_points = min([prompts_left, prompts_per_curve[ii]])
                coords = rp.coords[rng.choice(len(rp.coords), n_points, replace=False)]
                for point in coords:
                    points.append(point + 0.5)
                    prompt = [points[-1][1], points[-1][0]]
                    batch_point_prompts.append([prompt])
                    batch_point_labels.append([1])
                prompts_left -= n_points
                if prompts_left <= 0:
                    break
        else:
            ccf = connected_component_factor
            rps = regionprops(rtens, ridge_tensor)
            rps = [rp for rp in rps if rp.area >= min_component_size]
            for rp in rps:
                n_points = max([(len(rp.coords) // ccf), 1])
                coords = rp.coords[np.random.randint(0, len(rp.coords), n_points)]
                for point in coords:
                    points.append(point + 0.5)
                    prompt = [points[-1][1], points[-1][0]]
                    batch_point_prompts.append([prompt])
                    batch_point_labels.append([1])

        automask_prompts = np.array(batch_point_prompts)[:, 0, :]
        automask_prompts[:, 0] /= ridge_tensor.shape[1]
        automask_prompts[:, 1] /= ridge_tensor.shape[0]

        return dict(
            batch_point_prompts=batch_point_prompts,
            batch_point_labels=batch_point_labels,
            automask_prompts=automask_prompts,
        )

    @staticmethod
    def scale_to_width(value, factor=1, inverse=False):
        """Scale to width of array."""
        if inverse:
            return ((value * 1.025 / factor) / np.sqrt(2 * np.pi)) ** (2)
        return np.sqrt(np.array(value) * 2 * np.pi) / 1.025 * factor
