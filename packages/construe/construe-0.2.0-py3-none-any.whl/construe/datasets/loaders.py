"""
Managers for loading datasets
"""

import os
import glob

from .manifest import load_manifest
from .download import download_data
from ..exceptions import DatasetsError
from .path import dataset_archive, find_dataset_path, cleanup_dataset


__all__ = ["load_content_moderation", "cleanup_content_moderation"]


DATASETS = load_manifest()
CONTENT_MODERATION = "content-moderation"


def _info(dataset):
    if dataset not in DATASETS:
        raise DatasetsError(f"no dataset named {dataset} exists")
    return DATASETS[dataset]


def load_content_moderation(data_home=None):
    """
    Downloads the content moderation dataset if it does not exist then
    yields all of the paths for the images in the dataset.
    """
    info = _info(CONTENT_MODERATION)
    if not dataset_archive(CONTENT_MODERATION, info["signature"], data_home=data_home):
        # If the dataset does not exist, download and extract it
        info.update({"data_home": data_home, "replace": False, "extract": True})
        download_data(**info)

    data_path = find_dataset_path(CONTENT_MODERATION, fname=None, ext=None)
    for path in glob.glob(os.path.join(data_path, "**", "*")):
        yield path


def cleanup_content_moderation(data_home=None):
    """
    Removes the content moderation dataset and archive.
    """
    return cleanup_dataset(CONTENT_MODERATION, data_home=data_home)
