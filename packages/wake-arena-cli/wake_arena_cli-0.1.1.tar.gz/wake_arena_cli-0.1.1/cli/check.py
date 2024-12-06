import asyncio
import datetime
import json
import os
import subprocess
import sys
import time
import webbrowser
from enum import Enum
from pathlib import Path

import dateutil.parser
import requests
import rich_click as click
from typing_extensions import Self

import cli.ui as ui
from api.project_api import ProjectApi, ProjectApiError
from config import Config
from wake.cli.compile import compile
from wake.config import WakeConfig

WAKE_FILE = ".wake/sources.json"
CHECK_TIMEOUT_IN_S = 60 * 10  # 10 minutes
UPLOAD_CONFIRM_TIMEOUT_IN_S = 60 * 3  # 3 minutes


class CheckState(Enum):
    VERIFICATION = "VERIFICATION"
    WAITING_FOR_UPLOAD = "WAITING_FOR_UPLOAD"
    WAITING_FOR_CHECK = "WAITING_FOR_CHECK"
    FETCHING_CODE = "FETCHING_CODE"
    CHECKING = "CHECKING"
    FINISHED = "FINISHED"
    ERROR = "ERROR"


class WakeExportError(click.ClickException):
    def __init__(self, message: str, help: str):
        super().__init__(message)
        self.help = help


class WakeExport:
    WAKE_MIN_VERSION = "4.13.1"

    def __init__(self, file: str):
        self.file = file
        self.sources = {}
        self.file_size = 0

        if not Path(self.file).is_file():
            return

        with open(self.file) as content:
            self.sources = json.load(content)
            self.file_size = Path(self.file).stat().st_size

    def validate(self) -> Self:
        if not self.sources:
            raise WakeExportError(
                "No compilation export file found, nothing to check",
                "Check the compilation output for errors",
            )

        if self.sources.get("version") != self.WAKE_MIN_VERSION:
            raise WakeExportError(
                "Invalid Wake version in export",
                f"Run export again with Wake version >= ${self.WAKE_MIN_VERSION}",
            )

        sources = self.sources.get("sources")

        if not sources or len(sources) == 0:
            raise WakeExportError(
                "Empty export, nothing to check",
                "Use non-empty directory. Check the compilation output for errors",
            )

        return self

    def upload(self, url: str):
        headers = {"Content-Type": "application/json"}
        res = requests.put(url, data=json.dumps(self.sources), headers=headers)

        if res.status_code != 200:
            raise WakeExportError("Upload not successful", res.content)


def is_final_state(state: str):
    return state in [CheckState.FINISHED.value, CheckState.ERROR.value]


def upload_export(
    project_api: ProjectApi, project_id: str, export: WakeExport, name: str | None
):
    check_id = None

    with ui.spinner("Requesting upload") as spinner:
        upload = project_api.get_upload_link(project_id, name)

        upload_link = upload.get("link")
        check_id = upload.get("checkId")

        if not upload_link or not check_id:
            raise WakeExportError("Upload was not successful", "Please try again")

        spinner.update("Uploading")
        export.upload(upload_link)

    return check_id


def wait_for_server_upload_confirm(api: ProjectApi, project_id: str, check_id: str):
    state = None

    with ui.spinner("Waiting for server confirmation"):
        timeout = time.time() + UPLOAD_CONFIRM_TIMEOUT_IN_S

        while True:
            if time.time() > timeout:
                raise WakeExportError(
                    "Timeout: Server didn't confirmed export upload", "Please try again"
                )

            check = api.get_vulnerability_check(project_id, check_id)
            status = check.get("status")

            if status != "PREPARATION":
                break

            time.sleep(1)

    return state


def wait_for_server_execution(project_api: ProjectApi, project_id: str, check_id: str):
    with ui.spinner("Waiting for the remote execution") as spinner:
        timeout = time.time() + CHECK_TIMEOUT_IN_S

        last_log_time = None
        check_state = None

        while True:
            if time.time() > timeout:
                raise WakeExportError(
                    "Timeout: Server didn't executed the check",
                    "Please try again or contact ABCH",
                )
            state_logs = project_api.get_vulnerability_check_state_logs(
                project_id, check_id, last_log_time
            )

            new_logs = state_logs.get("logs")
            if len(new_logs):
                for log in new_logs:
                    log_time = dateutil.parser.parse(log.get("createTime"))
                    ui.log(log_time, log.get("message"))
                last_log_time = new_logs[-1].get("createTime")

            curr_state = state_logs.get("state")
            if curr_state != check_state:
                check_state = curr_state
                if check_state == CheckState.CHECKING.value:
                    spinner.update("Server is checking the code")

            if is_final_state(check_state):
                break

            time.sleep(1)

        spinner.update("Getting results")
        check = project_api.get_vulnerability_check(project_id, check_id)
        check_state = check.get("status")

        if check_state == CheckState.ERROR.value:
            raise WakeExportError("Remote execution failed", check.get("error"))


@click.command("check")
@click.option("-n", "--name", help="Name for the performed check")
@click.option("-p", "--project", help="Project")
@click.pass_context
def check(ctx, name, project):
    """Performs remote Wake detection connected to Wake Arena project"""

    try:
        config: Config = ctx.obj.get("config")
        project_api: ProjectApi = ctx.obj.get("project_api")

        project_id = project if project else config.get_active_project()

        if not project_api or not project_id:
            ui.error(f"Please use INIT command first")
            return

        with ui.spinner("Checking configuration"):
            try:
                project_api.get_project(project_id)
            except ProjectApiError as error:
                if error.code == "NOT_FOUND":
                    ui.error(
                        title="Project not found",
                        lines=[
                            f"Project {project_id} does not exist, please call PROJECT SELECT command first"
                        ],
                    )
                    sys.exit(1)
                else:
                    raise error

        ui.section_start(f"Compiling the source (Wake {WakeExport.WAKE_MIN_VERSION})")

        subprocess.run(["wake", "compile", "--export", "json"])

        ui.section_end()

        output_file = os.getcwd() + "/" + WAKE_FILE
        export = WakeExport(output_file).validate()

        check_id = upload_export(project_api, project_id, export, name)

        ui.section_start("Export uploaded, waiting for code check")

        wait_for_server_upload_confirm(project_api, project_id, check_id)
        wait_for_server_execution(project_api, project_id, check_id)

        ui.section_end()

        result_url = f"{config.get_web_url()}/project/{project_id}/check/{check_id}"

        ui.success(
            title="Check is completed",
            lines=["Results are available at", ui.highlight(result_url)],
        )
        webbrowser.open(result_url)

    except WakeExportError as err:
        ui.error(title=err.message, lines=[err.help])
        sys.exit(1)
