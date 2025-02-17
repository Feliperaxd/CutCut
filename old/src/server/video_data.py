
__all__ = ['VideoData']
__author__ = 'Felipe Amaral'
__version__ = '0.1'

from typing import Any, Dict, Optional    

from paths import Paths
from utils import Utils
from constants import VideoErrorType


class VideoData:
    """
    Represents video details including metadata and status information.
    """


    def __init__(
        self: 'VideoData',
        *,
        tag: Optional[str],
        url: Optional[str],
        title: Optional[str],
        duration: Optional[str],
        thumbnail: Optional[str],
        view_count: Optional[str],
        live_status: Optional[str],
        channel_tag: Optional[str],
        channel_url: Optional[str],
        channel_name: Optional[str],
        channel_is_verified: Optional[bool],
        error_code: Optional[str],
    ) -> None:
        """
        Parameters:
            - tag (Optional[str]): Unique identifier or tag for the video.
            - url (Optional[str]): URL of the video.
            - title (Optional[str]): Title of the video.
            - duration (Optional[str]): Duration of the video, formatted 
                as a string.
            - thumbnail (Optional[str]): URL of the video's thumbnail image.
            - view_count (Optional[str]): Number of views the video has, 
                formatted as a string.
            - live_status (Optional[str]): Live status of the video 
                (e.g., "live", "upcoming", "ended").
            - channel_tag (Optional[str]): Unique identifier or tag for the 
                video channel.
            - channel_url (Optional[str]): URL of the channel hosting the video.
            - channel_name (Optional[str]): Name of the channel hosting the video.
            - channel_is_verified (Optional[bool]): Indicates if the channel 
                is verified.
            - error_code (Optional[str]): Error code associated with video 
                retrieval, if any.
        """

        self.tag = tag
        self.url = url
        self.title = title
        self.duration = self._format_duration(duration)
        self.thumbnail = thumbnail
        self.view_count = self._format_view_count(view_count)
        self.live_status = live_status
        self.channel_tag = channel_tag
        self.channel_url = channel_url
        self.channel_name = channel_name
        self.channel_is_verified = channel_is_verified
        self.error_code = error_code

    @classmethod
    def from_defaults(
        cls: 'VideoData', 
        type_: VideoErrorType
    ) -> "VideoData":
        """
        Factory method to create a VideoData instance with default values.

        Parameters:
            - type_ (VideoErrorType): The error type to load default data for.

        Returns:
            - VideoData: A VideoData instance with default values.
        """

        default_data_path = Paths.CONFIG / 'default_video_details.json'
        data = Utils.get_data_from_json(default_data_path)
        return cls(**data[type_.value])

    def is_live(
        self: 'VideoData'
    ) -> bool:
        """
        Checks if the video is live.

        Returns:
            - bool: True if the video is live, otherwise False.
        """

        return self.live_status == "is_live"

    def to_dict(
        self: 'VideoData'
    ) -> Dict[str, Any]:
        """
        Converts the video data to a dictionary.

        Returns:
            - Dict[str, Any]: A dictionary representation of the video data.
        """

        return vars(self)

    @staticmethod
    def _format_duration(
        duration: Optional[str]
    ) -> Optional[str]:
        """
        Formats a given duration into a standard time format (hh:mm:ss).

        This method takes a string representing the duration and converts it 
        into a standard time format. If no duration is provided, it returns None.

        Parameters:
            - duration (Optional[str]): The duration to format, typically in 
                string format like '1:10:10'. 

        Returns:
            - Optional[str]: The formatted duration as a string (e.g., '01:10:10') 
                or None if no duration is provided.
        """
        
        return Utils.format_time(duration) if duration else None

    @staticmethod
    def _format_view_count(
        view_count: Optional[str]
    ) -> Optional[str]:
        """
        Format view count to a compact number representation.

        Parameters:
            - view_count (Optional[str]): The view count as a string.

        Returns:
            - Optional[str]: The formatted compact number representation, 
                or None if view_count is None.
        """

        return Utils.format_compact_number(view_count) if view_count else None
