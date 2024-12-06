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
    ctx.obj["project_api"] = (
        ProjectApi(
            logger=logger, server_url=config.get_api_url(), token=client["token"]
        )
        if client
        else None
    )


main.add_command(init_command)
main.add_command(check_command)
main.add_command(config_command)
main.add_command(project_command)

if __name__ == "__main__":
    main()
