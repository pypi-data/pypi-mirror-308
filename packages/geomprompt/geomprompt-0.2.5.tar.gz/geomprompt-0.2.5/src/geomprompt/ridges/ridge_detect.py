"""
A method to perform ridge detection on 2d images.

:author: Kenneth Ball
:email: kenneth<dot>ball<at>geomdata<dot>com
:created: 2020 08 14
:copyright: (c) 2020, GDA
:license: All Rights Reserved, see LICENSE for more details
"""

import itertools
from multiprocessing import Pool

import numpy as np

# from PIL import Image
from scipy.ndimage import gaussian_filter  # , fourier_uniform
from skimage.feature import hessian_matrix, hessian_matrix_eigvals

EPSILON = np.half(1e-7)


def scale_space_ridge(
    gray, scales, method="sq-pcd", pool=True, threads=3, chunksize=1, windowsize=400
):
    """
    Compute a multiscale ridge/valley representation of an image.

    Features are curves in image/scale space that are local height ridges/valleys
    and local max's of the ridge test value in scale space.

    :param gray: A gray-scaled image array.
    :param scales: A 1-d array of ordered scale values to test.
    :param method: (str) either 'pcd' or 'sq-pcd'
    :param pool: Should we use multiprocessing.Pool to parallelize computation?
    :param threads: (int) number of pool threads
    :param chunksize: (int) number of imap chunks
    :param windowsize: (int) height/width of windows in pixels to chunk up the image for parallel processing.
    :return: (tuple) Ridge and valley tensors indicating ridge/valley test vals in image/scale space and directionality.
    """
    if gray.dtype == np.uint8:
        gray = gray.astype(float) / 255
    test_tensor = np.zeros(gray.shape + (len(scales),))  # .astype(np.half)
    ridge_mark = np.zeros(gray.shape + (len(scales),)).astype(bool)
    valley_mark = np.zeros(gray.shape + (len(scales),)).astype(bool)
    zc1_tensor = np.zeros(gray.shape + (len(scales),)).astype(bool)
    zc2_tensor = np.zeros(gray.shape + (len(scales),)).astype(bool)
    ridge_r_comp = np.zeros(gray.shape + (len(scales),)).astype(np.half)
    ridge_c_comp = np.zeros(gray.shape + (len(scales),)).astype(np.half)
    if not pool:
        for ss, scale in enumerate(scales):
            output = scale_slice_ridge(gray=gray, scale=scale, method=method)
            test_tensor[:, :, ss] = output["test_tensor"]
            ridge_mark[:, :, ss] = output["ridge_mark"]
            valley_mark[:, :, ss] = output["valley_mark"]
            ridge_r_comp[:, :, ss] = output["ridge_r_comp"]
            ridge_c_comp[:, :, ss] = output["ridge_c_comp"]
            zc1_tensor[:, :, ss] = output["zc1"]
            zc2_tensor[:, :, ss] = output["zc2"]
    else:
        with Pool(threads) as p:
            ws = windowsize
            max_scale = np.max(scales)
            buffer = int(
                np.ceil(2 * np.sqrt(max_scale)) + np.ceil(np.log10(max_scale)) * 1.5
            )
            window_top_left_row_indices = np.arange(0, gray.shape[0], ws - 2 * buffer)
            window_top_left_col_indices = np.arange(0, gray.shape[1], ws - 2 * buffer)
            window_row_bounds = [
                [w, np.min([w + ws, gray.shape[0]])]
                for w in window_top_left_row_indices
            ]
            window_col_bounds = [
                [w, np.min([w + ws, gray.shape[1]])]
                for w in window_top_left_col_indices
            ]
            windows = [
                [*r, *c]
                for r, c in itertools.product(window_row_bounds, window_col_bounds)
            ]
            sub_windows = [
                [
                    (w[0] + buffer if w[0] != 0 else 0),
                    (w[1] - buffer if w[1] != gray.shape[0] else w[1]),
                    (w[2] + buffer if w[2] != 0 else 0),
                    (w[3] - buffer if w[3] != gray.shape[1] else w[3]),
                ]
                for w in windows
            ]
            sub_buffers = [
                [
                    (buffer if w[0] != 0 else 0),
                    (ws - buffer if w[1] != gray.shape[0] else ws),
                    (buffer if w[2] != 0 else 0),
                    (ws - buffer if w[3] != gray.shape[1] else ws),
                ]
                for w in windows
            ]
            for ii, output in enumerate(
                p.imap(
                    scale_slice_ridge_wrapper,
                    scale_slice_ridge_generator(gray, scales, method, windows),
                    chunksize=chunksize,
                )
            ):
                ss = ii // len(windows)
                ww = ii % len(windows)
                w = sub_windows[ww]
                b = sub_buffers[ww]
                test_tensor[w[0] : w[1], w[2] : w[3], ss] = output["test_tensor"][
                    b[0] : b[1], b[2] : b[3]
                ]
                ridge_mark[w[0] : w[1], w[2] : w[3], ss] = output["ridge_mark"][
                    b[0] : b[1], b[2] : b[3]
                ]
                valley_mark[w[0] : w[1], w[2] : w[3], ss] = output["valley_mark"][
                    b[0] : b[1], b[2] : b[3]
                ]
                ridge_r_comp[w[0] : w[1], w[2] : w[3], ss] = output["ridge_r_comp"][
                    b[0] : b[1], b[2] : b[3]
                ]
                ridge_c_comp[w[0] : w[1], w[2] : w[3], ss] = output["ridge_c_comp"][
                    b[0] : b[1], b[2] : b[3]
                ]
                zc1_tensor[w[0] : w[1], w[2] : w[3], ss] = output["zc1"][
                    b[0] : b[1], b[2] : b[3]
                ]
                zc2_tensor[w[0] : w[1], w[2] : w[3], ss] = output["zc2"][
                    b[0] : b[1], b[2] : b[3]
                ]
            p.close()
            p.join()

    # having recorded all the test values, we look for critical points (local maxima) of the test values across scale.
    # We record those critical points in the tcrit_boolean tensor.

    tcrit_tensor = np.zeros(gray.shape + (len(scales),)).astype(bool)
    tcrit_tensor[:, :, 1 : (len(scales) - 1)] = np.logical_and(
        test_tensor[:, :, 1 : (len(scales) - 1)]
        >= test_tensor[:, :, 0 : (len(scales) - 2)],
        test_tensor[:, :, 1 : (len(scales) - 1)]
        >= test_tensor[:, :, 2 : (len(scales))],
    )
    tcrit_tensor[:, :, 0] = test_tensor[:, :, 0] > test_tensor[:, :, 1]
    tcrit_tensor[:, :, len(scales) - 1] = (
        test_tensor[:, :, len(scales) - 1] > test_tensor[:, :, len(scales) - 2]
    )

    # True ridges are points with a critical test value and a zero crossing of the gradient that were marked as
    # ridge-like. We get these points as true values and multiply them by log2 of the test value.

    ridge_tensor = np.logical_and(tcrit_tensor, zc2_tensor)
    ridge_tensor = np.logical_and(ridge_tensor, ridge_mark)
    ridge_tensor = ridge_tensor * test_tensor

    # True valleys are points with a critical test value and a zero crossing of the gradient that were marked as
    # valley-like. We get these points as true values and multiply them by log2 of the test value.

    valley_tensor = np.logical_and(tcrit_tensor, zc1_tensor)
    valley_tensor = np.logical_and(valley_tensor, valley_mark)
    valley_tensor = valley_tensor * test_tensor

    # We return the ridge and valley tensors, as well as a list of the row and column components of the leading
    # Hessian eigenvector at each scale.

    return ridge_tensor, valley_tensor, [ridge_r_comp, ridge_c_comp]


