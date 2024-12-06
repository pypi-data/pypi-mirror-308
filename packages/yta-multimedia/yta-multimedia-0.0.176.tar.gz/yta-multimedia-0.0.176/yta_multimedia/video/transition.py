from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.video_effect import MoviepySetPosition
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_corner import CoordinateCorner
from yta_general_utils.math.rate_functions import RateFunction
from yta_multimedia.video.frames import VideoFrameExtractor
from yta_general_utils.programming.parameter_validator import NumberValidator
from yta_general_utils.programming.error_message import ErrorMessage
from moviepy.editor import ImageClip, CompositeVideoClip, concatenate_videoclips


class Transition:
    """
    Class to simplify and encapsulate the functionality
    related to transition between videos
    """
    @staticmethod
    def slide(video1, video2, duration: float = 0.5):
        """
        Simple transition in which the last frame of the provided 'video1'
        is replaced by the first frame of the provided 'video2' by sliding
        from right to left.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)

        if not NumberValidator.is_positive_number(duration):
            raise Exception(ErrorMessage.parameter_is_not_positive_number('duration'))
        # TODO: Maybe put some limit (10s or similar) (?)

        # TODO: I was working before in setting the position
        # constants so I could use them to easily handle slides
        # from different sides of the screen

        # Transition from last frame of vide1 to first of video2
        transition_clip_1 = MoviepySetPosition(CoordinateCorner(0, 0), CoordinateCorner(-transition_clip_1.w, 0), TFunctionSetPosition.linear, RateFunction.linear).apply(ImageClip(VideoFrameExtractor.get_last_frame(video1), duration = duration).set_fps(60))
        # TODO: Maybe set 'transition_clip_1.pos' instead of (0, 0)
        transition_clip_2 = MoviepySetPosition(CoordinateCorner(transition_clip_1.w, 0), CoordinateCorner(0, 0), TFunctionSetPosition.linear, RateFunction.linear).apply(ImageClip(VideoFrameExtractor.get_first_frame(video2), duration = duration).set_fps(60))

        return CompositeVideoClip([
            transition_clip_1,
            transition_clip_2
        ])

    @staticmethod
    def apply(video1, video2, duration: float = 0.5, transition_method: type = 'Transition.slide'):
        """
        Build a transition by using the provided 'transition_method' 
        (that must be a transition method within the Transition class)
        and put it between the provided 'video1' and 'video2' that are
        played completely.

        So, the sequence is the next.
        1. The 'video1' is played completely.
        2. The transition is played completely.
        3. The 'video2' is played completely.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)

        # TODO: Validate 'transition_method' is one of the methods
        # we accept (and refactor it)

        return concatenate_videoclips([
            video1,
            transition_method(video1, video2, duration),
            video2
        ])

