"""
Using the 'get_frame' in moviepy returns a numpy array of 3 or 1 
dimension depending on the type of clip. If the clip is a main 
clip, a 3d array with values between [0, 255] is returned (one
[255, 255, 255] array would be a white pixel). If the clip is a
mask clip, a 1d array with values between [0, 1] is returned (the
1 completely transparent, the 0 is not).

Thats why you need to normalize or denormalize those values to
work with them because they are different and turning frames into
an image would need you to have the same range [0, 1] or [0, 255].

Check the Pillow, ImageIO and other libraries to see what kind of
numpy arrays are needed to write (or read) images.
"""
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.image.converter import ImageConverter
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from yta_general_utils.image.parser import ImageParser
from imageio import imsave

import numpy as np


class FrameExtractionType(Enum):
    TIME = 'time'
    FRAME_NUMBER = 'frame_number'

class VideoFrameExtractor:
    """
    Class to simplify the process of extracting video frames by time
    or frame number.
    """
    # TODO: Implement the 'output_filename' optional parameter to store
    # the frames if parameter is provided.
    @classmethod
    def _get_frame_time(cls, video, frame_number_or_time, extraction_type: FrameExtractionType):
        """
        Returns the time to obtain the frame of the provided 'video'
        according to the provided 'frame_number_or_time' parameter and
        the desired 'extraction_type'.

        This method is useful to be used first to validate that the
        frame times or numbers are valid and avoid getting all the 
        frames and loading them in memory if it is going to fail.
        """
        video = VideoParser.to_moviepy(video)
        extraction_type = FrameExtractionType.to_enum(extraction_type)
        
        if not NumberValidator.is_positive_number(frame_number_or_time):
            raise Exception('The provided "frame_number_or_time" is not a valid number.')
        
        if extraction_type == FrameExtractionType.FRAME_NUMBER:
            max_frame_number = video.fps * video.duration
            if frame_number_or_time > max_frame_number:
                raise Exception(f'The provided "frame_number" parameter {str(frame_number_or_time)}" is not valid. The maximum is {str(max_frame_number)}.')
            
            frame_number_or_time = frame_number_or_time * 1.0 / video.fps
        elif extraction_type == FrameExtractionType.TIME:
            if frame_number_or_time > video.duration:
                raise Exception(f'The provided "time" parameter {str(frame_number_or_time)} is not valid. The maximum is {str(video.duration)}.')
            
        return frame_number_or_time

    # TODO: I think I won't use this because I need to validate them first
    @classmethod
    def _get_frame(cls, video, frame_number_or_time, extraction_type: FrameExtractionType, output_filename: str = None):
        """
        Returns the frame of the provided 'video' according to the provided
        'frame_number_or_time' parameter and the desired 'extraction_type'.
        """
        video = VideoParser.to_moviepy(video)

        frame = video.get_frame(t = cls._get_frame_time(video, frame_number_or_time, extraction_type))

        if output_filename:
            cls._save_frame(frame, output_filename)

        return frame
    
    @classmethod
    def _get_frames(cls, video, frame_numbers_or_times, extraction_type: FrameExtractionType):
        """
        This method validates if all the provided 'frame_numbers_or_times'
        array parameter items are valid or not and them get all the frames
        and returns them as an array. This is optimum as it doesn't load
        frames until it's been verified the condition that all are valid.
        """
        video = VideoParser.to_moviepy(video)

        # Validate and get all times to obtain the frames later
        times = [cls._get_frame_time(video, frame_number_or_time, extraction_type) for frame_number_or_time in frame_numbers_or_times]

        return [video.get_frame(t = time) for time in times]
    
    @classmethod
    def get_frames_by_time(cls, video, times: list[float]):
        """
        Returns the frames (as numpy arrays) from the provided 'video'
        that corresponds to the provided 'times' time momnets of the
        video.

        This method will raise an Exception if the limits are not valid
        for the given 'video'.
        """
        return cls._get_frames(video, times, FrameExtractionType.TIME)

    @classmethod
    def _save_frame(cls, frame, output_filename: str):
        if not output_filename:
            return None
        
        # TODO: Validate 'output_filename'
        
        # TODO: This is how 'video.save_frame' works
        # https://github.com/Zulko/moviepy/blob/master/moviepy/video/VideoClip.py#L166
        # from imageio import imsave
        # im = self.get_frame(t)
        # if with_mask and self.mask is not None:
        #     mask = 255 * self.mask.get_frame(t)
        #     im = np.dstack([im, mask]).astype("uint8")
        # else:
        #     im = im.astype("uint8")

        imsave(output_filename, frame.astype("uint8"))

        return True

    @classmethod
    def get_frame_by_time(cls, video, time: float, output_filename: str = None):
        """
        Returns the frame (as numpy arrays) from the provided 'video'
        that corresponds to the provided 'time' moment.

        This method will raise an Exception if the limits are not valid
        for the given 'video'.
        """
        frame = cls.get_frames_by_time(video, [time])[0]

        if output_filename:
            cls._save_frame(frame, output_filename)

        return frame
    
    @classmethod
    def get_frames_by_time_from_start_to_end(cls, video, start_time: float, end_time: float):
        """
        Returns the frames (as numpy arrays) from the provided 'video'
        that corresponds to the lapse of time between the provided
        'start_time' and 'end_time'.

        This method will raise an Exception if the limits are not valid
        for the given 'video'.
        """
        video = VideoParser.to_moviepy(video)

        # Validate start and end parameters
        if not NumberValidator.is_positive_number(start_time) or start_time < 0 or start_time > video.duration:
            raise Exception(f'The provided "start_time" parameter "{str(start_time)}" is not valid. It must be a positive number between 0 and the video duration ({str(video.duration)}).')
        if not NumberValidator.is_positive_number(end_time) or end_time < 0 or end_time < start_time or end_time > video.duration:
            raise Exception(f'The provided "end_time" parameter "{str(end_time)}" is not valid. It must be a positive number between 0 and the video duration ({str(video.duration)}), and greater than the provided "start_time" parameter.')
        
        total_frames = int(video.duration * video.fps)
        time_moments = []
        for frame in range(total_frames):
            frame_time_moment = frame / video.fps  # tiempo en segundos para el frame actual
            if start_time <= frame_time_moment <= end_time:
                time_moments.append(frame_time_moment)

        return cls.get_frames_by_time(video, time_moments)

    @classmethod
    def get_frame_by_frame_number(cls, video, frame_number: int, output_filename: str = None):
        """
        Returns the frame (as numpy array) for the provided 'video' that
        corresponds to the provided 'frame_number'.

        This method will raise an Exception if the provided 'frame_number'
        is not a valid frame number for the given 'video'.
        """
        frame = cls._get_frame(video, frame_number, FrameExtractionType.FRAME_NUMBER)

        if output_filename:
            cls._save_frame(frame, output_filename)

        return frame
    
    @classmethod
    def get_frames_by_frame_number(cls, video, frame_numbers: list[int]):
        """
        Returns the frames (as numpy arrays) from the provided 'video'
        that corresponds to the provided 'frame_numbers'.

        This method will raise an Exception if the limits are not valid
        for the given 'video'.
        """
        return cls._get_frames(video, frame_numbers, FrameExtractionType.FRAME_NUMBER)
    
    @classmethod
    def get_frames_by_frame_number_from_start_to_end(cls, video, start_frame: float, end_frame: float):
        """
        Returns the frames (as numpy arrays) from the provided 'video' 
        from the 'start_frame' to the 'end_frame'.

        This method will raise an Exception if the limits are not valid
        for the given 'video'.
        """
        video = VideoParser.to_moviepy(video)

        max_frame_number = int(video.fps * video.duration)
        # Validate start and end parameters
        if not NumberValidator.is_positive_number(start_frame) or start_frame < 0 or start_frame > max_frame_number:
            raise Exception(f'The provided "start_frame" parameter "{str(start_frame)}" is not valid. It must be a positive number between 0 and the maximum frame ({str(max_frame_number)}).')
        if not NumberValidator.is_positive_number(end_frame) or end_frame < 0 or end_frame < start_frame or end_frame > max_frame_number:
            raise Exception(f'The provided "end_frame" parameter "{str(end_frame)}" is not valid. It must be a positive number between 0 and the maximum frame ({str(max_frame_number)}), and greater than the provided "start_time" parameter.')
        
        frames = [frame for frame in range(start_frame, end_frame + 1)]
        time_moments = [cls._get_frame_time(video, frame, FrameExtractionType.FRAME_NUMBER) for frame in frames]

        return cls.get_frames_by_time(video, time_moments)
    
    @classmethod
    def get_all_frames(cls, video):
        """
        Returns all the frames from the provided 'video'.
        """
        video = VideoParser.to_moviepy(video)

        # TODO: This was previously written in files like this:
        # if output_folder:
        #     video.write_images_sequence(output_folder + 'frame%05d.png')

        last_frame = (int) (video.duration * video.fps)

        return cls.get_frames_by_frame_number_from_start_to_end(video, 0, last_frame)
    
    @staticmethod
    def get_first_frame(video):
        """
        Obtain the first frame of the provided 'video' as a ndim=3
        numpy array containing the clip part (no mask) as not
        normalized values (between 0 and 255).
        """
        video = VideoParser.to_moviepy(video)

        # TODO: Some of the methods are failing (the ones with time
        # I think) so, when fixed, refactor this to make it light
        # weighting
        return VideoFrameExtractor.get_all_frames(video)[0]
    
    @staticmethod
    def get_last_frame(video):
        """
        Obtain the last frame of the provided 'video' as a ndim=3
        numpy array containing the clip part (no mask) as not
        normalized values (between 0 and 255).
        """
        video = VideoParser.to_moviepy(video)

        # TODO: Some of the methods are failing (the ones with time
        # I think) so, when fixed, refactor this to make it light
        # weighting
        all_frames = VideoFrameExtractor.get_all_frames(video)

        return all_frames[len(all_frames) - 1]
    
    # TODO: Would be perfect to have some methods to turn frames into
    # RGBA denormalized (0, 255) or normalized (0, 1) easier because
    # it is needed to work with images and other libraries. Those 
    # methods would iterate over the values and notice if they are in
    # an specific range so they need to be change or even if they are
    # invalid values (not even in [0, 255] range because they are not
    # rgb or rgba colors but math calculations).
    # This is actually being done by the VideoMaskHandler
    @classmethod
    def get_frame_as_rgba_by_time(cls, video, time: int, do_normalize: bool = False, output_filename: str = None):
        """
        Gets the frame of the requested 'time' of the provided
        'video' as a normalized RGBA numpy array that is built
        by joining the rgb frame (from main clip) and the alpha
        (from .mask clip), useful to detect transparent regions.
        """
        video = VideoParser.to_moviepy(video, do_include_mask = True)

        # We first normalize the clips
        main_frame = cls.get_frame_by_time(video, time) / 255  # RGB numpy array normalized 3d <= r,g,b
        mask_frame = cls.get_frame_by_time(video.mask, time)[:, :, np.newaxis]  # Alpha numpy array normalized 1d <= alpha
        # Combine RGB of frame and A from mask to RGBA numpy array (it is normalized)
        frame_rgba = np.concatenate((main_frame, mask_frame), axis = 2) # 4d <= r,g,b,alpha

        if output_filename:
            # TODO: Check extension
            ImageConverter.numpy_image_to_pil(frame_rgba).save(output_filename)
            # TODO: Write numpy as file image
            # Video mask is written as 0 or 1 (1 is transparent)
            # but main frame is written as 0 to 255, and the
            # 'numpy_image_to_pil' is expecting from 0 to 1
            # (normalized) instead of from 0 to 255 so it won't
            # work

        if not do_normalize:
            frame_rgba *= 255

        return frame_rgba
    
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