def scale_slice_ridge_wrapper(x):
    """
    Wrap scale_slice_ridge for multiprocessing.

    :param x: list of arguments for multiprocessing.
    :return: a dictionary of arrays to be used in scale_space_ridge.
    """
    return scale_slice_ridge(gray=x[0], scale=x[1], method=x[2])


def scale_slice_ridge_generator(gray, scales, method, windows):
    """
    Act as generator for scale_slice_ridge arguments for multiprocessing.

    :param gray: The grayscale image for ridge detection.
    :param scales: Scales to be considered for multiscale ridge detection.
    :param method: Which ridge test critiera should be used? ('sq-pcd' or 'pcd').
    :param windows: Slice values for windowing into multiprocess tasks.
    :yield: Arguments for a signle scale_slice_ridge run on a window of the total gray image.
    """
    ii = 0
    while ii < len(scales) * len(windows):
        ww = ii % len(windows)
        ss = ii // len(windows)
        w = windows[ww]
        yield [gray[w[0] : w[1], w[2] : w[3]], scales[ss], method]
        ii += 1


def scale_slice_ridge(gray, scale, method):
    """
    Compute ridge/valley tests, zero crossings of the gradient, and ev orientations for an image at scale.

    :param gray: The grayscale image for ridge detection.
    :param scale: The scale at which to apply the ridge test.
    :param method: Which ridge test critiera should be used? ('sq-pcd' or 'pcd').
    :return: a dictionary of arrays to be used in scale_space_ridge.
    """
    # For every given scale, we get the local test values and mark whether or not each pixel is a local ridge
    # or valley point.
    gamma = 3 / 4
    sigma = np.sqrt(scale)
    # rr, rc, cc = [_ * 255 for _ in hessian_matrix(gray, sigma=sigma, order='rc')]
    rr, rc, cc = hessian_matrix(
        gray,
        sigma=sigma,
        order="rc",
        use_gaussian_derivatives=True,
    )
    aa, bb = hessian_matrix_eigvals((rr, rc, cc))
    output = dict()
    if method == "sq-pcd":
        test_value = np.sqrt(
            (scale) ** (gamma * 4) * ((rr + cc) ** 2 * ((rr - cc) ** 2 + 4 * rc**2))
        )
    elif method == "pcd":
        test_value = (scale) ** (gamma * 2) * ((rr - cc) ** 2 + 4 * rc**2)
    output.update(test_tensor=test_value)
    del test_value
    output.update(ridge_mark=np.logical_and(bb < 0, np.abs(aa) < np.abs(bb)))
    output.update(valley_mark=np.logical_and(aa > 0, np.abs(aa) > np.abs(bb)))

    # Next we compute the eigenvector associated with the smallest eigenvalue of the Hessian at each pixel and record
    # the row, col components. This eigenvector is in the direction of least principal curvature, and hence runs
    # transverse to the ridge orientation. (The other eigenvector may be obtained trivially as orthogonal to this one.)

    eigenvec = [np.zeros(rr.shape), np.zeros(rr.shape)]
    canonical_row = np.logical_and(rc == 0, cc <= rr)
    canonical_col = np.logical_and(rc == 0, cc > rr)
    regular_guys = np.logical_and(~canonical_col, ~canonical_row)
    eigenvec[0][canonical_row] = 1
    eigenvec[1][canonical_col] = 1
    eigenvec[1][regular_guys] = 1
    eigenvec[0][regular_guys] = (
        cc[regular_guys]
        - rr[regular_guys]
        - np.sqrt(
            (rr[regular_guys] - cc[regular_guys]) ** 2 + 4 * rc[regular_guys] ** 2
        )
    ) / rc[regular_guys]
    del aa, bb, rr, rc, cc, canonical_col, canonical_row, regular_guys
    mag = np.sqrt(eigenvec[0] ** 2 + eigenvec[1] ** 2)
    eigenvec[0][mag > 0] /= mag[mag > 0]
    eigenvec[1][mag > 0] /= mag[mag > 0]
    del mag

    output.update(ridge_r_comp=eigenvec[0].astype(np.half))
    output.update(ridge_c_comp=eigenvec[1].astype(np.half))

    # True ridge and valley paths sweep out curves in the multi-scale space. Also, the local gradient in the
    # direction of the most negative pc eigenvector should have a zero crossing at each curve point at the local scale.

    lr, lc = np.gradient(gaussian_filter(gray, sigma=sigma))
    output.update(
        zc2=principal_curvature_gradient_zero_crossings(lr, lc, eigenvec, gray.shape)
    )
    output.update(
        zc1=principal_curvature_gradient_zero_crossings(
            lr, lc, [eigenvec[1], -eigenvec[0]], gray.shape
        )
    )

    return output


