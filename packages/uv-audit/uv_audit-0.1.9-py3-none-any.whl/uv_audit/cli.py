from typing import Optional

import typer

import uv_audit
from uv_audit.manager import UvAuditManager

cli = typer.Typer(help='uv-audit CLI')


def version_callback(value: bool):
    if value:
        print(f'Version of uv-audit is {uv_audit.__version__}')
        raise typer.Exit(0)


@cli.callback(invoke_without_command=True)
def callback(  # noqa: C901
    ctx: typer.Context,
    #
    version: bool = typer.Option(
        False,
        '--version',
        callback=version_callback,
        help='Print version of uv-audit.',
        is_eager=True,
    ),
    #
    verbose: bool = typer.Option(
        False,
        '--verbose',
        '-v',
        help='Run with verbose',
    ),
    #
    ignore: Optional[list[str]] = typer.Option(
        None,
        '--ignore',
        help='Ignore codes',
    ),
    # Setters
    extra: bool = typer.Option(
        True,
        '--extra',
        help='TODO',
        metavar='by default',
        rich_help_panel='uv-audit Options',
        show_default=False,
    ),
    dev: bool = typer.Option(
        True,
        '--dev',
        help='TODO',
        metavar='by default',
        rich_help_panel='uv-audit Options',
        show_default=False,
    ),
):
    uv_audit_manager = UvAuditManager()

    ignore_codes = []

    if ignore is not None:
        ignore_codes = [item for i in ignore for item in i.split(',')]

    uv_audit_manager.set_options(
        verbose=verbose,
        ignore_codes=ignore_codes,
        scan_extra_deps=dev,
        scan_dev_deps=dev,
    )

    errors = uv_audit_manager.scan()

    if errors > 1:
        raise typer.Exit(1)

    raise typer.Exit(0)


@cli.command('audit', hidden=True)
def audit_command():
    """Plug."""
    pass
