import os
import uuid
from urllib.parse import urlparse

from moviepy.editor import VideoFileClip

from .download.file_downloader import download_file
from .player_notation import extract_player_notation
from .dataset import VideoData


def split_videos(videos: list[VideoData], video_dir: str, target_dir: str) -> set[str]:
    os.makedirs(video_dir, exist_ok=True)
    classes = set()

    for video in videos:
        video_url = video.video_url
        video_filename = os.path.join(video_dir, os.path.basename(urlparse(video_url).path))

        # Download Video
        download_file(video_url, video_filename)

        # Load video
        clip = VideoFileClip(video_filename)
        width, height = clip.size
        real_fps = clip.reader.nframes / clip.duration

        # --- Process annotations ---
        for ann in video.annotations:
            for result in ann.results:
                if result.type != "timelinelabels":
                    continue

                ranges = result.value.ranges
                labels = result.value.timelinelabels

                for label in labels:
                    player_notation, base_label = extract_player_notation(label)
                    classes.add(base_label)

                    screen_regions = player_notation.get_screen_regions(width, height)
                    for screen_region in screen_regions:
                        roi = screen_region.get_absolute_region_of_interest()

                        os.makedirs(os.path.join(target_dir, base_label), exist_ok=True)

                        for i, r in enumerate(ranges, start=1):
                            start = r.start / 24
                            end = r.end / 24

                            subclip = clip.subclip(start, end).crop(x1=roi[0], y1=roi[1],
                                                                    x2=roi[2], y2=roi[3])
                            out_path = os.path.join(target_dir, base_label,
                                                    f"clip_{str(uuid.uuid4()).replace('-', '')}.mp4")
                            subclip.write_videofile(out_path, codec="libx264", audio=False)
    return classes
