import os
from dataclasses import dataclass
from typing import Optional
import json
import yaml


@dataclass
class Range:
    start: int
    end: int
    timelinelabels: Optional[list[str]] = None


@dataclass
class Value:
    ranges: list[Range]
    timelinelabels: Optional[list[str]] = None


@dataclass
class Result:
    id: str
    from_name: str
    to_name: str
    type: str
    origin: str
    value: Value


@dataclass
class Annotation:
    id: int
    completed_by: int
    results: list[Result]


@dataclass
class VideoData:
    id: int
    video_url: str
    annotations: list[Annotation]


def load_video_dataset(annotations_file: str) -> list[VideoData]:
    with open(annotations_file, "r") as f:
        data_list = json.load(f)

    # Convert to dataclasses
    videos = []
    for item in data_list:
        annotations = []
        for ann in item["annotations"]:
            results = []
            for res in ann["result"]:
                ranges = [Range(**r) for r in res["value"]["ranges"]]
                value = Value(ranges=ranges, timelinelabels=res["value"].get("timelinelabels"))
                result = Result(
                    id=res["id"],
                    from_name=res["from_name"],
                    to_name=res["to_name"],
                    type=res["type"],
                    origin=res["origin"],
                    value=value
                )
                results.append(result)
            annotation = Annotation(id=ann["id"], completed_by=ann["completed_by"], results=results)
            annotations.append(annotation)
        video = VideoData(id=item["id"], video_url=item["data"]["video"], annotations=annotations)
        videos.append(video)
    return videos


def create_dataset_yaml(classes: set[str], dataset_dir: str):
    dataset_info = {
        "train": "./train",
        "val": "./val",
        "nc": len(classes),
        "names": list(classes)  # order doesn't matter here
    }

    yaml_path = os.path.join(dataset_dir, "dataset.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(dataset_info, f, default_flow_style=False, allow_unicode=True)
