import os

from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Dict , Union
from yt_dlp import YoutubeDL
from moviepy import VideoFileClip

def get_transcript(video_id: str) -> Union[List[Dict[str, str]], None]:
    """
    Fetches the transcript for a given YouTube video ID.
    
    :param video_id: The ID of the YouTube video.
    :return: A list of dictionaries containing the transcript.
    """

    try:
        # Attempt to fetch the transcript
        return YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        # If an error occurs, print it and return an empty list
        print(f"Error fetching transcript for video ID {video_id}: {e}")
    return None



def get_video_info(url: str) -> Dict[str, Union[str, int]]:
    """
    Fetches video information using yt-dlp.
    
    :param url: The URL of the YouTube video.
    :return: A dictionary containing important video information.
    Info includes fields are: id, title, description, channel, channel_id, channel_url, duration, duration_string, view_count, like_count, upload_date, uploader, webpage_url, categories, tags, age_limit, availability, language
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,  # Changed to False to get full info
    }
    
    # Important fields to extract
    important_fields = [
        'id',
        'title', 
        'description',
        'channel',
        'channel_id',
        'channel_url',
        'duration',
        'duration_string',
        'view_count',
        'like_count',
        'upload_date',
        'uploader',
        'webpage_url',
        'categories',
        'tags',
        'age_limit',
        'availability',
        'language'
    ]
    
    try:
        # Attempt to fetch video information
        if not url.startswith("https://www.youtube.com/watch?v="):
            raise ValueError("Invalid YouTube URL format.")
        with YoutubeDL(ydl_opts) as ydl:
            full_info = ydl.extract_info(url, download=False)
            
        # Extract only important fields
        filtered_info = {}
        for field in important_fields:
            if field in full_info:
                filtered_info[field] = full_info[field]

    except Exception as e:
        # If an error occurs, print it and return an empty dictionary
        print(f"Error fetching video info for URL {url}: {e}")
        return {}
    
    return filtered_info

def search_videos(keyword: str, max_results: int = 5, ydl_opts: Dict[str, Union[str, int, bool]] = None) -> List[Dict[str, Union[str, int]]]:
    """
    Searches YouTube for a given keyword and returns a list of video information.

    Args:
        keyword (str): The keyword to search for.
        max_results (int): Number of results to fetch (default is 5).
        ydl_opts (dict): Optional yt-dlp options to customize the search.
            Available options:
                username:          Username for authentication purposes.
                password:          Password for authentication purposes.
                videopassword:     Password for accessing a video.
                ap_mso:            Adobe Pass multiple-system operator identifier.
                ap_username:       Multiple-system operator account username.
                ap_password:       Multiple-system operator account password.
                usenetrc:          Use netrc for authentication instead.
                netrc_location:    Location of the netrc file. Defaults to ~/.netrc.
                netrc_cmd:         Use a shell command to get credentials
                verbose:           Print additional info to stdout.
                quiet:             Do not print messages to stdout.
                no_warnings:       Do not print out anything for warnings.
                forceprint:        A dict with keys WHEN mapped to a list of templates to
                                    print to stdout. The allowed keys are video or any of the
                                    items in utils.POSTPROCESS_WHEN.
                                    For compatibility, a single list is also accepted
                print_to_file:     A dict with keys WHEN (same as forceprint) mapped to
                                    a list of tuples with (template, filename)
                forcejson:         Force printing info_dict as JSON.
                dump_single_json:  Force printing the info_dict of the whole playlist
                                    (or video) as a single JSON line.
                force_write_download_archive: Force writing download archive regardless
                                    of 'skip_download' or 'simulate'.
                simulate:          Do not download the video files. If unset (or None),
                                    simulate only if listsubtitles, listformats or list_thumbnails is used
                format:            Video format code. see "FORMAT SELECTION" for more details.
                                    You can also pass a function. The function takes 'ctx' as
                                    argument and returns the formats to download.
                                    See "build_format_selector" for an implementation
                allow_unplayable_formats:   Allow unplayable formats to be extracted and downloaded.
                ignore_no_formats_error: Ignore "No video formats" error. Usefull for
                                    extracting metadata even if the video is not actually
                                    available for download (experimental)
                format_sort:       A list of fields by which to sort the video formats.
                                    See "Sorting Formats" for more details.
                format_sort_force: Force the given format_sort. see "Sorting Formats"
                                    for more details.
                prefer_free_formats: Whether to prefer video formats with free containers
                                    over non-free ones of the same quality.
                allow_multiple_video_streams:   Allow multiple video streams to be merged
                                    into a single file
                allow_multiple_audio_streams:   Allow multiple audio streams to be merged
                                    into a single file
                check_formats      Whether to test if the formats are downloadable.
                                    Can be True (check all), False (check none),
                                    'selected' (check selected formats),
                                    or None (check only if requested by extractor)
                paths:             Dictionary of output paths. The allowed keys are 'home'
                                    'temp' and the keys of OUTTMPL_TYPES (in utils/_utils.py)
                outtmpl:           Dictionary of templates for output names. Allowed keys
                                    are 'default' and the keys of OUTTMPL_TYPES (in utils/_utils.py).
                                    For compatibility with youtube-dl, a single string can also be used
                outtmpl_na_placeholder: Placeholder for unavailable meta fields.
                restrictfilenames: Do not allow "&" and spaces in file names
                trim_file_name:    Limit length of filename (extension excluded)
                windowsfilenames:  True: Force filenames to be Windows compatible
                                    False: Sanitize filenames only minimally
                                    This option has no effect when running on Windows
                ignoreerrors:      Do not stop on download/postprocessing errors.
                                    Can be 'only_download' to ignore only download errors.
                                    Default is 'only_download' for CLI, but False for API
                skip_playlist_after_errors: Number of allowed failures until the rest of
                                    the playlist is skipped
                allowed_extractors:  List of regexes to match against extractor names that are allowed
                overwrites:        Overwrite all video and metadata files if True,
                                    overwrite only non-video files if None
                                    and don't overwrite any file if False
                playlist_items:    Specific indices of playlist to download.
                playlistrandom:    Download playlist items in random order.
                lazy_playlist:     Process playlist entries as they are received.
                matchtitle:        Download only matching titles.
                rejecttitle:       Reject downloads for matching titles.
                logger:            A class having a `debug`, `warning` and `error` function where
                                    each has a single string parameter, the message to be logged.
                                    For compatibility reasons, both debug and info messages are passed to `debug`.
                                    A debug message will have a prefix of `[debug] ` to discern it from info messages.
                logtostderr:       Print everything to stderr instead of stdout.
                consoletitle:      Display progress in the console window's titlebar.
                writedescription:  Write the video description to a .description file
                writeinfojson:     Write the video description to a .info.json file
                clean_infojson:    Remove internal metadata from the infojson
                getcomments:       Extract video comments. This will not be written to disk
                                    unless writeinfojson is also given
                writeannotations:  Write the video annotations to a .annotations.xml file
                writethumbnail:    Write the thumbnail image to a file
                allow_playlist_files: Whether to write playlists' description, infojson etc
                                    also to disk when using the 'write*' options
                write_all_thumbnails:  Write all thumbnail formats to files
                writelink:         Write an internet shortcut file, depending on the
                                    current platform (.url/.webloc/.desktop)
                writeurllink:      Write a Windows internet shortcut file (.url)
                writewebloclink:   Write a macOS internet shortcut file (.webloc)
                writedesktoplink:  Write a Linux internet shortcut file (.desktop)
                writesubtitles:    Write the video subtitles to a file
                writeautomaticsub: Write the automatically generated subtitles to a file
                listsubtitles:     Lists all available subtitles for the video
                subtitlesformat:   The format code for subtitles
                subtitleslangs:    List of languages of the subtitles to download (can be regex).
                                    The list may contain "all" to refer to all the available
                                    subtitles. The language can be prefixed with a "-" to
                                    exclude it from the requested languages, e.g. ['all', '-live_chat']
                keepvideo:         Keep the video file after post-processing
                daterange:         A utils.DateRange object, download only if the upload_date is in the range.
                skip_download:     Skip the actual download of the video file
                cachedir:          Location of the cache files in the filesystem.
                                    False to disable filesystem cache.
                noplaylist:        Download single video instead of a playlist if in doubt.
                age_limit:         An integer representing the user's age in years.
                                    Unsuitable videos for the given age are skipped.
                min_views:         An integer representing the minimum view count the video
                                    must have in order to not be skipped.
                                    Videos without view count information are always
                                    downloaded. None for no limit.
                max_views:         An integer representing the maximum view count.
                                    Videos that are more popular than that are not
                                    downloaded.
                                    Videos without view count information are always
                                    downloaded. None for no limit.
                download_archive:  A set, or the name of a file where all downloads are recorded.
                                    Videos already present in the file are not downloaded again.
                break_on_existing: Stop the download process after attempting to download a
                                    file that is in the archive.
                break_per_url:     Whether break_on_reject and break_on_existing
                                    should act on each input URL as opposed to for the entire queue
                cookiefile:        File name or text stream from where cookies should be read and dumped to
                cookiesfrombrowser:  A tuple containing the name of the browser, the profile
                                    name/path from where cookies are loaded, the name of the keyring,
                                    and the container name, e.g. ('chrome', ) or
                                    ('vivaldi', 'default', 'BASICTEXT') or ('firefox', 'default', None, 'Meta')
                legacyserverconnect: Explicitly allow HTTPS connection to servers that do not
                                    support RFC 5746 secure renegotiation
                nocheckcertificate:  Do not verify SSL certificates
                client_certificate:  Path to client certificate file in PEM format. May include the private key
                client_certificate_key:  Path to private key file for client certificate
                client_certificate_password:  Password for client certificate private key, if encrypted.
                                    If not provided and the key is encrypted, yt-dlp will ask interactively
                prefer_insecure:   Use HTTP instead of HTTPS to retrieve information.
                                    (Only supported by some extractors)
                enable_file_urls:  Enable file:// URLs. This is disabled by default for security reasons.
                http_headers:      A dictionary of custom headers to be used for all requests
                proxy:             URL of the proxy server to use
                geo_verification_proxy:  URL of the proxy to use for IP address verification
                                    on geo-restricted sites.
                socket_timeout:    Time to wait for unresponsive hosts, in seconds
                bidi_workaround:   Work around buggy terminals without bidirectional text
                                    support, using fridibi
                debug_printtraffic:Print out sent and received HTTP traffic
                default_search:    Prepend this string if an input url is not valid.
                                    'auto' for elaborate guessing
                encoding:          Use this encoding instead of the system-specified.
                extract_flat:      Whether to resolve and process url_results further
                                    * False:     Always process. Default for API
                                    * True:      Never process
                                    * 'in_playlist': Do not process inside playlist/multi_video
                                    * 'discard': Always process, but don't return the result
                                                from inside playlist/multi_video
                                    * 'discard_in_playlist': Same as "discard", but only for
                                                playlists (not multi_video). Default for CLI
                wait_for_video:    If given, wait for scheduled streams to become available.
                                    The value should be a tuple containing the range
                                    (min_secs, max_secs) to wait between retries
                postprocessors:    A list of dictionaries, each with an entry
                                    * key:  The name of the postprocessor. See
                                            yt_dlp/postprocessor/__init__.py for a list.
                                    * when: When to run the postprocessor. Allowed values are
                                            the entries of utils.POSTPROCESS_WHEN
                                            Assumed to be 'post_process' if not given
                progress_hooks:    A list of functions that get called on download
                                    progress, with a dictionary with the entries
                                    * status: One of "downloading", "error", or "finished".
                                                Check this first and ignore unknown values.
                                    * info_dict: The extracted info_dict

                                    If status is one of "downloading", or "finished", the
                                    following properties may also be present:
                                    * filename: The final filename (always present)
                                    * tmpfilename: The filename we're currently writing to
                                    * downloaded_bytes: Bytes on disk
                                    * total_bytes: Size of the whole file, None if unknown
                                    * total_bytes_estimate: Guess of the eventual file size,
                                                            None if unavailable.
                                    * elapsed: The number of seconds since download started.
                                    * eta: The estimated time in seconds, None if unknown
                                    * speed: The download speed in bytes/second, None if
                                            unknown
                                    * fragment_index: The counter of the currently
                                                        downloaded video fragment.
                                    * fragment_count: The number of fragments (= individual
                                                        files that will be merged)

                                    Progress hooks are guaranteed to be called at least once
                                    (with status "finished") if the download is successful.
                postprocessor_hooks:  A list of functions that get called on postprocessing
                                    progress, with a dictionary with the entries
                                    * status: One of "started", "processing", or "finished".
                                                Check this first and ignore unknown values.
                                    * postprocessor: Name of the postprocessor
                                    * info_dict: The extracted info_dict

                                    Progress hooks are guaranteed to be called at least twice
                                    (with status "started" and "finished") if the processing is successful.
                merge_output_format: "/" separated list of extensions to use when merging formats.
                final_ext:         Expected final extension; used to detect when the file was
                                    already downloaded and converted
                fixup:             Automatically correct known faults of the file.
                                    One of:
                                    - "never": do nothing
                                    - "warn": only emit a warning
                                    - "detect_or_warn": check whether we can do anything
                                                        about it, warn otherwise (default)
                source_address:    Client-side IP address to bind to.
                impersonate:       Client to impersonate for requests.
                                    An ImpersonateTarget (from yt_dlp.networking.impersonate)
                sleep_interval_requests: Number of seconds to sleep between requests
                                    during extraction
                sleep_interval:    Number of seconds to sleep before each download when
                                    used alone or a lower bound of a range for randomized
                                    sleep before each download (minimum possible number
                                    of seconds to sleep) when used along with
                                    max_sleep_interval.
                max_sleep_interval:Upper bound of a range for randomized sleep before each
                                    download (maximum possible number of seconds to sleep).
                                    Must only be used along with sleep_interval.
                                    Actual sleep time will be a random float from range
                                    [sleep_interval; max_sleep_interval].
                sleep_interval_subtitles: Number of seconds to sleep before each subtitle download
                listformats:       Print an overview of available video formats and exit.
                list_thumbnails:   Print a table of all thumbnails and exit.
                match_filter:      A function that gets called for every video with the signature
                                    (info_dict, *, incomplete: bool) -> Optional[str]
                                    For backward compatibility with youtube-dl, the signature
                                    (info_dict) -> Optional[str] is also allowed.
                                    - If it returns a message, the video is ignored.
                                    - If it returns None, the video is downloaded.
                                    - If it returns utils.NO_DEFAULT, the user is interactively
                                        asked whether to download the video.
                                    - Raise utils.DownloadCancelled(msg) to abort remaining
                                        downloads when a video is rejected.
                                    match_filter_func in utils/_utils.py is one example for this.
                color:             A Dictionary with output stream names as keys
                                    and their respective color policy as values.
                                    Can also just be a single color policy,
                                    in which case it applies to all outputs.
                                    Valid stream names are 'stdout' and 'stderr'.
                                    Valid color policies are one of 'always', 'auto',
                                    'no_color', 'never', 'auto-tty' or 'no_color-tty'.
                geo_bypass:        Bypass geographic restriction via faking X-Forwarded-For
                                    HTTP header
                geo_bypass_country:
                                    Two-letter ISO 3166-2 country code that will be used for
                                    explicit geographic restriction bypassing via faking
                                    X-Forwarded-For HTTP header
                geo_bypass_ip_block:
                                    IP range in CIDR notation that will be used similarly to
                                    geo_bypass_country
                external_downloader: A dictionary of protocol keys and the executable of the
                                    external downloader to use for it. The allowed protocols
                                    are default|http|ftp|m3u8|dash|rtsp|rtmp|mms.
                                    Set the value to 'native' to use the native downloader
                compat_opts:       Compatibility options. See "Differences in default behavior".
                                    The following options do not work when used through the API:
                                    filename, abort-on-error, multistreams, no-live-chat,
                                    format-sort, no-clean-infojson, no-playlist-metafiles,
                                    no-keep-subs, no-attach-info-json, allow-unsafe-ext, prefer-vp9-sort.
                                    Refer __init__.py for their implementation
                progress_template: Dictionary of templates for progress outputs.
                                    Allowed keys are 'download', 'postprocess',
                                    'download-title' (console title) and 'postprocess-title'.
                                    The template is mapped on a dictionary with keys 'progress' and 'info'
                retry_sleep_functions: Dictionary of functions that takes the number of attempts
                                    as argument and returns the time to sleep in seconds.
                                    Allowed keys are 'http', 'fragment', 'file_access', 'extractor'
                download_ranges:   A callback function that gets called for every video with
                                    the signature (info_dict, ydl) -> Iterable[Section].
                                    Only the returned sections will be downloaded.
                                    Each Section is a dict with the following keys:
                                    * start_time: Start time of the section in seconds
                                    * end_time: End time of the section in seconds
                                    * title: Section title (Optional)
                                    * index: Section number (Optional)
                force_keyframes_at_cuts: Re-encode the video when downloading ranges to get precise cuts
                noprogress:        Do not print the progress bar
                live_from_start:   Whether to download livestreams videos from the start

                The following parameters are not used by YoutubeDL itself, they are used by
                the downloader (see yt_dlp/downloader/common.py):
                nopart, updatetime, buffersize, ratelimit, throttledratelimit, min_filesize,
                max_filesize, test, noresizebuffer, retries, file_access_retries, fragment_retries,
                continuedl, xattr_set_filesize, hls_use_mpegts, http_chunk_size,
                external_downloader_args, concurrent_fragment_downloads, progress_delta.

                The following options are used by the post processors:
                ffmpeg_location:   Location of the ffmpeg/avconv binary; either the path
                                    to the binary or its containing directory.
                postprocessor_args: A dictionary of postprocessor/executable keys (in lower case)
                                    and a list of additional command-line arguments for the
                                    postprocessor/executable. The dict can also have "PP+EXE" keys
                                    which are used when the given exe is used by the given PP.
                                    Use 'default' as the name for arguments to passed to all PP
                                    For compatibility with youtube-dl, a single list of args
                                    can also be used

                The following options are used by the extractors:
                extractor_retries: Number of times to retry for known errors (default: 3)
                dynamic_mpd:       Whether to process dynamic DASH manifests (default: True)
                hls_split_discontinuity: Split HLS playlists into different formats at
                                    discontinuities such as ad breaks (default: False)
                extractor_args:    A dictionary of arguments to be passed to the extractors.
                                    See "EXTRACTOR ARGUMENTS" for details.
                                    E.g. {'youtube': {'skip': ['dash', 'hls']}}
                mark_watched:      Mark videos watched (even with --simulate). Only for YouTube

                The following options are deprecated and may be removed in the future:

                break_on_reject:   Stop the download process when encountering a video that
                                    has been filtered out.
                                    - `raise DownloadCancelled(msg)` in match_filter instead
                force_generic_extractor: Force downloader to use the generic extractor
                                    - Use allowed_extractors = ['generic', 'default']
                playliststart:     - Use playlist_items
                                    Playlist item to start at.
                playlistend:       - Use playlist_items
                                    Playlist item to end at.
                playlistreverse:   - Use playlist_items
                                    Download playlist items in reverse order.
                forceurl:          - Use forceprint
                                    Force printing final URL.
                forcetitle:        - Use forceprint
                                    Force printing title.
                forceid:           - Use forceprint
                                    Force printing ID.
                forcethumbnail:    - Use forceprint
                                    Force printing thumbnail URL.
                forcedescription:  - Use forceprint
                                    Force printing description.
                forcefilename:     - Use forceprint
                                    Force printing final filename.
                forceduration:     - Use forceprint
                                    Force printing duration.
                allsubtitles:      - Use subtitleslangs = ['all']
                                    Downloads all the subtitles of the video
                                    (requires writesubtitles or writeautomaticsub)
                include_ads:       - Doesn't work
                                    Download ads as well
                call_home:         - Not implemented
                                    Boolean, true if we are allowed to contact the
                                    yt-dlp servers for debugging.
                post_hooks:        - Register a custom postprocessor
                                    A list of functions that get called as the final step
                                    for each video file, after all postprocessors have been
                                    called. The filename will be passed as the only argument.
                hls_prefer_native: - Use external_downloader = {'m3u8': 'native'} or {'m3u8': 'ffmpeg'}.
                                    Use the native HLS downloader instead of ffmpeg/avconv
                                    if True, otherwise use ffmpeg/avconv if False, otherwise
                                    use downloader suggested by extractor if None.
                prefer_ffmpeg:     - avconv support is deprecated
                                    If False, use avconv instead of ffmpeg if both are available,
                                    otherwise prefer ffmpeg.
                youtube_include_dash_manifest: - Use extractor_args
                                    If True (default), DASH manifests and related
                                    data will be downloaded and processed by extractor.
                                    You can reduce network I/O by disabling it if you don't
                                    care about DASH. (only for youtube)
                youtube_include_hls_manifest: - Use extractor_args
                                    If True (default), HLS manifests and related
                                    data will be downloaded and processed by extractor.
                                    You can reduce network I/O by disabling it if you don't
                                    care about HLS. (only for youtube)
                no_color:          Same as `color='no_color'`
                no_overwrites:     Same as `overwrites=False`

    Returns:
        list: A list of video information dicts.
    """
    search_url = f"ytsearch{max_results}:{keyword}"

    if ydl_opts is None:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'default_search': 'ytsearch',
            'ignoreerrors': True,
        }
    results = []
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=False)

        if 'entries' in info:
            for entry in info['entries']:
                if entry is None:
                    continue
                results.append({
                    'title': entry.get('title'),
                    'url': entry.get('webpage_url'),
                    'id': entry.get('id'),
                    'duration': entry.get('duration'),
                    'view_count': entry.get('view_count'),
                    'upload_date': entry.get('upload_date'),
                    'channel': entry.get('channel'),
                })
    return results



def download_youtube_video(url: str, save_dir: str = "./downloads", cookie_file: str = None) -> str:
    """Robustly downloads the best available version of a YouTube video."""
    os.makedirs(save_dir, exist_ok=True)

    ydl_opts = {
     #   "format": "(bv*[ext=mp4]+ba[ext=m4a])/(bv*+ba/best)/best",
        "outtmpl": os.path.join(save_dir, "%(title)s.%(ext)s"),
    }
    if cookie_file:
        ydl_opts["cookiefile"] = cookie_file

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return os.path.abspath(ydl.prepare_filename(info))


def convert_webm_to_mp4(input_file: str, output_file: str = None) -> str:
    """
    Converts a .webm video to .mp4 using MoviePy.
    
    :param input_file: Path to the input .webm file.
    :param output_file: Optional path for the output .mp4 file.
    :return: The absolute path of the saved MP4.
    """
    if output_file is None:
        # Default output name if not provided
        name, _ = os.path.splitext(input_file)
        output_file = f"{name}.mp4"

    clip = VideoFileClip(input_file)
    clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    return os.path.abspath(output_file)

if __name__ == "__main__":
    from pprint import pprint
    # Example usage
    video_id = "3B-X3c5c9Sc"   # Replace with your YouTube video ID
    # transcript = get_transcript(video_id)

    # print("Transcript for video ID:", type(transcript))
    # video_info = get_video_info(f"https://www.youtube.com/watch?v={video_id}")
    # print("Important video information fields:")
    list_of_videos = search_videos("Python programming", max_results=5)

    with open("videos_list.json", "w") as f:
        import json
        json.dump(list_of_videos, f, indent=4)
    pprint(list_of_videos)


