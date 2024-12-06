from segmentation_models import Unet
import numpy as np
import numpy.typing as npt
from skimage.measure import label
from . import utils
from . import MODEL_WEIGHTS


class SpotSegmenter:
    def __init__(self) -> None:
        self.model = Unet(backbone_name='resnet34', encoder_weights='imagenet')
        self.model.load_weights(MODEL_WEIGHTS)
        
    
    def segment_spots(self, rgb_image: npt.ArrayLike, channel: str = 'R') -> npt.ArrayLike:
        """
        Segment spots using Unet.

        Parameters:
            rgb_image: Single RGB image or array of RGB images as numpy array.
            channel: Which color channel should be used for segmentation ('R', 'G' or 'B').
        
        Returns:
            Single image or array of images containing segmentation masks.
        """
        if len(rgb_image.shape) < 3:
            raise ValueError(f"Given image has invalid dimensions! Given: {rgb_image.shape}, Expected: (height, width, 3)")
        elif len(rgb_image.shape) == 3:
            rgb_image = np.array([rgb_image])

        int_image = utils.convert_dtype(rgb_image)

        image, height_diff, width_diff = utils.preprocess(int_image, channel)
        
        probabilities = self.model.predict(image)
        segmentation_results = probabilities[:,:,:,0] > 0.875
        
        cropped_results = utils.postprocess(segmentation_results, height_diff, width_diff)

        if cropped_results.shape[0] == 1:
            return label(cropped_results[0])
        return np.array([label(image) for image in cropped_results])
