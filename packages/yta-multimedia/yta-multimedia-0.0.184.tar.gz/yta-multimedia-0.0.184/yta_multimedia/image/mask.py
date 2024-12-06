from yta_general_utils.image.parser import ImageParser
from yta_general_utils.programming.output import handle_output_filename
from yta_general_utils.file.enums import ImageFileExtension
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.parameter_validator import PythonValidator
from PIL import ImageDraw, Image
from typing import Union

import numpy as np
import cv2


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

        The provided 'mask_image' must be an image in pure
        black and white colors, where black will be the 
        transparent part.

        This method returns a numpy array that can be set as
        an ImageClip(mask, ismask = True) directly, as it is
        a ndim = 1 numpy array with normalized values between
        0 and 1.
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
    
    @staticmethod
    def apply_mask(image, mask_generator_method: 'function', output_filename: Union[str, None] = None):
        """
        Generate the provided 'mask_generator_method' (that
        must be one of the static methods of the MaskGenerator
        class) and apply it in the provided 'image' (that must
        be a valid image).

        This method return the result image as a ndim = 4 numpy
        array of not normalized values between 0 and 255, even
        the alpha channel.
        """
        # TODO: Is this the best way to handle a valid masking
        # generation method (?)
        # TODO: Maybe just check if the provided method is
        # contained in the MaskGenerator class (?)
        if not PythonValidator.is_class_staticmethod(MaskGenerator, mask_generator_method):
            raise Exception('The provided "mask_generator_method" parameter is not a valid MaskGenerator static method.')

        image = ImageParser.to_numpy(image, mode = 'RGB')

        # Obtain mask as ndim = 1 where black is transparent
        mask = ImageParser.to_numpy(mask_generator_method(image))[:, :, 1]
        
        # Add the mask to the Pillow Image
        image = np.dstack((image, mask))

        if output_filename:
            # TODO: Apply 'output' handler
            cv2.imwrite(output_filename, image)

        return image

        # TODO: How to write a numpy image
        #cv2.imwrite('atripa_trans.png', image_with_mask)
    
    

class MaskGenerator:
    """
    Class to encapsulate the different methods we have to
    dynamically generate image masks.
    """
    @staticmethod
    def rounded_corners(image, output_filename: Union[str, None] = None):
        """
        Generate a mask of the provided 'image' with the corners
        rounded and return it as a not normalized RGB Pillow Image 
        with all values between 0 (white) and 255 (black). This 
        means that the result, if converted to array, will be
        [0, 0, 0] for each white pixel and [255, 255, 255] for 
        black ones.

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

        return mask

    def ticket(image, output_filename: Union[str, None] = None):
        image = ImageParser.to_pillow(image)

        # Create a whole black image of the same size
        mask = Image.new('L', image.size, 'white')
        mask_drawing = ImageDraw.Draw(mask)

        # Generate the mask
        w, h = image.size
        triangle_size = 15

        for i in range(0, w, triangle_size):
            mask_drawing.polygon([(i, h), (i + triangle_size, h), (i + triangle_size // 2, h - triangle_size)], fill = 'black')
            mask_drawing.polygon([(i, 0), (i + triangle_size, 0), (i + triangle_size // 2, triangle_size)], fill = 'black')

        if output_filename:
            output_filename = handle_output_filename(output_filename, ImageFileExtension.PNG)
            mask.save(output_filename)

        return mask

    # TODO: Add more effects 