class VideoFrameHandler:
    """
    Class to encapsulate functionality related to moviepy
    video frame handling.
    """
    # TODO: This method should be in Image utils
    @staticmethod
    def is_pure_black_and_white_image(image):
        """
        Check if the provided 'image' only contains pure 
        black ([0, 0, 0]) and white ([255, 255, 255]) colors.
        """
        image = ImageParser.to_numpy(image)

        if np.any(~np.all((image == WHITE) | (image == BLACK), axis = -1)):
            return False
        
        return True
    
    @staticmethod
    def pure_black_and_white_image_to_moviepy_mask_numpy_array(image):
        """
        Turn the received 'image' (that must be a pure black
        and white image) to a numpy array that can be used as
        a moviepy mask (by using ImageClip).

        This is useful for static processed images that we 
        want to use as masks, such as frames to decorate our
        videos.
        """
        image = ImageParser.to_numpy(image)

        if not VideoFrameHandler.is_pure_black_and_white_image(image):
            raise Exception(f'The provided "image" parameter "{str(image)}" is not a black and white image.')

        # Image to a numpy parseable as moviepy mask
        mask = np.zeros(image.shape[:2], dtype = int) # 3col to 1col
        mask[np.all(image == WHITE, axis = -1)] = 1 # white to 1 value

        return mask
    
    def frame_to_pure_black_and_white_image(frame):
        """
        Process the provided moviepy clip mask frame (that
        must have values between 0.0 and 1.0) or normal clip
        frame (that must have values between 0 and 255) and
        convert it into a pure black and white image (an
        image that contains those 2 colors only).

        This method returns a not normalized numpy array of only
        2 colors (pure white [255, 255, 255] and pure black
        [0, 0, 0]), perfect to turn into a mask for moviepy clips.

        This is useful when handling an alpha transition video 
        that can include (or not) an alpha layer but it is also
        clearly black and white so you transform it into a mask
        to be applied on a video clip.
        """
        frame = ImageParser.to_numpy(frame)

        if not VideoFrameHandler.frame_is_mask_clip_frame(frame) and not VideoFrameHandler.frame_is_normal_clip_frame(frame):
            raise Exception('The provided "frame" parameter is not a moviepy mask clip frame nor a normal clip frame.')
        
        if VideoFrameHandler.frame_is_normal_clip_frame(frame):
            # TODO: Process it with some threshold to turn it
            # into pure black and white image (only those 2
            # colors) to be able to transform them into a mask.
            threshold = 220
            white_pixels = np.all(frame >= threshold, axis = -1)

            # Image to completely and pure black
            new_frame = np.array(frame)
            
            # White pixels to pure white
            new_frame[white_pixels] = [255, 255, 255]
            new_frame[~white_pixels] = [0, 0, 0]
        elif VideoFrameHandler.frame_is_mask_clip_frame(frame):
            transparent_pixels = frame == 1

            new_frame = np.array(frame)
            
            # Transparent pixels to pure white
            new_frame[transparent_pixels] = [255, 255, 255]
            new_frame[~transparent_pixels] = [0, 0, 0]

        return new_frame
    
    @staticmethod
    def frame_is_normal_clip_frame(frame: np.ndarray):
        """
        Checks if the provided 'frame' numpy array is recognized as
        a frame of a normal moviepy clip with values between 0 and
        255.

        This numpy array should represent a frame of a clip.
        
        A non-modified clip is '.ndim = 3' and '.dtype = np.uint8'.
        """
        return NumpyFrameHelper.is_rgb_not_normalized(frame)
        
    @staticmethod
    def frame_is_mask_clip_frame(frame: np.ndarray):
        """
        Checks if the provided 'mask_clip' numpy array is recognized
        as an original moviepy mask clip with values between 0 and 1.
        This numpy array should represent a frame of a mask clip.
        
        A non-modified mask clip is '.ndim = 2' and '.dtype = np.float64'.
        """
        return NumpyFrameHelper.is_alpha_normalized(frame)
        
    @staticmethod
    def invert_frame(frame: np.ndarray):
        """
        Invert the values of the provided 'frame', that can be
        a moviepy normal clip frame (with values between 0 and
        255) or a mask clip frame (with values between 0 and 1).

        This method invert the values by applying the max value
        (255 for normal frame, 1 for mask frame) minus each value
        in the numpy array.

        This method returns the numpy array inverted.
        """
        if not VideoFrameHandler.frame_is_normal_clip_frame(frame) and not VideoFrameHandler.frame_is_mask_clip_frame(frame):
            raise Exception('The provided "frame" is not actually a moviepy normal clip frame nor a mask clip frame.')
        
        if VideoFrameHandler.frame_is_normal_clip_frame(frame):
            frame = 255 - frame
        elif VideoFrameHandler.frame_is_mask_clip_frame(frame):
            frame = 1 - frame

        return frame
    
    @staticmethod
    def frame_to_mask_frame(frame: np.ndarray):
        """
        Turn the provided 'frame', that must be represented by
        RGB pixel values ([0-255, 0-255, 0-255]), to a mask
        frame represented by a single value between 0 and 1
        ([0.0-1.0]).
        """
        frame = ImageParser.to_numpy(frame)

        if not VideoFrameHandler.frame_is_normal_clip_frame(frame):
            raise Exception('The provided "frame" is not actually a moviepy normal clip frame.')
        
        frame = np.mean(frame, axis = -1) / 255.0

        return frame
    
