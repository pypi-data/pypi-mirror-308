"""
---
title: "Utilities - Client"
slug: "sdk-ref-utilities-client"
hidden: false
metadata:
  title: "Utilities - Client"
  description: "Encord SDK Utilities - Client."
category: "64e481b57b6027003f20aaa0"
---
"""

import pprint
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, List, Optional, Set, TypeVar, Union

from encord.common.time_parser import parse_datetime


def pretty_print(data):
    return pprint.pformat(data, indent=4, width=10)


class APIKeyScopes(Enum):
    """
    The APIKeyScope is used to provide specific access rights to a project through
    :meth:`.EncordUserClient.create_project_api_key`. The options are a follows:

        * ``LABEL_READ``: access to
          :ref:`tutorials/projects:Getting label rows`
        * ``LABEL_WRITE``: access to
          :ref:`tutorials/projects:Saving label rows`
        * ``MODEL_INFERENCE``: access to
          :ref:`tutorials/projects:Inference`
        * ``MODEL_TRAIN``: access to
          :ref:`tutorials/projects:Creating a model row` and
          :ref:`tutorials/projects:Training`
        * ``LABEL_LOGS_READ``: access to
          :ref:`tutorials/projects:Reviewing label logs`
        * ``ALGO_LIBRARY``: access to algorithms like
          :ref:`tutorials/projects:Object interpolation`

    """

    LABEL_READ = "label.read"
    LABEL_WRITE = "label.write"
    MODEL_INFERENCE = "model.inference"
    MODEL_TRAIN = "model.train"
    LABEL_LOGS_READ = "label_logs.read"
    ALGO_LIBRARY = "algo.library"


@dataclass
class LocalImport:
    """
    file_path:
        Supply the path of the exported folder which contains the images and `annotations.xml` file. Make
        sure to select "Save images" when exporting your CVAT Task or Project.
    transform_file_names:
        Encord expects that file names (including their relative paths), exactly matches the
        "name" parameter of CVAT image.
        If it is not, user can supply transform_file_names function that maps filename to the image name.
    """

    file_path: str
    map_filename_to_cvat_name: Optional[Callable[[str], str]] = None


ImportMethod = LocalImport
"""Using images/videos in cloud storage as an alternative import method will be supported in the future."""


@dataclass
class Issue:
    """
    For each `issue_type` there may be multiple occurrences which are documented in the `instances`. The `instances`
    list can provide additional information on how the issue was encountered. If there is no additional information
    available, the `instances` list will be empty.
    """

    issue_type: str
    instances: List[str]


@dataclass
class Issues:
    """
    Any issues that came up during importing a project. These usually come from incompatibilities between data saved
    on different platforms.
    """

    errors: List[Issue]
    warnings: List[Issue]
    infos: List[Issue]

    @staticmethod
    def from_dict(d: dict) -> "Issues":
        errors, warnings, infos = [], [], []
        for error in d["errors"]:
            issue = Issue(issue_type=error["issue_type"], instances=error["instances"])
            errors.append(issue)
        for warning in d["warnings"]:
            issue = Issue(issue_type=warning["issue_type"], instances=warning["instances"])
            warnings.append(issue)
        for info in d["infos"]:
            issue = Issue(issue_type=info["issue_type"], instances=info["instances"])
            infos.append(issue)
        return Issues(errors=errors, warnings=warnings, infos=infos)


@dataclass
class CvatImporterSuccess:
    project_hash: str
    dataset_hash: str
    issues: Issues


@dataclass
class CvatImporterError:
    dataset_hash: str
    issues: Issues


def optional_datetime_to_iso_str(key: str, val: Optional[Union[str, datetime]]) -> Optional[str]:
    if not val:
        return None
    if isinstance(val, str):
        return parse_datetime(val).isoformat()
    if isinstance(val, datetime):
        return val.isoformat()
    else:
        raise ValueError(f"Value for {key} should be a datetime")


T = TypeVar("T")


def optional_set_to_list(s: Optional[Set[T]]) -> Optional[List[T]]:
    if s is None:
        return s
    else:
        return list(s)
