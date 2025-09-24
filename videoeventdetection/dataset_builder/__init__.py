import os
import shutil

from .dataset import load_video_dataset, create_dataset_yaml
from .dataset_splitter import split_data
from .video_splitter import split_videos


def setup_cli(subparsers):
    parser = subparsers.add_parser("prepare-data")

    parser.add_argument("-i", "--input", help="Path to the annotations.json", required=True)
    parser.add_argument("-t", "--temp", help="Path to the temp directory", required=False, default="./temp")
    parser.add_argument("-o", "--output", help="Path where the output dataset should be", required=False,
                        default="./training-data")
    parser.add_argument("-r", "--ratio",
                        help="Ratio between train/val data (number between 0.0 to 1.0 represents the percentage of train data)",
                        required=False, default=0.8)

    parser.set_defaults(func=prepare_data)


def prepare_data(args):
    split_ratio = args.ratio  # <split_ratio> % train, <1.0 - split_ratio> % val
    input_dataset_dir = args.input
    output_dataset_dir = args.output
    temp_dir = args.temp

    print("Loading input dataset...")
    videos = load_video_dataset(os.path.join(input_dataset_dir, "annotations.json"))

    print("Downloading videos required for the dataset...")
    temp_videos_dir = os.path.join(temp_dir, "videos")
    temp_clips_dir = os.path.join(temp_dir, "clips")

    print("Preparing clips...")
    classes = split_videos(videos, temp_videos_dir, temp_clips_dir)
    split_data(temp_clips_dir, output_dataset_dir, split_ratio)

    print("Generating metadata file for the dataset...")
    create_dataset_yaml(classes, output_dataset_dir)

    print("Cleaning up temp files...")
    shutil.rmtree(temp_clips_dir)  # TODO Delete whole temp_dir

    print(f"Dataset finished and written to {output_dataset_dir}")
