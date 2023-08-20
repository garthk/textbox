"Command line."

import click

import textbox


@click.group()
def main() -> None:
    "Remember text for you, wholesale."


@main.command("import")
def import_() -> None:
    "Import text."


@main.group()
def plugins() -> None:
    "Manage textbox' plugins."


@plugins.command()
def list() -> None:  # noqa: A001
    "List textbox' plugins."


@click.command()
def version() -> None:
    "Print textbox' version."
    click.echo(f"{textbox.__name__} {textbox.__version__}")


@click.command("help")
@click.argument("subcmd", required=False)
@click.pass_context
def helf(ctx: click.Context, subcmd: str | None) -> None:
    '"Wait, wait, I guess it says HELF."'  # noqa: D400, D415
    if not subcmd:
        assert ctx.parent  # noqa: S101
        click.echo(ctx.parent.command.get_help(ctx.parent))
        return
    if subcmd_obj := main.get_command(ctx, subcmd):
        ctx.info_name = subcmd
        click.echo(subcmd_obj.get_help(ctx))
        return
    ctx.fail(f"No such command '{subcmd}'")


main.add_command(helf)
plugins.add_command(helf)
