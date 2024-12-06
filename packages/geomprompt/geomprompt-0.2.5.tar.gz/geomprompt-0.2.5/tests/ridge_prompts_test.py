"""Tests for RidgePrompt."""

import pytest
from geomprompt.ridges.ridge_prompts import RidgePrompts
from skimage.data import brick


@pytest.fixture(scope="module", params=[None, [2.0, 4.0, 8.0]])
def prompter(request: list | None):
    """Fixture of RidgePrompts objects.

    :param request: scales argument for initialization of RidgePrompts
    :type request: list | None
    :yield: RidgePrompts initialized object
    :rtype: RidgePrompts
    """
    prompter = RidgePrompts(brick(), scales=request.param)
    yield prompter


class TestRidgePrompts:
    """Test recovery of salient prompt points from RidgePrompts."""

    @pytest.mark.parametrize("points", [8, 16, 32])
    def test_ridge_prompts(self, prompter: RidgePrompts, points: int):
        """Test multiscale ridge prompt selection.

        :param prompter: geomprompt RidgePrompts object initialized with an image.
        :type prompter: RidgePrompts
        :param points: Number of prompt points to find.
        :type points: int
        """
        ridge_prompts = prompter.get_prompts(ridge_prompt_count=points)
        assert len(ridge_prompts["automask_prompts"][0]) == points
        assert len(ridge_prompts["batch_point_prompts"]) == points

    @pytest.mark.parametrize("valley_points", [8, 16, 32])
    def test_concurrent_valley_prompts(
        self, prompter: RidgePrompts, valley_points: int
    ):
        """Test multiscale ridge and valley prompt sellection (concurrent).

        :param prompter: geomprompt RidgePrompts object initialized with an image.
        :type prompter: RidgePrompts
        :param valley_points: Number of valley points to find.
        :type valley_points: int
        """
        prompts = prompter.get_prompts(
            ridge_prompt_count=8, valley_prompt_count=valley_points
        )
        assert len(prompts["batch_point_prompts"]) == valley_points + 8

    @pytest.mark.parametrize("quantile_filter", [None, 0.0, 0.5])
    def test_quantile_filter(
        self, prompter: RidgePrompts, quantile_filter: float | None
    ):
        """Test prompt selection when filtering less ridge-like points at varying thresholds.

        :param prompter: geomprompt RidgePrompts object initialized with an image.
        :type prompter: RidgePrompts
        :param quantile_filter: Filter out less "ridgy" points for determining salient ridge features.
        :type quantile_filter: float | None
        """
        prompts = prompter.get_prompts(
            ridge_prompt_count=8, test_quantile_filter=quantile_filter
        )
        assert len(prompts["batch_point_prompts"]) == 8

    @pytest.mark.parametrize("min_component_size", [0, 1, 4])
    def test_min_component_size(self, prompter: RidgePrompts, min_component_size: int):
        """Test prompt selection with minimal connected component sizes for salient ridge curves.

        :param prompter: geomprompt RidgePrompts object initialized with an image.
        :type prompter: RidgePrompts
        :param min_component_size: Minimum size of connected salient ridge curves.
        :type min_component_size: int
        """
        prompts = prompter.get_prompts(
            ridge_prompt_count=8, min_component_size=min_component_size
        )
        assert len(prompts["batch_point_prompts"]) == 8
