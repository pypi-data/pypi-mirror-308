import numpy as np
import numpy.typing as npt

COLOR_CHANNELS = {'R': 0, 'G': 1, 'B': 2}


def convert_dtype(images: npt.ArrayLike) -> npt.ArrayLike:
    if images.dtype != np.uint8:
        # 1.1 in case of potential interpolation noise (e.g. when zooming)
        if np.min(images) >= 0 and np.max(images) <= 1.1:
            new_images = images * (255 / np.max(images))
        return new_images.astype(np.uint8)
    return images


def _get_dimension_missmatch(images: npt.ArrayLike) -> tuple:
    dimensions = images.shape
    # shape must be dividable by 32
    height_diff = 32 - dimensions[0] % 32 if dimensions[0] % 32 != 0 else 0
    width_diff = 32 - dimensions[1] % 32 if dimensions[1] % 32 != 0 else 0
    return height_diff, width_diff


def _pad_and_greyscale(images: npt.ArrayLike, channel: str, height_diff: int, width_diff: int) -> npt.ArrayLike:
    num_images, height, width, _ = images.shape
    new_images = np.zeros((num_images, height + height_diff, width + width_diff, 3), dtype=np.float16)
    for i, img in enumerate(images):
        new_images[i, height_diff:, width_diff:, 0] = img[:, :, COLOR_CHANNELS[channel.upper()]]
        new_images[i, height_diff:, width_diff:, 1] = img[:, :, COLOR_CHANNELS[channel.upper()]]
        new_images[i, height_diff:, width_diff:, 2] = img[:, :, COLOR_CHANNELS[channel.upper()]]
    return new_images


def preprocess(images: npt.ArrayLike, channel: str = 'R') -> tuple:
    height_diff, width_diff = _get_dimension_missmatch(images[0])
    return _pad_and_greyscale(images, channel, height_diff, width_diff), height_diff, width_diff


def postprocess(images: npt.ArrayLike, height_diff: int, width_diff: int) -> npt.ArrayLike:
    return np.array([img[height_diff:, width_diff:] for img in images])
