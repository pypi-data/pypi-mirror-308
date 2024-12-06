#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#
from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Union

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.api.utils import disable_function, DotDict
from ngcbpc.constants import STAGING_ENV
from ngcbpc.util.utils import extra_args, get_environ_tag

if TYPE_CHECKING:
    import ngcsdk

    import ngccli.api.apiclient

    Client = Union[ngccli.api.apiclient.APIClient, ngcsdk.APIClient]


class TaskAPI:  # noqa: D101
    def __init__(self, connection: Connection = None, api_client: Client = None) -> None:
        self.connection = connection
        self.config = Configuration()
        self.client = api_client

    @staticmethod
    def _construct_task_endpoint(
        org_name: str,
        task_id: Optional[str] = None,
    ) -> str:
        parts = ["v2/orgs", org_name]

        parts.extend(["nvct", "tasks"])

        if task_id:
            parts.extend([task_id])

        return "/".join(parts)

    @disable_function(get_environ_tag() <= STAGING_ENV)
    def create(self):
        """Create a task with the specification provided by input.

        Returns:
            DotDict: Function Response provided by NVCF
        """
        self.config.validate_configuration()

    @disable_function(get_environ_tag() <= STAGING_ENV)
    def list(self) -> list[DotDict]:
        """List tasks available to the organization currently set.

        Returns:
            A list of task DotDicts.
        """
        self.config.validate_configuration()
        return []

    @extra_args
    def info(self, task_id: str) -> DotDict:
        """Get information about a given task.

        Returns:
            dict: DotDict of task information.
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        url = self._construct_task_endpoint(org_name, task_id)
        response = self.connection.make_api_request("GET", url, auth_org=org_name, operation_name="get task")
        return DotDict(response)

    @disable_function(get_environ_tag() <= STAGING_ENV)
    def delete(self):
        """Delete a task."""
        self.config.validate_configuration()

    @disable_function(get_environ_tag() <= STAGING_ENV)
    def cancel(self):
        """Cancel a task."""
        self.config.validate_configuration()

    @disable_function(get_environ_tag() <= STAGING_ENV)
    def get_events(self) -> list[DotDict]:
        """Get a list of the task's events."""
        self.config.validate_configuration()

    @disable_function(get_environ_tag() <= STAGING_ENV)
    def get_results(self) -> list[DotDict]:
        """Get a list of the tasks' results."""
        self.config.validate_configuration()
