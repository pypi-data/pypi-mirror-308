# coding: utf-8

from supervisely.collection.str_enum import StrEnum


class ProjectType(StrEnum):
    IMAGES = "images"
    VIDEOS = "videos"
    VOLUMES = "volumes"
    POINT_CLOUDS = "point_clouds"
    POINT_CLOUD_EPISODES = "point_cloud_episodes"



# Constants for multispectral and multiview projects.
_MULTISPECTRAL_TAG_NAME = "multispectral"
_MULTIVIEW_TAG_NAME = "multiview"
