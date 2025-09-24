import glob
import os

import torch
from torch.utils.data import Dataset
from torchvision.io import read_video


def pad_or_subsample(frames, target_frames):
    T = frames.shape[0]
    if T < target_frames:
        pad = frames[-1].unsqueeze(0).repeat(target_frames - T, 1, 1, 1)
        frames = torch.cat([frames, pad], dim=0)
    elif T > target_frames:
        idxs = torch.linspace(0, T - 1, target_frames).long()
        frames = frames[idxs]
    return frames


class VideoDataset(Dataset):
    def __init__(self, root_dirs, labels, clip_frame_count, transform=None):
        """
        root_dirs: List of folders, one per class
        labels: List of integer labels
        """
        self.video_files = []
        self.video_labels = []
        self.clip_frame_count = clip_frame_count
        self.transform = transform
        for folder, label in zip(root_dirs, labels):
            files = glob.glob(os.path.join(folder, "*.mp4"))
            self.video_files.extend(files)
            self.video_labels.extend([label] * len(files))

    def __len__(self):
        return len(self.video_files)

    def __getitem__(self, idx):
        path = self.video_files[idx]
        video, _, _ = read_video(path, pts_unit='sec')  # video: T,H,W,C
        video = video.permute(0, 3, 1, 2).float() / 255.0  # T,C,H,W
        video = pad_or_subsample(video, self.clip_frame_count)
        if self.transform:
            video = self.transform(video)
        label = self.video_labels[idx]
        return video, label