def principal_curvature_gradient_zero_crossings(lr, lc, eigenvec, shape):
    """
    Identify zero crossings of an image gradient projected (locally) on a vector field.

    :param lr: row components of the image gradient
    :param lc: column components of the image gradient
    :param eigenvec: a list of [row, column] components of the vector field (typically an eigenvector of the Hessian).
    :param shape: a tuple (m, n) of the row, column dimensions of the underlying images. shape == lr.shape
    :return: zc, a boolean array of size `shape` where True indicates the presence of a zero crossing of the
        gradient in the local direction of eigenvec.
    """
    m, n = shape
    # the gradient in the local least eigenvector direction:
    lpc = eigenvec[0] * lr + eigenvec[1] * lc
    # array to record the zero crossings:
    zc = np.zeros(shape, dtype=bool)
    # the up directional offset of the gradient... that is, what is the gradient at the (i - 1, j) point in the (i, j)
    # principal curvature direction?
    lpc_dir = (
        lr[0 : (m - 2), :] * eigenvec[0][1 : (m - 1), :]
        + lc[0 : (m - 2), :] * eigenvec[1][1 : (m - 1), :]
    )
    zc[1 : (m - 1), :] |= np.logical_and(
        np.sign(lpc_dir) != np.sign(lpc[1 : (m - 1), :]),
        np.abs(lpc_dir) > np.abs(lpc[1 : (m - 1), :]),
    )
    # same but in the down direction.
    lpc_dir = (
        lr[2:m, :] * eigenvec[0][1 : (m - 1), :]
        + lc[2:m, :] * eigenvec[1][1 : (m - 1), :]
    )
    zc[1 : (m - 1), :] |= np.logical_and(
        np.sign(lpc_dir) != np.sign(lpc[1 : (m - 1), :]),
        np.abs(lpc_dir) > np.abs(lpc[1 : (m - 1), :]),
    )
    # same but in the left direction.
    lpc_dir = (
        lr[:, 0 : (n - 2)] * eigenvec[0][:, 1 : (n - 1)]
        + lc[:, 0 : (n - 2)] * eigenvec[1][:, 1 : (n - 1)]
    )
    zc[:, 1 : (n - 1)] |= np.logical_and(
        np.sign(lpc_dir) != np.sign(lpc[:, 1 : (n - 1)]),
        np.abs(lpc_dir) > np.abs(lpc[:, 1 : (n - 1)]),
    )
    # same but in the right direction.
    lpc_dir = (
        lr[:, 2:n] * eigenvec[0][:, 1 : (n - 1)]
        + lc[:, 2:n] * eigenvec[1][:, 1 : (n - 1)]
    )
    zc[:, 1 : (n - 1)] |= np.logical_and(
        np.sign(lpc_dir) != np.sign(lpc[:, 1 : (n - 1)]),
        np.abs(lpc_dir) > np.abs(lpc[:, 1 : (n - 1)]),
    )
    return zc


