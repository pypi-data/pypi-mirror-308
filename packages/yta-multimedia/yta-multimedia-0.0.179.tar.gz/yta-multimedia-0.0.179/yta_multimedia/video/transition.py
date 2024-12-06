from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.video_effect import MoviepySetPosition
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate_corner import CoordinateCorner
from yta_general_utils.math.rate_functions import RateFunction
from yta_multimedia.video.frames import VideoFrameExtractor
from yta_general_utils.programming.parameter_validator import NumberValidator
from yta_general_utils.programming.error_message import ErrorMessage
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from moviepy.editor import ImageClip, CompositeVideoClip, concatenate_videoclips


class TransitionType(Enum):
    """
    Class to represent the transition types (the way we
    join the videos between a transition).
    """
    FREEZE = 'freeze'
    """
    Freeze the last frame of the first video and the first
    frame ot he second video and make the transition with
    those static frames so the duration is extended by the
    transition duration.
    """
    PLAYING = 'playing'
    """
    Keep both video playing while the transition is run.
    """

class Transition:
    """
    Class to encapsulate all the transition methods we
    handle in our system. Each transition is a way of
    connecting two different videos.

    This class is built to be used within the
    TransitionGenerator class as parameter to build 
    videos with those transitions.
    """
    @staticmethod
    def handle_transition(video1, video2, duration: float = 0.5, transition_type: TransitionType = TransitionType.FREEZE, transition_method: type = 'Transition.slide'):
        """
        Create the transition between 'video1' and 'video2' and 
        return the items in the next order: video1, video2,
        transition.
        """
        video1 = VideoParser.to_moviepy(video1)
        video2 = VideoParser.to_moviepy(video2)

        if not NumberValidator.is_positive_number(duration):
            raise Exception(ErrorMessage.parameter_is_not_positive_number('duration'))
        # TODO: Maybe make 'duration' be multiple of frame_time
        # and multiple of a pair frame_time to allow the 
        # transition work equally in both videos
        
        if not PythonValidator.is_class_staticmethod(Transition, transition_method):
            # TODO: We have some methods we don't accept
            raise Exception('The provided "transition_method" parameter is not an static method of the Transition class.')
        
        transition = None
        # Handle transition and videos
        if transition_type == TransitionType.FREEZE:
            # Original videos are not modified
            transition_first_clip = ImageClip(VideoFrameExtractor.get_last_frame(video1), duration = duration).set_fps(60)
            transition_second_clip = ImageClip(VideoFrameExtractor.get_first_frame(video2), duration = duration).set_fps(60)
        elif transition_type == TransitionType.PLAYING:
            if duration > (video1.duration / 2) or duration > (video2.duration / 2):
                # TODO: Make this Exception more description (which video is wrong)
                # and talk about that we use the half of the provided duration
                raise Exception(f'The provided "duration" parameter {str(duration)} is not valid according to the provided video duration.')
            
            half_duration = duration / 2
            transition_first_clip = video1.subclip(video1.duration - half_duration, video1.duration)
            transition_second_clip = video2.subclip(0, half_duration)
            video1 = video1.subclip(0, video1.duration - half_duration)
            video2 = video2.subclip(half_duration, video2.duration)
        
        transition = transition_method(transition_first_clip, transition_second_clip, duration)

        return video1, transition, video2

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

        # Transition from last frame of video1 to first of video2
        transition_clip_1 = MoviepySetPosition(CoordinateCorner(0, 0), CoordinateCorner(-video1.w, 0), TFunctionSetPosition.linear, RateFunction.linear).apply(video1)
        # TODO: Maybe set 'transition_clip_1.pos' instead of (0, 0)
        transition_clip_2 = MoviepySetPosition(CoordinateCorner(video2.w, 0), CoordinateCorner(0, 0), TFunctionSetPosition.linear, RateFunction.linear).apply(video2)

        return CompositeVideoClip([
            transition_clip_1,
            transition_clip_2
        ])

class TransitionGenerator:
    """
    Class to simplify and encapsulate the functionality
    related to transition between videos
    """
    # TODO: This method is no longer being used due to the
    # code format we need to use due to we could change the
    # original videos so we need to update those instances
    @staticmethod
    def get_transition_clips(videos, duration: float = 0.5, transition_type: TransitionType = TransitionType.FREEZE, transition_method: type = Transition.slide):
        """
        Generate all the transition clips between the provided
        'videos' and with the also provided 'transition_method'
        (that must be a transition method within the Transition
        class).
        """
        # TODO: This method is a candidate for internal use only
        if not NumberValidator.is_positive_number(duration):
            raise Exception(ErrorMessage.parameter_is_not_positive_number('duration'))
        
        if not PythonValidator.is_class_staticmethod(Transition, transition_method):
            raise Exception('The provided "transition_method" parameter is not an static method of the Transition class.')
        
        transition_type = TransitionType.to_enum(transition_type)
        videos = [VideoParser.to_moviepy(video) for video in videos]

        transitions = []

        for video1, video2 in zip(videos, videos[1:]):
            transitions.append(TransitionGenerator.get_transition_clip(video1, video2, duration, transition_method, transition_type))

        return transitions

    @staticmethod
    def apply(videos, duration: float = 0.5, transition_type: TransitionType = TransitionType.FREEZE, transition_method: type = 'Transition.slide'):
        """
        Build a transition by using the provided 'transition_method' 
        (that must be a transition method within the Transition class)
        and put it between all the provided videos that are played
        completely before and after the transition.

        So, the sequence is the next.
        1. The 'videoX' is played completely.
        2. The transition is played completely.
        3. Go to step 1 with the next video until last one
        4. Last video is played completely
        """
        # TODO: Make the 'transition_method' more dynamic to
        # accept different transitions between clips so we
        # can handle all of them separately
        # TODO: 'transitions' array should be len(videos) - 1
        # and all members should be accepted transition methods
        if not NumberValidator.is_positive_number(duration):
            raise Exception(ErrorMessage.parameter_is_not_positive_number('duration'))

        if not PythonValidator.is_class_staticmethod(Transition, transition_method):
            raise Exception('The provided "transition_method" parameter is not an static method of the Transition class.')

        videos = [VideoParser.to_moviepy(video) for video in videos]
        transition_type = TransitionType.to_enum(transition_type)

        clips_to_concat = []
        prev_video2 = None
        for video1, video2 in zip(videos, videos[1:]):
            # TODO: The video2 changes, but I don't know if the for
            # loop keeps the object changed in the next iteration.
            # If it does just remove the 'prev_video2' var
            if prev_video2 is not None:
                video1 = prev_video2

            video1, transition, video2 = Transition.handle_transition(video1, video2, duration, transition_type, transition_method)
            clips_to_concat.extend([video1, video2, transition])
            prev_video2 = video2
        clips_to_concat.append(prev_video2)

        # transitions = TransitionGenerator.get_transition_clips(videos, duration, transition_method)
        # videos_to_concat = []

        # for video, transition in zip(videos[:-1], transitions):
        #     videos_to_concat.append(video)
        #     videos_to_concat.append(transition)
        # videos_to_concat.append(videos[-1])

        return concatenate_videoclips(clips_to_concat)

