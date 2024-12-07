import os
from pathlib import Path

import pydantic
import pyfzf
from rich import print
import typer
import yaml

from kb_cli import __version__

app = typer.Typer()


class Config(pydantic.BaseModel):
    fps: list[Path]


CONFIG_FP = Path(os.environ["HOME"]) / ".config/kb_cli.yaml"
if not CONFIG_FP.exists():
    CONFIG_FP.write_text("fps: []")
with open(CONFIG_FP, "r") as f:
    CONFIG = Config.model_validate(yaml.load(f, Loader=yaml.FullLoader))


@app.command()
def add(fp: Path):
    CONFIG.fps.append(fp)
    with open(CONFIG_FP, "w") as f:
        yaml.dump(CONFIG.model_dump(mode="json"), f)
    print("Added", fp)


@app.command()
def search():
    kb = {}
    for fp in CONFIG.fps:
        with open(fp, "r") as f:
            kb.update(yaml.load(f, Loader=yaml.FullLoader))
    if not kb:
        print("No knowledge base found")
        return

    fzf = pyfzf.FzfPrompt()
    choice = fzf.prompt(kb.keys())
    if len(choice) == 0:
        print("No choice made")
        return
    result = kb[choice[0]]
    print("-" * 20)
    print("choice:", choice[0])
    print("-" * 20)
    print(result)


@app.command()
def version():
    print(__version__)


if __name__ == "__main__":
    app()