# TODO: Maybe move this to another place
class NumpyFrameHelper:
    """
    Class to encapsulate functionality related to numpy
    frames.
    """
    @staticmethod
    def is_rgb_not_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.uint8 and all the values (3)
        are between 0 and 255.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 3 and frame.dtype == np.uint8 and frame.shape[2] == 3 and np.all((frame >= 0) & (frame <= 255))
    
    @staticmethod
    def is_rgb_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.float64|np.float32 and all 
        the values (3) are between 0.0 and 1.0.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 3 and frame.dtype in (np.float64, np.float32) and frame.shape[2] == 3 and np.all((frame >= 0.0) & (frame <= 1.0))
    
    @staticmethod
    def is_rgba_not_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.uint8 and all the values (4)
        are between 0 and 255.
        """
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.uint8 and all the values (3)
        are between 0 and 255.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 3 and frame.dtype == np.uint8 and frame.shape[2] == 4 and np.all((frame >= 0) & (frame <= 255))
    
    @staticmethod
    def is_rgba_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 3, dtype = np.float64|np.float32 and all 
        the values (4) are between 0.0 and 1.0.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 3 and frame.dtype in (np.float64, np.float32) and frame.shape[2] == 4 and np.all((frame >= 0.0) & (frame <= 1.0))
    
    @staticmethod
    def is_alpha_not_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 2, dtype = np.uint8 and all
        the values are between 0 and 255.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 2 and frame.dtype == np.uint8 and np.all((frame >= 0) & (frame <= 255))

    @staticmethod
    def is_alpha_normalized(frame: np.ndarray):
        """
        Check if the provided 'frame' is a numpy array of
        ndim = 2, dtype = np.float64|np.float32 and all
        the values are between 0.0 and 1.0.
        """
        frame = ImageParser.to_numpy(frame)

        if not PythonValidator.is_numpy_array(frame):
            raise Exception('The provided "frame" parameter is not a numpy array.')
        
        return frame.ndim == 2 and frame.dtype in (np.float64, np.float32) and np.all((frame >= 0.0) & (frame <= 1.0))

