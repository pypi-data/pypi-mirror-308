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

from nvcf.command.cloud_function import CloudFunctionCommand
from nvcf.printer.task_printer import TaskPrinter

from ngcbpc.command.clicommand import CLICommand
from ngcbpc.command.config import Configuration
from ngccli.modules.client import Client


class TaskCommand(CloudFunctionCommand):  # noqa: D101

    CMD_NAME = "task"
    DESC = "description of the task command"
    HELP = "Task Help"
    CMD_ALIAS = []

    TASK_ID_HELP = "Task ID"
    TASK_ID_METAVAR = "<task-id>"

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.client = Client()
        self.config = Configuration()
        self.printer = TaskPrinter()

    @CLICommand.arguments("target", metavar=TASK_ID_METAVAR, help=TASK_ID_HELP, type=str, default=None)
    @CLICommand.command(help="Info about a task", description="Info about a task")
    def info(self, args):  # noqa: D102
        resp = self.client.cloud_function.tasks.info(args.target)
        self.printer.print_info(resp.get("task", {}))
