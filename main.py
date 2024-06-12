import typer
from typing_extensions import Annotated

from cli.auto_command import auto_command
from cli.manual_command import manual_command
from enums import AvailableLLM
from utils import suppress_stderr

app = typer.Typer()

@app.command()
def auto(
    file_path: Annotated[
        str, typer.Argument(help="The path to XLSX file to parse the tables")
    ],
    llm: Annotated[
        AvailableLLM, typer.Argument(help="The LLM you want to answer your questions")
    ] = AvailableLLM.BAMBOO,
):
    suppress_stderr()
    auto_command(file_path, llm)


@app.command()
def manual(
    file_path: Annotated[
        str, typer.Argument(help="The path to XLSX file to parse the tables")
    ],
    llm: Annotated[
        AvailableLLM, typer.Argument(help="The LLM you want to answer your questions")
    ] = AvailableLLM.BAMBOO,
):
    suppress_stderr()
    manual_command(file_path, llm)


if __name__ == "__main__":
    app()
