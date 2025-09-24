import os
import yaml


class DatasetMetadata:
    def __init__(self, classes: list[str], class_count: int, train_directories: list[str], val_directories: list[str]):
        self.classes = classes
        self.class_count = class_count
        self.train_directories = train_directories
        self.val_directories = val_directories
        self.label_indexes = list(range(class_count))


def load_dataset_metadata(dataset_dir: str):
    with open(os.path.join(dataset_dir, "dataset.yaml")) as f:
        dataset_yaml = yaml.safe_load(f)

    classes = dataset_yaml["names"]
    train_dirs = [os.path.join(dataset_dir, dataset_yaml["train"], cls) for cls in classes]
    val_dirs = [os.path.join(dataset_dir, dataset_yaml["val"], cls) for cls in classes]

    return DatasetMetadata(classes=classes, class_count=dataset_yaml["nc"],
                           train_directories=train_dirs, val_directories=val_dirs)