def gradient_zero_crossings(lr, lc, shape):
    """
    Find zero crossings of the gradient in the row and gradient directions.

    :param lr: Row components of the gradient
    :param lc: Column components of the gradient.
    :param shape: Shape of the arrays.
    :return:
    """
    m, n = shape
    # array to record the zero crossings:
    zcr = np.zeros(shape).astype(bool)
    zcr[1 : (m - 1), :] = np.logical_or(
        np.logical_and(
            np.sign(lr[0 : (m - 2), :]) != np.sign(lr[1 : (m - 1), :]),
            np.abs(lr[0 : (m - 2), :]) > np.abs(lr[1 : (m - 1), :]),
        ),
        np.logical_and(
            np.sign(lr[2:m, :]) != np.sign(lr[1 : (m - 1), :]),
            np.abs(lr[2:m, :]) > np.abs(lr[1 : (m - 1), :]),
        ),
    )
    zcc = np.zeros(shape).astype(bool)
    zcc[:, 1 : (n - 1)] = np.logical_or(
        np.logical_and(
            np.sign(lc[:, 0 : (n - 2)]) != np.sign(lc[:, 1 : (n - 1)]),
            np.abs(lc[:, 0 : (n - 2)]) > np.abs(lc[:, 1 : (n - 1)]),
        ),
        np.logical_and(
            np.sign(lc[:, 2:n]) != np.sign(lc[:, 1 : (n - 1)]),
            np.abs(lc[:, 2:n]) > np.abs(lc[:, 1 : (n - 1)]),
        ),
    )
    zc = np.logical_or(zcr, zcc)
    return zc
