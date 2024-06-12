import typer

from utils import suppress_stderr
from typing_extensions import Annotated

app = typer.Typer()

suppress_stderr()
from enums import AvailableLLM


from cli.manual_command import manual_command
from cli.auto_command import auto_command

@app.command()
def auto(
	file_path: Annotated[str, typer.Argument(help="The path to XLSX file to parse the tables")],
	llm: Annotated[AvailableLLM, typer.Argument(help="The LLM you want to answer your questions")] = AvailableLLM.BAMBOO
):
	auto_command(file_path, llm)

@app.command()
def manual(
	file_path: Annotated[str, typer.Argument(help="The path to XLSX file to parse the tables")],
	llm: Annotated[AvailableLLM, typer.Argument(help="The LLM you want to answer your questions")] = AvailableLLM.BAMBOO
):
	manual_command(file_path, llm)

if __name__ == "__main__":
	app()