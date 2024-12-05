from yta_general_utils.image.parser import ImageParser
from yta_general_utils.programming.output import handle_output_filename
from yta_general_utils.file.enums import ImageFileExtension
from PIL import ImageDraw, Image
from typing import Union

import numpy as np


class ImageMask:
    """
    Class to encapsulate and simplify the functionality
    related to image masking.
    """
    @staticmethod
    def to_moviepy_mask_numpy_array(mask_image):
        """
        Convert the provided 'mask_image' to a moviepy mask
        numpy array. This array could be used to generate an
        ImageClip in order to use it as a moviepy clip mask.
        """
        # Image can be GoogleDrive url, str filename, PIL, numpy
        # TODO: Handle if Google Drive url (?)
        mask_image = ImageParser.to_numpy(mask_image)

        WHITE = [255, 255, 255]
        BLACK = [0, 0, 0]
        # Check pure black and white image. The '~' inverts the condition
        if np.any(~np.all((mask_image == WHITE) | (mask_image == BLACK), axis = -1)):
            raise Exception(f'The provided "image" parameter "{str(mask_image)}" is not a black and white image.')

        # Image to a numpy parseable as moviepy mask
        mask = np.zeros(mask_image.shape[:2], dtype = int) # 3col to 1col
        mask[np.all(mask_image == WHITE, axis = -1)] = 1 # white to 1 value

        return mask
    
    # @staticmethod
    # def to_moviepy_mask_imageclip(mask_image):
    #     """
    #     Convert the provided 'mask_image' to a moviepy mask
    #     numpy array and puts it in an ImageClip as a mask,
    #     returning a ImageClip object that can be used as any
    #     clip mask by setting it with '.set_mask()'.
    #     """
    #     # TODO: This maybe should not exist as it is importing
    #     # moviepy library so we could have it less dependant
    #     return ImageClip(ImageMask.to_moviepy_mask_numpy_array(mask_image), ismask = True)
    
    @staticmethod
    def get_rounded_corners(image, output_filename: Union[str, None]):
        """
        Generate a mask of the provided 'image' with the corners
        rounded and return it as a Pillow Image.

        Thank you: https://github.com/Zulko/moviepy/issues/2120#issue-2141195159
        """
        image = ImageParser.to_pillow(image)

        # Create a whole black image of the same size
        mask = Image.new('L', image.size, 'black')
        mask_drawing = ImageDraw.Draw(mask)

        # Generate the rounded corners mask
        w, h = image.size
        radius = 20
        # Rectangles to cover
        mask_drawing.rectangle([radius, 0, w - radius, h], fill = 'white')
        mask_drawing.rectangle([0, radius, w, h - radius], fill = 'white')
        # Circles at the corners: TL, TR, BL, BR
        mask_drawing.ellipse([0, 0, 2 * radius, 2 * radius], fill = 'white')
        mask_drawing.ellipse([w - 2 * radius, 0, w, 2 * radius], fill = 'white')
        mask_drawing.ellipse([0, h - 2 * radius, 2 * radius, h], fill = 'white')
        mask_drawing.ellipse([w - 2 * radius, h - 2 * radius, w, h], fill = 'white')

        if output_filename:
            output_filename = handle_output_filename(output_filename, ImageFileExtension.PNG)
            mask.save(output_filename)

        # TODO: Is this 'image' actually edited (?)
        return mask

    # TODO: Add more effects 
    
    