from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.models.video import r3d_18, VideoResNet

from videoeventdetection.training.dataset import DatasetMetadata
from videoeventdetection.training.video import VideoDataset


@dataclass
class TrainConfig:
    frame_size: int
    frames_per_clip: int
    batch_size: int
    epoch_count: int
    learning_rate: float
    device: str


@dataclass
class DatasetLoaders:
    train: DataLoader
    val: DataLoader


def create_dataset_loaders(metadata: DatasetMetadata, config: TrainConfig) -> DatasetLoaders:
    video_transform = transforms.Compose([
        transforms.Resize((config.frame_size, config.frame_size)),
        transforms.Normalize(mean=[0.45, 0.45, 0.45], std=[0.225, 0.225, 0.225])
    ])

    train_dataset = VideoDataset(metadata.train_directories, metadata.label_indexes,
                                 config.frames_per_clip, transform=video_transform)
    val_dataset = VideoDataset(metadata.val_directories, metadata.label_indexes,
                               config.frames_per_clip, transform=video_transform)

    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=config.batch_size, shuffle=False)

    return DatasetLoaders(train=train_loader, val=val_loader)


def create_model(metadata: DatasetMetadata, config: TrainConfig) -> VideoResNet:
    model = r3d_18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, metadata.class_count)
    return model.to(config.device)


def train_model(model: VideoResNet, loaders: DatasetLoaders, config: TrainConfig):
    # Create optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)

    # Training loop
    for epoch in range(config.epoch_count):
        # Training
        model.train()
        running_loss = 0.0
        for videos, labels_batch in loaders.train:
            videos = videos.to(config.device).permute(0, 2, 1, 3, 4)  # B,C,T,H,W
            labels_batch = labels_batch.to(config.device)
            optimizer.zero_grad()
            outputs = model(videos)
            loss = criterion(outputs, labels_batch)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        avg_loss = running_loss / len(loaders.train)
        print(f"Epoch {epoch + 1}/{config.epoch_count}, Loss: {avg_loss:.4f}")

        # Validation
        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for videos, labels_batch in loaders.val:
                videos = videos.to(config.device).permute(0, 2, 1, 3, 4)
                labels_batch = labels_batch.to(config.device)
                outputs = model(videos)
                preds = torch.argmax(outputs, dim=1)
                correct += (preds == labels_batch).sum().item()
                total += labels_batch.size(0)
        val_acc = correct / total
        print(f"Validation Accuracy: {val_acc:.4f}")
