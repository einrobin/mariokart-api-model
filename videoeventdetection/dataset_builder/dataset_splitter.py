import os
import random
import shutil


def split_data(source_dir: str, target_dir: str, split_ratio: float):
    for current_dir in os.listdir(source_dir):
        videos = [f for f in os.listdir(os.path.join(source_dir, current_dir)) if f.endswith(".mp4")]
        random.shuffle(videos)

        split_index = int(len(videos) * split_ratio)
        train_files = videos[:split_index]
        val_files = videos[split_index:]

        def move_files(file_list, target_dir):
            os.makedirs(target_dir, exist_ok=True)
            for vid_file in file_list:
                shutil.move(os.path.join(source_dir, current_dir, vid_file), os.path.join(target_dir, vid_file))

        move_files(train_files, os.path.join(target_dir, "train", current_dir))
        move_files(val_files, os.path.join(target_dir, "val", current_dir))
