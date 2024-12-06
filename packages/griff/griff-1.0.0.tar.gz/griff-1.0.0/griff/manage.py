import os

from griff.runtime.runtime_factory import RuntimeFactory

exec_profile = os.environ.get("EXEC_PROFILE", "dev")
cli_runtime = RuntimeFactory(env=exec_profile).cli_runtime().build()
cli_runtime.initialize()
cli_runtime.start()
cli = cli_runtime.get_typer()

if __name__ == "__main__":
    cli()
