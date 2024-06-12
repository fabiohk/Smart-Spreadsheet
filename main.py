import pandas as pd
from pandasai import Agent
from pandasai.llm import BambooLLM
import os

from auto_parser import AutoParser
from manual_parser import ManualParser

import typer

from utils import suppress_stderr
from typing_extensions import Annotated

def make_agent(dfs: list[pd.DataFrame], llm) -> Agent:
	return Agent(dfs, config={"llm": llm, "enforce_privacy": True})


app = typer.Typer()

suppress_stderr()

from enums import AvailableLLMs

from llms import make_agent

def main_loop(agent: Agent):
	while True:
		question = typer.prompt("Ask me anything")
		answer = agent.chat(question)
		if "Unfortunately, I was not able to answer your question" in answer:
			print("Unfortunately, I was not able to answer your question.")
		else:
			print(answer)


@app.command()
def auto(
	file_path: Annotated[str, typer.Argument(help="The path to XLSX file to parse the tables")],
	llm: Annotated[AvailableLLMs, typer.Argument(help="The LLM you want to answer your questions")] = AvailableLLMs.BAMBOO
):
	print("Starting to parse the file...")
	parser = AutoParser()
	tables = parser.parse_xlsx(file_path)
	agent = make_agent(tables, llm)
	main_loop(agent)


from manual_parser.types import TableInfo
from typing import Optional

def ask_for_table_info(sheet_name: Optional[str] = None):
	if sheet_name:
		use_previous_sheet_name = typer.confirm(f"Should use the previous sheet name ({sheet_name})?")
		if not use_previous_sheet_name:
			sheet_name = None

	if not sheet_name:
		sheet_name = typer.prompt("What is the sheet the table is?")
	topleft_cell = typer.prompt("What is the top left cell the table is in?")
	num_rows = int(typer.prompt("How many rows the table have?"))
	num_cols = int(typer.prompt("How many columns the table have?"))
	return TableInfo(sheet_name, topleft_cell, num_rows, num_cols)

@app.command()
def manual(
	file_path: Annotated[str, typer.Argument(help="The path to XLSX file to parse the tables")],
	llm: Annotated[AvailableLLMs, typer.Argument(help="The LLM you want to answer your questions")] = AvailableLLMs.BAMBOO
):
	print("I'll need to collect some information from the file...")
	tables_info = [ask_for_table_info()]
	last_sheet_name = tables_info[0].sheet_name
	has_another_table_to_add = typer.confirm("Do you have any other table to add?")

	while has_another_table_to_add:
		tables_info.append(ask_for_table_info(last_sheet_name))
		has_another_table_to_add = typer.confirm("Do you have any other table to add?")

	parser = ManualParser()
	tables = parser.parse_xlsx(file_path, tables_info)
	agent = make_agent(tables, llm)
	main_loop(agent)

if __name__ == "__main__":
	app()