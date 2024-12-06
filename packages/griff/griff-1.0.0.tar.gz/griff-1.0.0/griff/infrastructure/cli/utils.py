import typer

from griff.infrastructure.cli.commands.typer_print import TyperPrint


def _check_process_run(p, action: str):
    if p.returncode != 0:
        TyperPrint.error(f"{action} has failed")
        raise typer.Exit()
