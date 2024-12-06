from pathlib import Path
from typing import Optional

from hydra import compose, initialize_config_dir
from hydra.utils import instantiate
from typer import Argument, Typer

from .config import Configuration


def run(path: Path, name: str, dry_run: bool = False) -> Configuration:
    config = Configuration.load(path, name)
    config.run(dry_run=dry_run)
    return config


def run_hydra(path: str = "", overrides: Optional[list[str]] = Argument(None), dry_run: bool = False) -> Configuration:  # noqa: B008
    path = Path(path)
    if not isinstance(overrides, list):
        # maybe running via python, reset
        overrides = []
    with initialize_config_dir(config_dir=str(path.parent.absolute()), version_base=None):
        cfg = compose(config_name=str(path.name), overrides=overrides)
        config = instantiate(cfg)
        if not isinstance(config, Configuration):
            config = Configuration(**config)
        config.run(dry_run=dry_run)
    return config


def main() -> None:
    app = Typer()
    app.command("run")(run)
    app.command("hydra")(run_hydra)
    app()
