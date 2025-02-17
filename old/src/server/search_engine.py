
__all__ = ['SearchEngine']
__author__ = 'Felipe Amaral'
__version__ = '0.1'

import yt_dlp
import logging

from typing import (
    Any, Dict, Generator, 
    List, Optional
)

from video_data import VideoData
from constants import VideoErrorType


class SearchEngine:
    """To perform video searches and process video details."""


    def __init__(
        self: 'SearchEngine'
    ) -> None:
        """
        Attributes:
            - logger (logging.Logger): Logger instance for logging operations.
            - ydl_opts (Dict[str, Any]): Options to configure YouTube-DL or similar
                extractor tools. These options control aspects like verbosity,
                warning suppression, and extraction behavior.
        """

        self.logger = logging.getLogger('search_engine')
        self.logger.info("'search_engine' logger test!")
        
        self.ydl_opts = {
            "quiet": True,                
            "no_warnings": True,           
            "extract_flat": True,          
            "force_generic_extractor": True
        }

    def search(
        self: 'SearchEngine', 
        query: str,
        max_results: Optional[int] = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for videos on YouTube by query.

        Parameters:
            - query (str): Search query string.
            - max_results (Optional[int]): Maximum number of results. Defaults to 5.

        Returns:
            - List[Dict[str, Any]]: List of video details as dictionaries.
        """

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                results = ydl.extract_info(
                    f"ytsearch{max_results}:{query}", download=False
                )

                if 'entries' in results:
                    return list(self._filter_video_details(results['entries']))
                else:
                    return [
                        VideoData.from_defaults(
                            VideoErrorType.NOT_AVAILABLE
                        ).to_dict()
                    ]
            
            except Exception as e:
                self.logger.error(
                    (
                        f'Error during search: {e}\n'
                        f'Query: {query}\n'
                        f'Max Results: {max_results}'
                    )
                )
                return [
                    VideoData.from_defaults(
                        VideoErrorType.UNKNOWN_ERROR
                    ).to_dict()
                ]

    def search_by_url(
        self: 'SearchEngine', 
        url: str
    ) -> List[Dict[str, Any]]:
        """
        Search for video details using a YouTube URL.

        Parameters:
            - url (str): YouTube video URL.

        Returns:
            - List[Dict[str, Any]]: List of video details as dictionaries.
        """

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                results = ydl.extract_info(url=url, download=False)
                return list(self._filter_video_details([results]))
            
            except yt_dlp.utils.DownloadError:
                return [
                    VideoData.from_defaults(
                        VideoErrorType.NOT_VALID
                    ).to_dict()
                ]
            
            except Exception as e:
                self.logger.error(
                    (
                        f'Error during search by URL: {e}\n'
                        f'Query: {url}'
                    )
                )
                return [
                    VideoData.from_defaults(
                        VideoErrorType.UNKNOWN_ERROR
                    ).to_dict()
                ]
            
    def _filter_video_details(
        self: 'SearchEngine',
        raw_data: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Filter and format raw video details.

        Parameters:
            - raw_data (List[Dict[str, Any]]): Raw video details from yt_dlp.

        Yields:
            - Dict[str, Any]: Processed video details as dictionaries.
        """

        for data in raw_data:
            video = VideoData(
                tag=self._get_or_default(data, 'id', 'tag'),
                url=self._get_or_default(data, 'url'),
                title=self._get_or_default(data, 'title'),
                duration=self._get_or_default(data, 'duration'),
                thumbnail=self._get_best_thumbnail(data.get('thumbnails')),
                view_count=self._get_or_default(data, 'view_count'),
                live_status=self._get_or_default(data, 'live_status'),
                channel_tag=self._get_or_default(data, 'channel_id', 'channel_tag'),
                channel_url=self._get_or_default(data, 'channel_url'),
                channel_name=self._get_or_default(data, 'uploader', 'channel_name'),
                channel_is_verified=self._get_or_default(data, 'channel_is_verified'),
                error_code=None,
            )
            if video.is_live():
                video = VideoData.from_defaults(
                    VideoErrorType.NOT_ALLOWED
                )
            yield video.to_dict()

    def _get_or_default(
        self: 'SearchEngine',
        data: Dict[str, Any],
        data_key: str,
        default_key: Optional[str] = None,
    ) -> Any:
        """
        Retrieve a value from data or fallback to a default.

        Parameters:
            - data (Dict[str, Any]): Dictionary containing video data.
            - data_key (str): Key to retrieve from the data.
            - default_key (Optional[str]): Key to retrieve from the defaults 
                if data_key is missing.

        Returns:
            - Any: Retrieved value or default.
        """

        default_key = default_key or data_key
        default_attr = getattr(
            VideoData.from_defaults(VideoErrorType.NOT_AVAILABLE), default_key
        )
        return data.get(data_key, default_attr)

    def _get_best_thumbnail(
        self: 'SearchEngine', 
        thumbnails: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Select the best thumbnail from a list.

        Parameters:
            - thumbnails (Optional[List[Dict[str, Any]]]): List of thumbnail dictionaries.

        Returns:
            - str: URL of the best thumbnail.
        """

        default_thumbnail = VideoData.from_defaults(
            VideoErrorType.NOT_AVAILABLE
        ).thumbnail

        if not thumbnails:
            return default_thumbnail
        
        best_thumbnail = max(
            thumbnails, key=lambda x: x.get('preference', float('-inf'))
        )
        return best_thumbnail.get('url', default_thumbnail)
