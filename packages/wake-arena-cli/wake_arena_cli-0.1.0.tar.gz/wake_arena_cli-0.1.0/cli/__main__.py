import logging

from cli import ui

logging.basicConfig(
    format="%(asctime)s,%(msecs)d [%(levelname)s] %(name)s: %(message)s",
    level=logging.CRITICAL,
)

import rich_click as click

from api.project_api import ProjectApi, ProjectApiError
from cli.check import check as check_command
from cli.config import config as config_command
from cli.init import init as init_command
from cli.project import project as project_command
from config.config import Config


@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)

    logger = logging.getLogger("CLI")
    config = Config()
    client = config.get_active_client()

    ctx.obj["logger"] = logger
    ctx.obj["config"] = config
    if client:
        api = ProjectApi(
            logger=logger, server_url=config.get_api_url(), token=client["token"]
        )
        ctx.obj["project_api"] = api

        project = config.get_active_project()
        if project:
            with ui.spinner("Checking configuration"):
                try:
                    api.get_project(project)
                except ProjectApiError as error:
                    if error.code == "NOT_FOUND":
                        ui.error(
                            title="Project not found",
                            lines=[
                                f"Project {project} does not exists, please call {ui.command('config project select')} first"
                            ],
                        )
                    else:
                        raise error

    else:
        ctx.obj["project_api"] = None
    pass


main.add_command(init_command)
main.add_command(check_command)
main.add_command(config_command)
main.add_command(project_command)

if __name__ == "__main__":
    main()
